import json
import sys
from typing import Optional, Dict, Union, Tuple

import requests
from loguru import logger

from konan_sdk.endpoints import LOGIN_ENDPOINT, get_predict_endpoint, TOKEN_REFRESH_ENDPOINT
from konan_sdk.konan_user import KonanUser


class KonanSDK:
    # TODO: Create a generic function that handles requests, raising for status and extracting data
    def __init__(self, auth_url="https://auth.konan.ai", api_url="https://api.konan.ai", verbose=False):
        self.auth_url = auth_url
        self.api_url = api_url

        self.email = ''
        self.password = ''

        self.user: Optional[KonanUser] = None

        if not verbose:
            logger.remove()
            logger.add(sys.stderr, level="INFO")

    def login(self, email: str, password: str) -> KonanUser:
        # Save user credentials in case we need to login again
        self.email = email
        self.password = password

        # Login using provided credentials
        response = requests.post(
            self.auth_url + LOGIN_ENDPOINT,
            data={
                'email': email,
                'password': password
            }
        )
        # Raise any HTTP errors > 400
        # TODO: Check for 401, would mean invalid credentials were supplied
        response.raise_for_status()

        # Extract authentication tokens
        tokens = response.json()

        # Create a new user using these token
        self.user = KonanUser(tokens['access'], tokens['refresh'])

        logger.info(f"Successfully logged in using {self.email}")
        return self.user

    def _post_login_checks(self) -> None:
        assert self.user is not None, "User credentials were not provided. Please use the .login() function first."

    def refresh_token(self) -> None:
        self._post_login_checks()

        logger.debug("Sending token refresh request.")
        response = requests.post(
            self.auth_url + TOKEN_REFRESH_ENDPOINT,
            data={
                "refresh": self.user.refresh_token
            },

        )
        logger.debug("Received token refresh response. Parsing output.")

        response.raise_for_status()

        data = response.json()

        self.user.set_access_token(data['access'])

    def predict(self, deployment_uuid: str, input_data: Union[Dict, str]) -> Tuple[str, Dict]:
        self._post_login_checks()

        # Convert input to json string if it's a dict
        if isinstance(input_data, Dict):
            input_data = json.dumps(input_data)

        # Check if access token is valid and retrieve a new one if needed
        if not self.user.is_access_valid():
            if self.user.is_refresh_valid():
                logger.debug(f"Access token has expired. Refreshing.")
                self.refresh_token()
            else:
                logger.debug(f"Both access and refresh tokens have expired, re-logging in.")
                self.login(self.email, self.password)

        logger.debug("Sending prediction request.")
        response = requests.post(
            get_predict_endpoint(self.api_url, deployment_uuid),
            headers={
                'Authorization': f"Bearer {self.user.access_token}",
                'Content-Type': 'application/json',
            },
            data=input_data
        )
        logger.debug("Received prediction response. Parsing output.")

        response.raise_for_status()

        data = response.json()
        prediction_uuid = data.pop('prediction_uuid')
        return prediction_uuid, data['output']
