
import requests

from loguru import logger
from typing import Optional

from konan_sdk.konan_user import KonanUser
from konan_sdk.endpoints.utils import LOGIN_ENDPOINT, TOKEN_REFRESH_ENDPOINT
from konan_sdk.endpoints.konan_endpoints import LoginEndpoint, RefreshTokenEndpoint


class KonanAuth:
    def __init__(self, auth_url: str, email: str, password: str):

        self.auth_url = auth_url
        self.email = email
        self.password = password
        self.user: Optional[KonanUser] = None


    def login(self) -> KonanUser:

        payload =  { 'email': self.email,
                    'password': self.password}

        response = LoginEndpoint(api_url=self.auth_url, user=self.user).post(payload=payload)

        logger.info(f"Successfully logged in using {self.email}")

        self.user = KonanUser(response['access'], response['refresh'])

        return self.user

    def _post_login_checks(self) -> None:
        assert self.user is not None, "User credentials were not provided. Please use the .login() function first."

    def refresh_token(self) -> None:
        self._post_login_checks()
        payload = { "refresh": self.user.refresh_token }

        response = RefreshTokenEndpoint(api_url=self.auth_url, user=self.user).post(payload=payload)

        self.user.set_access_token(response['access'])

    def auto_refresh_token(self) -> None:

        # Check if access token is valid and retrieve a new one if needed
        if not self.user.is_access_valid():
            if self.user.is_refresh_valid():
                logger.debug(f"Access token has expired. Refreshing.")
                self.auth.refresh_token()
            else:
                logger.debug(f"Both access and refresh tokens have expired, re-logging in.")
                self.login(self.email, self.password)