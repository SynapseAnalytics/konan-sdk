import pytest
from typing import Type

from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse
from konan_sdk.endpoints.konan_endpoints import DeleteDeployment

from tests.endpoints.test_endpoint import EndpointCommonTests


class TestDeleteEndpoint(EndpointCommonTests):
    @property
    def _endpoint_class(self) -> Type[KonanBaseEndpoint]:
        return DeleteDeployment

    @pytest.mark.parametrize(
        argnames='request_object',
        argvalues=[
            None,
            1,
            {'key': 'value'},
        ],
        ids=[
            'None', 'int', 'dict'
        ]
    )
    def test_prepare_request(self, request_object):
        konan_endpoint_request = self.endpoint.prepare_request(request_object)
        assert isinstance(konan_endpoint_request, KonanEndpointRequest)
        assert konan_endpoint_request.params is None
        assert konan_endpoint_request.json is None

    def test_process_response(self):
        response: bool = self.endpoint.process_response(
            KonanEndpointResponse(
                status_code=204,
                json=None,
            )
        )

        assert isinstance(response, bool)
        assert response is True
