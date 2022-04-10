from abc import abstractmethod
import importlib.resources as pkg_resources
import json
from typing import Dict, Type
import yaml

from konan_sdk.endpoints.base_endpoint import (
    KonanBaseEndpoint,
    KonanEndpointOperationEnum,
)
from konan_sdk.konan_user import (
    KonanUser,
)


class EndpointCommonTests:
    @property
    @abstractmethod
    def _endpoint_class(self) -> Type[KonanBaseEndpoint]:
        return None

    def make_user(self):
        self.user = KonanUser(self.access_token, self.refresh_token)

    def make_endpoint(self):
        self.endpoint: KonanBaseEndpoint = self._endpoint_class(
            self.api_url,
            deployment_uuid=self.deployment_uuid,
            user=self.user,
        )

    def setup(self):
        self.api_url = 'https://api.dev.konan.ai'
        self.auth_url = 'https://auth.dev.konan.ai'

        placeholders: Dict = yaml.safe_load(
            pkg_resources.read_text(
                f'{__package__}.refs',
                'placeholders.yaml'
            )
        )
        if self._endpoint_class:
            ref = yaml.safe_load(
                pkg_resources.read_text(
                    f'{__package__}.refs.endpoints',
                    f'{self._endpoint_class.__name__}.yaml'
                )
            )
            ref_str = json.dumps(ref)
            for key, val in placeholders.items():
                ref_str = ref_str.replace(f'<{key}>', val)
            self.ref_endpoint = json.loads(ref_str)

        self.deployment_uuid = placeholders['deployment_uuid']
        self.access_token = placeholders['access_token']
        self.refresh_token = placeholders['refresh_token']
        self.prediction_uuid = placeholders['prediction_uuid']

        self.make_user()
        self.make_endpoint()

    def test_name(self):
        assert self.endpoint.name == self.ref_endpoint['name']

    def test_path(self):
        assert self.endpoint.endpoint_path == self.ref_endpoint['endpoint_path']

    def test_operation(self):
        assert self.endpoint.endpoint_operation == KonanEndpointOperationEnum[self.ref_endpoint['endpoint_operation']]

    def test_api_url(self):
        assert self.endpoint.api_url == self.api_url

    def test_request_url(self):
        assert self.endpoint.request_url == self.api_url + self.ref_endpoint['endpoint_path']

    def test_headers(self):
        assert self.endpoint.headers == self.ref_endpoint['headers']
