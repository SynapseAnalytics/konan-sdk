from typing import Any, Dict, Generator, List, Union

from konan_sdk.endpoints.base_endpoint import (
    KonanBaseDeploymentPredictionsEndpoint,
    KonanBaseDeploymentEndpoint,
    KonanEndpointOperationEnum,
)
from konan_sdk.endpoints.interfaces import (
    KonanEndpointRequest,
    KonanEndpointResponse,
)
from konan_sdk.endpoints.mixins import KonanPaginatedEndpointMixin
from konan_sdk.konan_types import (
    KonanPrediction,
    KonanFeedbackSubmission, KonanFeedbackStatus, KonanFeedbacksResult,
    KonanTimeWindow,
)


class PredictionEndpoint(
    KonanBaseDeploymentEndpoint[Union[Dict, str], KonanPrediction]
):
    @property
    def name(self) -> str:
        return 'predict'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/predict/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(
        self, request_object: Union[Dict, str]
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(json=request_object)

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> KonanPrediction:
        return KonanPrediction(
            endpoint_response.json['prediction_uuid'],
            endpoint_response.json['output']
        )


class FeedbackEndpoint(
    KonanBaseDeploymentEndpoint[
        List[KonanFeedbackSubmission], KonanFeedbacksResult
    ]
):
    @property
    def name(self) -> str:
        return 'feedback'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/predictions/feedback/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(
        self, request_object: List[KonanFeedbackSubmission]
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(
            json={
                "feedback": [
                    {
                        "prediction_uuid": feedback.prediction_uuid,
                        "target": feedback.target,
                    } for feedback in request_object
                ]
            }
        )

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> KonanFeedbacksResult:
        return KonanFeedbacksResult(
            [
                KonanFeedbackStatus(
                    feedback_status['prediction_uuid'],
                    feedback_status['status'],
                    feedback_status['message'],
                ) for feedback_status in endpoint_response.json["data"]
            ],
            endpoint_response.json['success'],
            endpoint_response.json['failure'],
            endpoint_response.json['total']
        )


class GetPredictionsEndpoint(
    KonanBaseDeploymentPredictionsEndpoint[
        KonanTimeWindow,
        Generator[List[KonanPrediction], None, None],
    ]
):
    @property
    def name(self) -> str:
        return 'get-predictions'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/'

    def prepare_request(
        self, request_object: KonanTimeWindow,
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(params={
            'start_time': request_object.start_time.isoformat(),
            'end_time': request_object.end_time.isoformat(),
        })


class GetPaginatedPredictionsEndpoint(
    KonanPaginatedEndpointMixin[KonanTimeWindow, KonanPrediction],
    GetPredictionsEndpoint,
):
    def _process_page(
        self, results: List[Dict[str, Any]]
    ) -> List[KonanPrediction]:
        return [
            KonanPrediction(
                uuid=prediction['uuid'],
                output=prediction['mls_output_json'],
                features=prediction.get('features_json'),
                feedback=prediction.get('feedback'),
            ) for prediction in results
        ]
