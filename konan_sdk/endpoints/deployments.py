import datetime
from typing import Any, Dict, List

from konan_sdk.endpoints.base_endpoint import (
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
    KonanDeployment,
    KonanDeploymentCreationRequest,
    KonanDeploymentCreationResponse,
    KonanDeploymentError,
    KonanDeploymentErrorType,
    KonanModelState,
    KonanModel,
    KonanProjectCreationRequest,
    KonanTimeWindow,
)
from konan_sdk.konan_utils.enums import string_to_konan_enum


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
