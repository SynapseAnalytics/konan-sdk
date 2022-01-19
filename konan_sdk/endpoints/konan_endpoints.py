import datetime
from typing import Any, Dict, List, Union

from konan_sdk.endpoints.base_endpoint import (
    KonanBaseEndpoint,
    KonanBaseGenericDeploymentsEndpoint,
    KonanBaseDeploymentEndpoint,
    KonanEndpointOperationEnum,
)
from konan_sdk.endpoints.interfaces import (
    KonanEndpointRequest,
    KonanEndpointResponse,
)
from konan_sdk.konan_metrics import (
    KonanBaseMetric,
    KonanCustomMetric,
    KONAN_PREDEFINED_METRICS,
)
from konan_sdk.konan_types import (
    KonanCredentials,
    KonanDeployment,
    KonanDeploymentCreationRequest,
    KonanDeploymentCreationResponse,
    KonanDeploymentError,
    KonanDeploymentErrorType,
    KonanTokens,
    KonanPrediction,
    KonanFeedbackSubmission, KonanFeedbackStatus, KonanFeedbacksResult,
    KonanTimeWindow,
)


class LoginEndpoint(KonanBaseEndpoint[KonanCredentials, KonanTokens]):
    @property
    def name(self) -> str:
        return 'login'

    @property
    def endpoint_path(self) -> str:
        return '/api/auth/login/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(
        self, request_object: KonanCredentials
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(json={
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
        return '/api/auth/token/refresh/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(self, request_object: str) -> KonanEndpointRequest:
        return KonanEndpointRequest(json={'refresh': request_object})

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


class EvaluateEndpoint(
    KonanBaseDeploymentEndpoint[KonanTimeWindow, List[KonanBaseMetric]]
):
    @property
    def name(self) -> str:
        return 'evaluate'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/evaluate/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(
        self, request_object: KonanTimeWindow
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(json={
            'start_time': request_object.start_time.isoformat(),
            'end_time': request_object.end_time.isoformat(),
        })

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> List[KonanBaseMetric]:
        predfined_metrics_dict: Dict[str, Any] = endpoint_response.json['metrics'].get(
            "predefined", dict()
        )
        custom_metrics_list: List[Dict] = endpoint_response.json['metrics'].get(
            "custom", list()
        )

        metrics: List[KonanBaseMetric] = [
            KONAN_PREDEFINED_METRICS.get(metric_name, KonanCustomMetric)(
                metric_value, name=metric_name
            ) for metric_name, metric_value in predfined_metrics_dict.items()
        ] + [
            KonanCustomMetric(
                metric_dict["metric_value"],
                name=metric_dict["metric_name"]
            )
            for metric_dict in custom_metrics_list
        ]

        return metrics


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


class CreateDeploymentEndpoint(
    KonanBaseGenericDeploymentsEndpoint[
        KonanDeploymentCreationRequest,
        KonanDeploymentCreationResponse
    ]
):
    @property
    def name(self) -> str:
        return 'create-deployment'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(
        self, request_object: KonanDeploymentCreationRequest
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(json={
            'name': request_object.name,
            'docker_username': request_object.docker_credentials.username,
            'docker_password': request_object.docker_credentials.password,
            'image_url': request_object.docker_image.url,
            'exposed_port': request_object.docker_image.exposed_port,
        })

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> KonanDeploymentCreationResponse:
        return KonanDeploymentCreationResponse(
            KonanDeployment(
                endpoint_response.json['deployment']['uuid'],
                endpoint_response.json['deployment']['name'],
                datetime.datetime.fromisoformat(
                    endpoint_response.json['deployment']['created_at'],
                )
            ),
            [
                KonanDeploymentError(
                    KonanDeploymentErrorType(error['field']),
                    error['message'],
                ) for error in endpoint_response.json['errors']
            ],
            endpoint_response.json['container_logs']
        )


class DeleteDeployment(
    KonanBaseDeploymentEndpoint[
        None, bool
    ]
):
    @property
    def name(self) -> str:
        return 'delete-deployment'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.DELETE

    def prepare_request(
        self, request_object: None
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest()

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> bool:
        return True
