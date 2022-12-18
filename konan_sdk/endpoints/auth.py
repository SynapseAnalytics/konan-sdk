from konan_sdk.endpoints.base_endpoint import (
    KonanBaseEndpoint,
    KonanBaseLoginEndpoint,
    KonanEndpointOperationEnum,
)
from konan_sdk.endpoints.interfaces import (
    KonanEndpointRequest,
    KonanEndpointResponse,
)
from konan_sdk.konan_types import KonanCredentials


class APIKeyLoginEndpoint(KonanBaseLoginEndpoint[str]):
    @property
    def name(self) -> str:
        return 'login-api-key'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + "/api_key/"

    def prepare_request(
        self, request_object: str
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(json={
            'api_key': request_object,
        })


class LoginEndpoint(KonanBaseLoginEndpoint[KonanCredentials]):
    @property
    def name(self) -> str:
        return 'login'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + "/login/"

    def prepare_request(
        self, request_object: KonanCredentials
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(json={
            'email': request_object.email,
            'password': request_object.password
        })


class RefreshTokenEndpoint(KonanBaseEndpoint[str, str]):
    @property
    def name(self) -> str:
        return 'refresh_token'

    @property
    def endpoint_path(self) -> str:
        return '/api/auth/token/refresh/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(self, request_object: str) -> KonanEndpointRequest:
        return KonanEndpointRequest(json={'refresh': request_object})

    def process_response(self, endpoint_response: KonanEndpointResponse) -> str:
        return endpoint_response.json['access']
