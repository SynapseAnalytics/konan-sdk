
import json
import sys
from typing import Optional, Dict, Union, Tuple


from konan_sdk.konan_user import KonanUser
from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint
from konan_sdk.endpoints.utils import get_predict_endpoint, LOGIN_ENDPOINT, TOKEN_REFRESH_ENDPOINT


class LoginEndpoint(KonanBaseEndpoint):
    def __init__(self, api_url, user):
        super().__init__(api_url=api_url, name='login', user=user)

    def prepare_request(self, *kwargs):
        self.request_url = self.api_url + LOGIN_ENDPOINT

class RefreshTokenEndpoint(KonanBaseEndpoint):
    def __init__(self, api_url, user) -> None:
        super().__init__(api_url=api_url, name='refresh_token', user=user)

    def prepare_request(self, *kwargs):
        self.request_url = self.api_url + TOKEN_REFRESH_ENDPOINT

class PredictionEndpoint(KonanBaseEndpoint):

    def __init__(self, api_url, deployment_uuid, user) -> None:
        super().__init__(name="predict", api_url=api_url, user=user)

        self.deployment_uuid = deployment_uuid
        self.headers = {
                'Authorization': f"Bearer {self.user.access_token}",
                'Content-Type': 'application/json',
            }

    def prepare_request(self):
        self.request_url = get_predict_endpoint(api_url=self.api_url, deployment_uuid=self.deployment_uuid)


    def process_response(self):

        prediction_uuid = self.response.pop('prediction_uuid')
        self.response = prediction_uuid, self.response



