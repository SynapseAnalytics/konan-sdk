from typing import Type

import pytest

from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse
from konan_sdk.endpoints.konan_endpoints import PredictionEndpoint
from konan_sdk.konan_types import KonanPrediction

from tests.endpoints.test_endpoint import EndpointCommonTests


class TestPredictionEndpoint(EndpointCommonTests):
    @property
    def _endpoint_class(self) -> Type[KonanBaseEndpoint]:
        return PredictionEndpoint

    @pytest.mark.parametrize(
        argnames='predict_data',
        argvalues=[
            {},
            {
                'int_1': 1,
                'dict_2': {
                    'str_2_1': 'string',
                    'list_2_2': [
                        'element_1',
                        2,
                        {
                            'key': 'value',
                        },
                    ],
                },
            },
        ],
        ids=['empty-data', 'normal-data'],
    )
    def test_prepare_request(self, predict_data):
        konan_endpoint_request = self.endpoint.prepare_request(
            predict_data,
        )

        assert isinstance(konan_endpoint_request, KonanEndpointRequest)
        assert konan_endpoint_request.params is None
        assert isinstance(konan_endpoint_request.json, dict)
        assert konan_endpoint_request.json == predict_data

    @pytest.mark.parametrize(
        argnames='output',
        argvalues=[
            0.8,
            'car',
            {
                'type': 'client',
                'loan_amount': 230000,
            },
        ],
        ids=[
            'int',
            'string',
            'dict',
        ],
    )
    def test_process_response(self, output):
        konan_prediction: KonanPrediction = self.endpoint.process_response(
            KonanEndpointResponse(
                status_code=200,
                json={
                    'prediction_uuid': self.prediction_uuid,
                    'output': output,
                },
            )
        )

        assert isinstance(konan_prediction, KonanPrediction)
        assert konan_prediction.uuid == self.prediction_uuid
        assert konan_prediction.output == output
