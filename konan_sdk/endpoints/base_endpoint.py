from enum import Enum
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


class KonanEndpointOperationEnum(Enum):
    GET = requests.get
    POST = requests.post
    DELETE = requests.delete


class KonanBaseEndpoint(Generic[ReqT, ResT]):
    """Base Endpoint class for Konan endpoints to inherit.

    :param ReqT: type of request_object to use in .get() and .post() methods
    :type ReqT: type
    :param ResT: type of object that .get() and .post() methods return
    :type ResT: type
    """

    def __init__(self, api_url: str, **kwargs) -> None:
        """Initializes a Konan base endpoint

        :param api_url: base URL of Konan API
        :type api_url: str
        """
        self.api_url = api_url

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns name of endpoint

        :return: endpoint name
        :rtype: str
        """
        return None

    @property
    @abstractmethod
    def endpoint_path(self) -> str:
        """Returns endpoint path, relative to self.api_url

        :return: endpoint path
        :rtype: str
        """
        return None

    @property
    @abstractmethod
    def endpoint_operation(self) -> KonanEndpointOperationEnum:
        """Returns the operation to use on the endpoint path

        :return: operation
        :rtype: KonanEndpointOperationEnum
        """
        return None

    @property
    def request_url(self) -> str:
        """Returns the full API URL

        :return: URL-formatted string for endpoint
        :rtype: str
        """
        return self.api_url + self.endpoint_path

    @property
    def headers(self) -> Optional[Dict]:
        """Returns request headers to use

        :return: request headers
        :rtype: Optional[Dict]
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

    def request(self, request_object: ReqT) -> ResT:
        """Base REST method for all Konan endpoints
        Depending on the endpoint's endpoint_operation, the corresponding
        method will be used

        :param request_object: endpoint request
        :type request_object: ReqT
        :return: endpoint response
        :rtype: ResT
        """
        endpoint_request = self.prepare_request(request_object)

        logger.debug(f"Sending {self.name} request")
        response: requests.Response = self.endpoint_operation(
            self.request_url, headers=self.headers,
            data=endpoint_request.data, params=endpoint_request.params
        )
        logger.debug(f"Received response from {self.name}, parsing output")

        response.raise_for_status()

        endpoint_response = KonanEndpointResponse(
            status_code=response.status_code, json=response.json()
        )
        response_object = self.process_response(endpoint_response)
        return response_object


class KonanBaseAuthenticatedEndpoint(KonanBaseEndpoint[ReqT, ResT]):
    """Base Endpoint class for Konan endpoints that require authentication.

    :param ReqT: type of request_object to use in .get() and .post() methods
    :type ReqT: type
    :param ResT: type of object that .get() and .post() methods return
    :type ResT: type
    """
    def __init__(self, api_url: str, user: KonanUser = None, **kwargs) -> None:
        """Initializes a Konan endpoint that requires authentication

        :param api_url: base URL of Konan API
        :type api_url: str
        :param user: user to authenticate as, defaults to None
        :type user: KonanUser, optional
        :raises ValueError: raises ValueError when user is not valid
        """
        super().__init__(api_url, **kwargs)
        if user is None:
            raise ValueError("A valid user must be specified")
        self.user = user

    @property
    def headers(self) -> Dict:
        """Returns request headers with an Authorization Token added

        :return: request headers
        :rtype: Dict
        """
        return {
            **(super().headers or dict()),
            **{
                'Authorization': f"Bearer {self.user.access_token}",
            }
        }


class KonanBaseGenericDeploymentsEndpoint(
    KonanBaseAuthenticatedEndpoint[ReqT, ResT]
):
    """Base Endpoint class for Konan endpoints that deal with deployments

    :param ReqT: type of request_object to use in .get() and .post() methods
    :type ReqT: type
    :param ResT: type of object that .get() and .post() methods return
    :type ResT: type
    """

    @property
    def endpoint_path(self) -> str:
        """Returns base generic deployments endpoint path,
        relative to self.api_url

        :return: endpoint path
        :rtype: str
        """
        return "/deployments"


class KonanBaseDeploymentEndpoint(
    KonanBaseGenericDeploymentsEndpoint[ReqT, ResT]
):
    """Base Endpoint class for Konan endpoints that deal with
    a specific deployment.

    :param ReqT: type of request_object to use in .get() and .post() methods
    :type ReqT: type
    :param ResT: type of object that .get() and .post() methods return
    :type ResT: type
    """
    def __init__(
        self, api_url: str,
        deployment_uuid: str = None, user: KonanUser = None, **kwargs
    ) -> None:
        """Initializes a Konan endpoint that deals with a deployment

        :param api_url: base URL of Konan API
        :type api_url: str
        :param deployment_uuid: deployment uuid to use, defaults to None
        :type deployment_uuid: str
        :param user: user to authenticate as, defaults to None
        :type user: KonanUser
        :raises ValueError: raises ValueError with invalid deployment_uuid
            and/or user args.
        """
        super().__init__(api_url, user=user, **kwargs)
        if deployment_uuid is None:
            raise ValueError("A valid deployment_uuid must be specified")
        self.deployment_uuid = deployment_uuid

    @property
    def endpoint_path(self) -> str:
        """Returns base deployment endpoint path, relative to self.api_url

        :return: endpoint path
        :rtype: str
        """
        return super().endpoint_path + f"/{self.deployment_uuid}"
