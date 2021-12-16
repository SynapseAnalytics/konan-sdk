
import requests

from loguru import logger
from typing import Optional

from konan_sdk.konan_user import KonanUser
from konan_sdk.endpoints.utils import LOGIN_ENDPOINT, TOKEN_REFRESH_ENDPOINT


class KonanAuth:
    def __init__(self, auth_url: str, email: str, password: str):

        self.auth_url = auth_url
        self.email = email
        self.password = password
        self.user: Optional[KonanUser] = None


    def login(self) -> KonanUser:

        payload = { 'email': self.email,
                    'password': self.password}

        # Login using provided credentials
        response = requests.post(
            self.auth_url + LOGIN_ENDPOINT,
            data=payload
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


    def auto_refresh_token(self) -> None:

        # Check if access token is valid and retrieve a new one if needed
        if not self.user.is_access_valid():
            if self.user.is_refresh_valid():
                logger.debug(f"Access token has expired. Refreshing.")
                self.auth.refresh_token()
            else:
                logger.debug(f"Both access and refresh tokens have expired, re-logging in.")
                self.login(self.email, self.password)