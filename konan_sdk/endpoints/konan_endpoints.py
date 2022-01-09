from typing import Dict, Union
from konan_sdk.endpoints.base_endpoint import (
    KonanBaseEndpoint, KonanBaseDeploymentEndpoint
)
from konan_sdk.endpoints.interfaces import (
    KonanEndpointRequest, KonanEndpointResponse
)
from konan_sdk.konan_types import (
    KonanCredentials, KonanTokens,
    KonanPrediction
)


class LoginEndpoint(KonanBaseEndpoint[KonanCredentials, KonanTokens]):
    @property
    def name(self) -> str:
        return 'login'

    @property
    def endpoint_path(self) -> str:
        return '/api/auth/login'

    def prepare_request(
        self, request_object: KonanCredentials
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(data={
            'email': request_object.email,
            'password': request_object.password
        })

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> KonanTokens:
        return KonanTokens(
            endpoint_response.json['access'],
            endpoint_response.json['refresh']
        )


class RefreshTokenEndpoint(KonanBaseEndpoint[str, str]):
    @property
    def name(self) -> str:
        return 'refresh_token'

    @property
    def endpoint_path(self) -> str:
        return '/api/auth/token/refresh'

    def prepare_request(self, request_object: str) -> KonanEndpointRequest:
        return KonanEndpointRequest(data={'refresh': request_object})

    def process_response(self, endpoint_response: KonanEndpointResponse) -> str:
        return endpoint_response.json['access']


class PredictionEndpoint(
    KonanBaseDeploymentEndpoint[Union[Dict, str], KonanPrediction]
):
    @property
    def name(self) -> str:
        return 'predict'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/predict'

    def prepare_request(
        self, request_object: Union[Dict, str]
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(data=request_object)

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> KonanPrediction:
        return KonanPrediction(
            endpoint_response.json['prediction_uuid'],
            endpoint_response.json['output']
        )
