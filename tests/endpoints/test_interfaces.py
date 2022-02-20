import pytest

from konan_sdk.endpoints.interfaces import (
    KonanEndpointRequest,
    KonanEndpointResponse
)


class TestInterfaces():
    @pytest.mark.parametrize(
        argnames=["params", "json"],
        argvalues=[
            ({'param_1': 'p_value_1', 'param_2': 'p_value_2'}, {'json_1': 1, 'json_2': 2}),
            (None, {'json_1': 1, 'json_2': 2}),
            ({'param_1': 'p_value_1', 'param_2': 'p_value_2'}, None),
            (None, None),
        ],
        ids=[
            "params and json with value",
            "json with value",
            "params with value",
            "params and json with None",
        ],
    )
    def test_konan_endpoint_request(self, params, json):
        endpoint_request = KonanEndpointRequest(
            params=params,
            json=json,
        )
        assert endpoint_request.params == params
        assert endpoint_request.json == json

    @pytest.mark.parametrize(
        argnames=["status_code", "json"],
        argvalues=[
            (500, {'json_1': 1, 'json_2': 2}),
            (200, None),
        ],
        ids=[
            "status_code and json with value",
            "status_code with value",
        ],
    )
    def test_konan_endpoint_response(self, status_code, json):
        endpoint_request = KonanEndpointResponse(
            status_code=status_code,
            json=json,
        )
        assert endpoint_request.status_code == status_code
        assert endpoint_request.json == json
