from abc import abstractmethod
import json
import requests
from loguru import logger
from typing import Dict, Union


class KonanBaseEndpoint:
    """
    Base Endpoint class for Konan endpoints to inherit.
    """

    name = '' # endpoint name to reference in logs
    def __init__(self, api_url:str, user) -> None:

        self.api_url = api_url
        self.user = user

        # request headers
        self.headers = {}
        # response object
        self.response = {}

    @property
    def request_url(self):
        return self.api_url + self.endpoint_path

    @property
    @abstractmethod
    def endpoint_path(self):
        # Override method to return path of specified endpoint
        pass

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
        response = requests.post(
            api_url,
            headers={
                'Authorization': f"Bearer {self.user.access_token}",
                'Content-Type': 'application/json',
            }
        )

        response.raise_for_status()

        logger.debug(f"Received response from {self.name}, parsing output")

        response.raise_for_status()

        self.response = response.json()

        self.process_response()

        return self.response

