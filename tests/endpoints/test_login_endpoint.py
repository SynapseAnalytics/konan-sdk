from typing import Type

from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse
from konan_sdk.endpoints.konan_endpoints import LoginEndpoint
from konan_sdk.konan_types import KonanCredentials, KonanTokens

from tests.endpoints.test_endpoint import EndpointCommonTests


class TestLoginEndpoint(EndpointCommonTests):
    @property
    def _endpoint_class(self) -> Type[KonanBaseEndpoint]:
        return LoginEndpoint

    def test_prepare_request(self):
        email = 'test@email.com'
        password = 'super-secure-password'

        konan_endpoint_request = self.endpoint.prepare_request(
            KonanCredentials(email, password)
        )
        assert isinstance(konan_endpoint_request, KonanEndpointRequest)
        assert konan_endpoint_request.params is None
        assert isinstance(konan_endpoint_request.json, dict)
        assert konan_endpoint_request.json == {
            'email': email,
            'password': password,
        }

    def test_process_response(self):
        konan_tokens: KonanTokens = self.endpoint.process_response(
            KonanEndpointResponse(
                status_code=200,
                json={
                    'access': self.access_token,
                    'refresh': self.refresh_token,
                },
            )
        )
        assert isinstance(konan_tokens, KonanTokens)
        assert konan_tokens.access == self.access_token
        assert konan_tokens.refresh == self.refresh_token
