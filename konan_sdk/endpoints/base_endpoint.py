


# base class, checks login, refreh token, get and post
# class for each endpoint, inherits from base class, has hit endpoint, hit endpoint calls super to include hit from base class
# konan sdk wrapper for endpoint classes, instantiate endpoint classes and calls them
# store parameters in self instead of passing as args
import json
from logging import log
import requests
from loguru import logger
from typing import Dict


class KonanBaseEndpoint:
    def __init__(self, api_url, name, user) -> None:

        self.api_url = api_url
        self.name = name
        self.user = user

        self.request_url = ''
        self.response = {}

    def prepare_request(self, *kwargs):
        pass

    def process_response(self, *kwargs):
        pass

    def post(self, payload):

        self.prepare_request()

        # Convert input to json string if it's a dict
        if isinstance(payload, Dict):
            payload = json.dumps(payload)

        logger.debug(f"Sending {self.name} request")

        # send request
        response = requests.post(
            self.request_url,
            headers={
                'Authorization': f"Bearer {self.user.access_token}",
                'Content-Type': 'application/json',
            },
            data=payload
        )

        response.raise_for_status()

        logger.debug(f"Received response from {self.name}, parsing output")

        response.raise_for_status()

        self.response = response.json()

        self.process_response()

        return self.response



    def get(self, api_url):

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

