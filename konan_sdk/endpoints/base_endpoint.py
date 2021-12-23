import json
from logging import log
import requests
from loguru import logger
from typing import Dict, Union


class KonanBaseEndpoint:
    def __init__(self, api_url:str, name:str, user) -> None:

        self.api_url = api_url
        self.name = name
        self.user = user

        self.request_url = ''
        self.headers = {}
        self.response = {}

    def prepare_request(self):
        pass

    def process_response(self):
        pass

    def post(self, payload: Union[Dict, str]):

        self.prepare_request()

        # If request content type is json, convert input dict to json string
        if self.headers and self.headers['Content-Type'] == 'application/json' and isinstance(payload, Dict):
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

        response.raise_for_status()

        self.response = response.json()

        self.process_response()

        return self.response


    def get(self, api_url: str):

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

