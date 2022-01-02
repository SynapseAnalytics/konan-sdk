import json
import requests
from loguru import logger
from typing import Dict, Optional, Union
from abc import ABC, abstractmethod

from konan_sdk.konan_user import KonanUser


class KonanBaseEndpoint(ABC):
    """
    Base Endpoint class for Konan endpoints to inherit.
    """

    def __init__(self, api_url: str, **kwargs) -> None:
        """Initializes a Konan base endpoint

        Args:
            api_url (str): [description]
        """
        self.api_url = api_url
        self.response = None

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
        return None

    def prepare_request(self):
        # Override method with logic to implement before sending request
        pass

    def process_response(self):
        # Override method with logic to implement after receiving response
        pass

    def post(self, payload: Union[Dict, str]):
        """
        Base POST function for all post endpoints
        """
        self.prepare_request()

        # If request content type is json, convert input dict to json string
        if self.headers and dict(self.headers).get('Content-Type', '') == 'application/json' and isinstance(payload, Dict):
            payload = json.dumps(payload)

        logger.debug(f"Sending {self.name} request")

        # send request
        response = requests.post(
            self.request_url,
            headers=self.headers,
            data=payload
        )

        response.raise_for_status()

        logger.debug(f"Received response from {self.name}, parsing output")

        self.response = response.json()

        self.process_response()

        return self.response

    def get(self, api_url: str):
        """
        Base GET function for all get endpoints
        """
        self.prepare_request()

        logger.debug(f"Sending {self.name} request")

        # send request
        response = requests.get(
            api_url,
            headers=self.headers
        )

        response.raise_for_status()

        logger.debug(f"Received response from {self.name}, parsing output")

        self.response = response.json()

        self.process_response()

        return self.response


class KonanBaseAuthenticatedEndpoint(KonanBaseEndpoint):
    def __init__(self, api_url: str, user: KonanUser = None, **kwargs) -> None:
        super().__init__(api_url, user=user, **kwargs)
        if user is None:
            raise ValueError("A valid user must be specified")
        self.user = user

    @property
    def headers(self) -> Dict:
        return {
            'Authorization': f"Bearer {self.user.access_token}",
            'Content-Type': 'application/json',
        }


class KonanBaseDeploymentEndpoint(KonanBaseAuthenticatedEndpoint):
    def __init__(self, api_url: str, user: KonanUser = None, deployment_uuid: str = None, **kwargs) -> None:
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
