import datetime
from typing import List

from konan_sdk.endpoints.base_endpoint import (
    KonanBaseDeploymentEndpoint,
    KonanBaseDeploymentGenericModelsEndpoint,
    KonanBaseModelEndpoint,
    KonanEndpointOperationEnum,
)
from konan_sdk.endpoints.interfaces import (
    KonanEndpointRequest,
    KonanEndpointResponse,
)
from konan_sdk.konan_types import (
    KonanLiveModelSwitchState,
    KonanModelCreationRequest,
    KonanModelState,
    KonanModel,
)
from konan_sdk.konan_utils.enums import string_to_konan_enum


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
