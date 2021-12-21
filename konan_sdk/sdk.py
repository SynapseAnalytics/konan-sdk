import json
from konan_sdk.auth import KonanAuth
import sys
from typing import Optional, Dict, Union, Tuple

from loguru import logger

from konan_sdk.konan_user import KonanUser
from konan_sdk.endpoints.konan_endpoints import PredictionEndpoint

class KonanSDK:
    # TODO: Create a generic function that handles requests, raising for status and extracting data
    def __init__(self, auth_url="https://auth.konan.ai", api_url="https://api.konan.ai", verbose=False):
        self.auth_url = auth_url
        self.api_url = api_url

        self.email = ''
        self.password = ''

        self.user: Optional[KonanUser] = None
        self.auth: Optional[KonanAuth] = None

        if not verbose:
            logger.remove()
            logger.add(sys.stderr, level="INFO")

    def login(self, email: str, password: str) -> KonanUser:

        self.auth = KonanAuth(email=email, password=password, auth_url=self.auth_url)
        self.user = self.auth.login()
        return self.user

    def predict(self, deployment_uuid: str, input_data: Union[Dict, str]) -> Tuple[str, Dict]:

        # check user performed login
        self.auth._post_login_checks()

        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        prediction_uuid, output = PredictionEndpoint(api_url=self.api_url, user=self.user, deployment_uuid=deployment_uuid).post(payload=input_data)

        return prediction_uuid, output




