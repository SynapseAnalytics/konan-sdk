import datetime
from typing import Any, Dict, List, Type
import pytest
import pytz

from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse
from konan_sdk.endpoints.konan_endpoints import CreateDeploymentEndpoint
from konan_sdk.konan_types import KonanDeploymentCreationRequest, KonanDeploymentCreationResponse, KonanDeploymentError, KonanDeploymentErrorType, KonanDockerCredentials, KonanDockerImage

from tests.endpoints.test_endpoint import EndpointCommonTests


class TestEvaluateEndpoint(EndpointCommonTests):
    @property
    def _endpoint_class(self) -> Type[KonanBaseEndpoint]:
        return CreateDeploymentEndpoint

    def test_prepare_request(self):
        deployment_name = 'deployment-name'
        docker_username = 'awesome-data-scientist'
        docker_password = 'super-secure-password'
        image_url = 'my-docker-hub.com/docker-repo/image-name:image-tag',
        exposed_port = 8000

        konan_endpoint_request = self.endpoint.prepare_request(
            KonanDeploymentCreationRequest(
                deployment_name, KonanDockerCredentials(docker_username, docker_password),
                KonanDockerImage(image_url, exposed_port),
            )
        )

        assert isinstance(konan_endpoint_request, KonanEndpointRequest)
        assert konan_endpoint_request.params is None
        assert isinstance(konan_endpoint_request.json, dict)
        assert konan_endpoint_request.json == {
            'docker_username': docker_username,
            'docker_password': docker_password,
            'image_url': image_url,
            'exposed_port': exposed_port,
            'name': deployment_name,
        }

    @pytest.mark.parametrize(
        argnames=['created_at', 'errors'],
        argvalues=[
            (
                datetime.datetime(2022, 2, 1, hour=9, minute=14, second=57),
                [],
            ),
            (
                datetime.datetime(2022, 2, 1, hour=11, minute=14, second=57, tzinfo=pytz.timezone('Africa/Cairo')),
                [],
            ),
            (
                datetime.datetime(2022, 2, 1, hour=9, minute=14, second=57),
                [
                    {
                        'field': 'image',
                        'message': 'Cant find image',
                    },
                    {
                        'field': 'health_endpoint',
                        'message': 'Cant find reach healthz endpoint',
                    },
                    {
                        'field': 'exposed_port',
                        'message': 'Forbidden port used',
                    },
                ],
            ),
            (
                datetime.datetime(2022, 2, 1, hour=9, minute=14, second=57),
                [
                    {
                        'field': 'new_error',
                        'message': 'Very descriptive error message',
                    },
                ],
            ),
        ],
        ids=[
            'no errors',
            '+02:00 time',
            'all error types',
            'new_error_type',
        ]
    )
    def test_process_response(self, created_at: datetime.datetime, errors: List[Dict[str, Any]]):
        container_logs = 'very-detailed-logs'
        deployment_name = 'deployment-name'
        expected_deployment_errors = [
            KonanDeploymentError(
                KonanDeploymentErrorType(error['field']), error['message']
            )
            for error in errors if error['field'] in [e.value for e in KonanDeploymentErrorType]
        ] + [
            KonanDeploymentError(
                KonanDeploymentErrorType.Other, error['message']
            )
            for error in errors if error['field'] not in [e.value for e in KonanDeploymentErrorType]
        ]

        konan_deployment_creation_response: KonanDeploymentCreationResponse = self.endpoint.process_response(
            KonanEndpointResponse(
                status_code=201,
                json={
                    'deployment': {
                        'uuid': self.deployment_uuid,
                        'name': deployment_name,
                        'created_at': created_at.isoformat(),
                    },
                    'errors': errors,
                    'container_logs': container_logs,
                },
            )
        )

        assert isinstance(konan_deployment_creation_response, KonanDeploymentCreationResponse)
        assert konan_deployment_creation_response.container_logs == container_logs

        assert konan_deployment_creation_response.deployment.created_at == created_at
        assert konan_deployment_creation_response.deployment.name == deployment_name
        assert konan_deployment_creation_response.deployment.uuid == self.deployment_uuid

        assert isinstance(konan_deployment_creation_response.errors, List)

        assert all([isinstance(error, KonanDeploymentError) for error in konan_deployment_creation_response.errors])
        assert len(konan_deployment_creation_response.errors) == len(expected_deployment_errors)
        assert set(konan_deployment_creation_response.errors) == set(expected_deployment_errors)
