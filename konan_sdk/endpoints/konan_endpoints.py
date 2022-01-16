import datetime
from typing import Any, Dict, List, Union

from konan_sdk.endpoints.base_endpoint import (
    KonanBaseEndpoint,
    KonanBaseGenericDeploymentsEndpoint,
    KonanBaseDeploymentEndpoint,
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


class EvaluateEndpoint(
    KonanBaseDeploymentEndpoint[KonanTimeWindow, List[KonanBaseMetric]]
):
    @property
    def name(self) -> str:
        return 'evaluate'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/evaluate'

    def prepare_request(
        self, request_object: KonanTimeWindow
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(data={
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
        return super().endpoint_path + '/predictions/feedback'

    def prepare_request(
        self, request_object: List[KonanFeedbackSubmission]
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(
            data={
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

    def prepare_request(
        self, request_object: KonanDeploymentCreationRequest
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(data={
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

    # TODO: Currently, every endpoint class exposes BOTH .get() and .post()
    # TODO: Perhaps it is better to explicitly support both or split them
    def get(
        self, request_object: KonanDeploymentCreationRequest
    ) -> KonanDeploymentCreationResponse:
        """Lists all deployments that this user has access to

        :param request_object: endpoint request
        :type request_object: KonanDeploymentCreationRequest
        :raises NotImplementedError: Method not impelmented yet
        :return: endpoint response
        :rtype: KonanDeploymentCreationResponse
        """
        raise NotImplementedError()
