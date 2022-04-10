import datetime
from typing import List, Type
import pytest

from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse
from konan_sdk.endpoints.konan_endpoints import EvaluateEndpoint
from konan_sdk.konan_metrics import KONAN_PREDEFINED_METRICS, KonanBaseMetric, KonanCustomMetric
from konan_sdk.konan_types import KonanTimeWindow

from tests.endpoints.test_endpoint import EndpointCommonTests


class TestEvaluateEndpoint(EndpointCommonTests):
    @property
    def _endpoint_class(self) -> Type[KonanBaseEndpoint]:
        return EvaluateEndpoint

    @pytest.mark.parametrize(
        argnames=['start_time_iso', 'end_time_iso'],
        argvalues=[
            ('2022-02-01T09:14:57', '2022-02-01T11:14:57'),
            ('2022-02-01T11:14:57+02:00', '2022-02-01T13:14:57+02:00'),
        ],
        ids=[
            'UTC', '+02:00'
        ]
    )
    def test_prepare_request(self, start_time_iso, end_time_iso):
        konan_endpoint_request = self.endpoint.prepare_request(
            KonanTimeWindow(
                datetime.datetime.fromisoformat(start_time_iso),
                datetime.datetime.fromisoformat(end_time_iso),
            )
        )
        assert isinstance(konan_endpoint_request, KonanEndpointRequest)
        assert konan_endpoint_request.params is None
        assert isinstance(konan_endpoint_request.json, dict)
        assert konan_endpoint_request.json == {
            'start_time': start_time_iso,
            'end_time': end_time_iso,
        }

    @pytest.mark.parametrize(
        argnames=['predefined_metrics', 'custom_metrics'],
        argvalues=[
            (
                {},
                [],
            ),
            (
                {
                    'rmse': 2.3,
                    'precision': 0.9,
                },
                [],
            ),
            (
                {
                    'f1_score': 2.3,
                    'precision': None,
                },
                [],
            ),
            (
                {
                    'accuracy': 0.8,
                },
                [],
            ),
            (
                {},
                [
                    {
                        'metric_name': 'accuracy',
                        'metric_value': 0.8,
                    },
                ],
            ),
            (
                {
                    'rmse': None,
                },
                [
                    {
                        'metric_name': 'accuracy',
                        'metric_value': 0.8,
                    },
                ],
            ),
        ],
        ids=[
            'no-metrics',
            'multiple-predefined-metrics',
            'predefined-metric-None',
            'new-predefined-metric',
            'custom-metric',
            'predefined-metric-None_custom-metric',
        ],
    )
    def test_process_response(self, predefined_metrics, custom_metrics):
        expected_metrics: List[KonanBaseMetric] = [
            KONAN_PREDEFINED_METRICS.get(metric_name, KonanCustomMetric)(
                metric_value,
                name=metric_name,
            )
            for metric_name, metric_value in predefined_metrics.items() if metric_value is not None
        ] + [
            KonanCustomMetric(
                metric['metric_value'],
                name=metric['metric_name'],
            )
            for metric in custom_metrics if metric['metric_name'] is not None and metric['metric_value'] is not None
        ]

        returned_metrics: List[KonanBaseMetric] = self.endpoint.process_response(
            KonanEndpointResponse(
                status_code=200,
                json={
                    'metrics': {
                        'predefined': predefined_metrics,
                        'custom': custom_metrics,
                    },
                },
            )
        )

        assert isinstance(returned_metrics, List)
        assert all([isinstance(metric, KonanBaseMetric) for metric in returned_metrics])
        assert len(returned_metrics) == len(expected_metrics)
        assert set(returned_metrics) == set(expected_metrics)
