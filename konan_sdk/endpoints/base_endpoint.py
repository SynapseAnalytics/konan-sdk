import requests
from loguru import logger
from typing import Dict, Generic, Optional, TypeVar
from abc import abstractmethod

from konan_sdk.konan_user import KonanUser
from konan_sdk.endpoints.interfaces import (
    KonanEndpointRequest, KonanEndpointResponse
)

ReqT = TypeVar('ReqT')
ResT = TypeVar('ResT')


class KonanBaseEndpoint(Generic[ReqT, ResT]):
    """
    Base Endpoint class for Konan endpoints to inherit.
    """

    def __init__(self, api_url: str, **kwargs) -> None:
        """Initializes a Konan base endpoint

        Args:
            api_url (str): [description]
        """
        self.api_url = api_url

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns name of endpoint to use in logs

        Returns:
            str: name of endpoint
        """
        return None

    @property
    @abstractmethod
    def endpoint_path(self) -> str:
        """Returns endpoint path, relative to self.api_url

        Returns:
            str: endpoint path
        """
        return None

    @property
    def request_url(self) -> str:
        """Returns full URL for API request

        Returns:
            [str]: URL-formatted string for endpoint
        """
        return self.api_url + self.endpoint_path

    @property
    def headers(self) -> Optional[Dict]:
        """Returns request headers to use

        Returns:
            Optional[Dict]: request headers
        """
        return {
            'Content-Type': 'application/json',
        }

    @abstractmethod
    def prepare_request(self, request_object: ReqT) -> KonanEndpointRequest:
        # Override method with logic to implement before sending request
        return None

    @abstractmethod
    def process_response(self, endpoint_response: KonanEndpointResponse) -> ResT:
        # Override method with logic to implement after receiving response
        return None

    def post(self, request_object: ReqT) -> ResT:
        """
        Base POST method for all get endpoints
        """
        endpoint_request = self.prepare_request(request_object)

        logger.debug(f"Sending {self.name} request")
        response = requests.post(
            self.request_url, headers=self.headers,
            data=endpoint_request.data, params=endpoint_request.params)
        logger.debug(f"Received response from {self.name}, parsing output")

        response.raise_for_status()

        endpoint_response = KonanEndpointResponse(
            status_code=response.status_code, json=response.json()
        )
        response_object = self.process_response(endpoint_response)
        return response_object

    def get(self, request_object: ReqT) -> ResT:
        """
        Base GET method for all get endpoints
        """
        endpoint_request = self.prepare_request(request_object)

        logger.debug(f"Sending {self.name} request")
        response = requests.get(
            self.request_url, headers=self.headers,
            data=endpoint_request.data, params=endpoint_request.params)
        logger.debug(f"Received response from {self.name}, parsing output")

        response.raise_for_status()

        endpoint_response = KonanEndpointResponse(
            status_code=response.status_code, json=response.json()
        )
        response_object = self.process_response(endpoint_response)
        return response_object


class KonanBaseAuthenticatedEndpoint(KonanBaseEndpoint[ReqT, ResT]):
    def __init__(self, api_url: str, user: KonanUser = None, **kwargs) -> None:
        super().__init__(api_url, **kwargs)
        if user is None:
            raise ValueError("A valid user must be specified")
        self.user = user

    @property
    def headers(self) -> Dict:
        return {
            **(super().headers or dict()),
            **{
                'Authorization': f"Bearer {self.user.access_token}",
            }
        }


class KonanBaseDeploymentEndpoint(KonanBaseAuthenticatedEndpoint[ReqT, ResT]):
    def __init__(
        self, api_url: str,
        deployment_uuid: str = None, user: KonanUser = None, **kwargs
    ) -> None:
        super().__init__(api_url, user=user, **kwargs)
        if deployment_uuid is None:
            raise ValueError("A valid deployment_uuid must be specified")
        self.deployment_uuid = deployment_uuid

    @property
    def endpoint_path(self) -> str:
        """Returns endpoint path, relative to self.api_url

        Returns:
            str: endpoint path
        """
        return f"/deployments/{self.deployment_uuid}"
