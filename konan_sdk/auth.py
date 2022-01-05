
from loguru import logger
from typing import Optional

from konan_sdk.konan_user import KonanUser
from konan_sdk.endpoints.konan_endpoints import LoginEndpoint, RefreshTokenEndpoint


class KonanAuth:
    def __init__(self, auth_url: str, email: str, password: str):
        self.auth_url = auth_url
        self.email = email
        self.password = password
        self.user: Optional[KonanUser] = None

    def login(self) -> KonanUser:
        response: LoginEndpoint.ResponseObject = LoginEndpoint(
            api_url=self.auth_url, user=self.user
        ).post(LoginEndpoint.RequestObject(self.email, self.password))

        logger.info(f"Successfully logged in using {self.email}")

        self.user = KonanUser(response.access_token, response.refresh_token)
        return self.user

    def _post_login_checks(self) -> None:
        assert self.user is not None, "User credentials were not provided. Please use the .login() method first."

    def refresh_token(self) -> None:
        self._post_login_checks()

        response: RefreshTokenEndpoint.ResponseObject = RefreshTokenEndpoint(
            api_url=self.auth_url, user=self.user
        ).post(RefreshTokenEndpoint.RequestObject(refresh_token=self.user.refresh_token))
        self.user.set_access_token(response.access_token)

    def auto_refresh_token(self) -> None:

        # Check if access token is valid and retrieve a new one if needed
        if not self.user.is_access_valid():
            if self.user.is_refresh_valid():
                logger.debug("Access token has expired. Refreshing.")
                self.refresh_token()
            else:
                logger.debug("Both access and refresh tokens have expired, re-logging in.")
                self.login()
