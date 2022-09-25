import datetime
from typing import Any, Dict, Generator, List, Union

from konan_sdk.endpoints.base_endpoint import (
    KonanBaseDeploymentPredictionsEndpoint,
    KonanBaseEndpoint,
    KonanBaseGenericDeploymentsEndpoint,
    KonanBaseDeploymentEndpoint,
    KonanBaseDeploymentGenericModelsEndpoint,
    KonanBaseModelEndpoint,
    KonanBaseLoginEndpoint,
    KonanEndpointOperationEnum,
)
from konan_sdk.endpoints.interfaces import (
    KonanEndpointRequest,
    KonanEndpointResponse,
)
from konan_sdk.endpoints.mixins import KonanPaginatedEndpointMixin
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
    KonanLiveModelSwitchState,
    KonanModelCreationRequest,
    KonanModelState,
    KonanModel,
    KonanProjectCreationRequest,
    KonanPrediction,
    KonanFeedbackSubmission, KonanFeedbackStatus, KonanFeedbacksResult,
    KonanTimeWindow,
)
from konan_sdk.konan_utils.enums import string_to_konan_enum


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
            ) for metric_name, metric_value in predfined_metrics_dict.items() if metric_value is not None
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
        request_dict = {
            'deployment_name': request_object.name,
            'model_name': request_object.model_creation_request.name,
            'image_url': request_object.model_creation_request.docker_image.url,
            'exposed_port': request_object.model_creation_request.docker_image.exposed_port,
        }
        if request_object.model_creation_request.docker_credentials is not None:
            request_dict['docker_username'] = request_object.model_creation_request.docker_credentials.username
            request_dict['docker_password'] = request_object.model_creation_request.docker_credentials.password

        return KonanEndpointRequest(json=request_dict)

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
            KonanModel(
                endpoint_response.json['deployment']['model']['uuid'],
                endpoint_response.json['deployment']['model']['name'],
                datetime.datetime.fromisoformat(
                    endpoint_response.json['deployment']['model']['created_at'],
                ),
                string_to_konan_enum(
                    endpoint_response.json['deployment']['model']['state'],
                    KonanModelState,
                ),
            ),
            [
                KonanDeploymentError(
                    KonanDeploymentErrorType(error['field']),
                    error['message'],
                ) for error in endpoint_response.json['errors']
            ],
            endpoint_response.json['container_logs'],
        )


class CreateProjectEndpoint(
    KonanBaseGenericDeploymentsEndpoint[
        KonanProjectCreationRequest,
        KonanDeployment
    ]
):
    @property
    def name(self) -> str:
        return 'create-project'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(
        self, request_object: KonanProjectCreationRequest
    ) -> KonanEndpointRequest:
        request_dict = {
            'name': request_object.name,
        }
        if request_object.description:
            request_dict['description'] = request_object.description

        return KonanEndpointRequest(json=request_dict)

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> KonanDeployment:
        return KonanDeployment(
            endpoint_response.json['uuid'],
            endpoint_response.json['name'],
            datetime.datetime.fromisoformat(
                endpoint_response.json['created_at'],
            )
        )


class CreateModelEndpoint(
    KonanBaseDeploymentGenericModelsEndpoint[
        KonanModelCreationRequest,
        KonanModel,
    ]
):
    @property
    def name(self) -> str:
        return 'create-model'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(
        self, request_object: KonanModelCreationRequest
    ) -> KonanEndpointRequest:
        request_dict = {
            'name': request_object.name,
            'image_url': request_object.docker_image.url,
            'exposed_port': request_object.docker_image.exposed_port,
            'state': request_object.state.value,
        }
        if request_object.docker_credentials is not None:
            request_dict['docker_username'] = request_object.docker_credentials.username
            request_dict['docker_password'] = request_object.docker_credentials.password

        return KonanEndpointRequest(json=request_dict)

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> KonanModel:
        return KonanModel(
            endpoint_response.json['model']['uuid'],
            endpoint_response.json['model']['name'],
            datetime.datetime.fromisoformat(
                endpoint_response.json['model']['created_at'],
            ),
            string_to_konan_enum(
                endpoint_response.json['model']['state'],
                KonanModelState,
            ),
        )


class GetModelsEndpoint(
    KonanBaseDeploymentGenericModelsEndpoint[
        None,
        List[KonanModel],
    ]
):
    @property
    def name(self) -> str:
        return 'get-models'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.GET

    def prepare_request(
        self, request_object: None
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest()

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> List[KonanModel]:
        return [
            KonanModel(
                model['uuid'],
                model['name'],
                datetime.datetime.fromisoformat(
                    model['created_at'],
                ),
                string_to_konan_enum(
                    model['state'],
                    KonanModelState,
                ),
            ) for model in endpoint_response.json['results']
        ]


class DeleteModelEndpoint(
    KonanBaseModelEndpoint[
        None, bool
    ]
):
    @property
    def name(self) -> str:
        return 'delete-model'

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


class SwitchLiveModelEndpoint(
    KonanBaseDeploymentEndpoint[
        KonanLiveModelSwitchState,
        None,
    ]
):
    @property
    def name(self) -> str:
        return 'switch-model-live'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/switch/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(
        self, request_object: KonanLiveModelSwitchState
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(
            json={
                "switch_to": request_object.switch_to.value,
                "new_live_model": request_object.new_live_model_uuid,
            },
        )

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> None:
        return None


class SwitchNonLiveModelEndpoint(
    KonanBaseModelEndpoint[
        KonanModelState,
        None,
    ]
):
    @property
    def name(self) -> str:
        return 'switch-model-nonelive'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/switch/'

    @property
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        return KonanEndpointOperationEnum.POST

    def prepare_request(
        self, request_object: KonanModelState
    ) -> KonanEndpointRequest:
        return KonanEndpointRequest(
            json={
                "switch_to": request_object.value,
            },
        )

    def process_response(
        self, endpoint_response: KonanEndpointResponse
    ) -> None:
        return None


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


class GetPredictionsEndpoint(
    KonanPaginatedEndpointMixin[KonanTimeWindow, KonanPrediction],
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
