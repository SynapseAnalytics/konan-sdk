from typing import Type

from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse
from konan_sdk.endpoints.konan_endpoints import RefreshTokenEndpoint

from tests.endpoints.test_endpoint import EndpointCommonTests


class TestRefreshTokenEndpoint(EndpointCommonTests):
    @property
    def _endpoint_class(self) -> Type[KonanBaseEndpoint]:
        return RefreshTokenEndpoint

    def test_prepare_request(self):
        konan_endpoint_request = self.endpoint.prepare_request(
            self.refresh_token,
        )

        assert isinstance(konan_endpoint_request, KonanEndpointRequest)
        assert konan_endpoint_request.params is None
        assert isinstance(konan_endpoint_request.json, dict)
        assert konan_endpoint_request.json == {
            'refresh': self.refresh_token,
        }

    def test_process_response(self):
        access_token: str = self.endpoint.process_response(
            KonanEndpointResponse(
                status_code=200,
                json={
                    'access': self.access_token,
                },
            )
        )

        assert isinstance(access_token, str)
        assert access_token == self.access_token
