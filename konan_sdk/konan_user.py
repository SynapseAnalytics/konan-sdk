from calendar import timegm
from datetime import datetime
from enum import Enum

import jwt


class TokenType(Enum):
    ACCESS = 1
    REFRESH = 2


class KonanUser:
    def __init__(self, access_token: str, refresh_token: str) -> None:
        self.access_token = None
        self.refresh_token = None

        # User Details
        self.email = ''
        self.first_name = ''
        self.last_name = ''
        self.organization_id = ''

        # Expiration Times
        self.access_exp = 0
        self.refresh_exp = 0

        self.set_access_token(access_token)
        self.set_refresh_token(refresh_token)

    def set_access_token(self, access_token: str) -> None:
        self.access_token = access_token

        access_token_payload = jwt.decode(access_token, options={"verify_signature": False})

        # Get user details
        self.email = access_token_payload['email']
        self.first_name = access_token_payload['first_name']
        self.last_name = access_token_payload['last_name']
        self.organization_id = access_token_payload['organization_id']

        self.access_exp = access_token_payload['exp']

    def set_refresh_token(self, refresh_token: str) -> None:
        self.refresh_token = refresh_token

        refresh_token_payload = jwt.decode(refresh_token, options={"verify_signature": False})

        self.refresh_exp = refresh_token_payload['exp']

    def _is_token_valid(self, token_type: TokenType):
        now = timegm(datetime.utcnow().utctimetuple())

        if token_type is TokenType.ACCESS:
            return self.access_exp > now
        elif token_type is TokenType.REFRESH:
            return self.refresh_exp > now
        else:
            raise TypeError("Unhandled TokenType in is_token_valid()")

    def is_access_valid(self):
        return self._is_token_valid(TokenType.ACCESS)

    def is_refresh_valid(self):
        return self._is_token_valid(TokenType.REFRESH)

    def __str__(self):
        return self.email
