
from abc import abstractmethod
from loguru import logger
from typing import Optional
from konan_sdk.konan_types import KonanCredentials
import deprecated

from konan_sdk.konan_user import KonanUser
from konan_sdk.endpoints.auth import APIKeyLoginEndpoint, LoginEndpoint, RefreshTokenEndpoint


class _AbstractKonanAuth():
    def __init__(self, auth_url: str) -> None:
        self.auth_url = auth_url
        self.user: Optional[KonanUser] = None

    def _post_login_checks(self) -> None:
        assert self.user is not None, "User credentials were not provided. Please use the .login() method first."

    def refresh_token(self) -> None:
        self._post_login_checks()

        new_access_token = RefreshTokenEndpoint(self.auth_url).request(
            self.user.refresh_token
        )
        self.user.set_access_token(new_access_token)

    def auto_refresh_token(self) -> None:
        # Check if access token is valid and retrieve a new one if needed
        if not self.user.is_access_valid():
            if self.user.is_refresh_valid():
                logger.debug("Access token has expired. Refreshing.")
                self.refresh_token()
            else:
                logger.debug("Both access and refresh tokens have expired, re-logging in.")
                self.login()

    @abstractmethod
    def login(self) -> KonanUser:
        ...


@deprecated.deprecated(
    reason='Password authentication is not recommonded. Use API Key authentication instead',
    version='1.4.0',
    category=DeprecationWarning,
)
class KonanAuth(_AbstractKonanAuth):
    def __init__(self, auth_url: str, email: str, password: str, *args, **kwargs) -> None:
        self.email = email
        self.password = password
        super().__init__(auth_url=auth_url, *args, **kwargs)

    def login(self) -> KonanUser:
        response = LoginEndpoint(self.auth_url).request(
            KonanCredentials(self.email, self.password)
        )

        logger.info(f"Successfully logged in using {self.email}")

        self.user = KonanUser(response.access, response.refresh)
        return self.user


class KonanAPIKeyAuth(_AbstractKonanAuth):
    def __init__(self, auth_url: str, api_key: str, *args, **kwargs) -> None:
        self.api_key = api_key
        super().__init__(auth_url=auth_url, *args, **kwargs)

    def login(self) -> KonanUser:
        response = APIKeyLoginEndpoint(self.auth_url).request(request_object=self.api_key)

        logger.info("Successfully logged in using an API Key")

        self.user = KonanUser(response.access, response.refresh)
        return self.user
