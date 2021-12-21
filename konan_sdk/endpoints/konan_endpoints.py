
import json
import sys
from typing import Optional, Dict, Union, Tuple

import requests
from loguru import logger

from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint
from konan_sdk.endpoints.utils import get_predict_endpoint



class PredictionEndpoint(KonanBaseEndpoint):

    def __init__(self, api_url, deployment_uuid, user) -> None:
        super().__init__(name="predict", api_url=api_url, user=user)
        self.deployment_uuid = deployment_uuid

    def prepare_request(self, *kwargs):
        self.request_url = get_predict_endpoint(api_url=self.api_url, deployment_uuid=self.deployment_uuid)


    def process_response(self, *kwargs):

        prediction_uuid = self.response.pop('prediction_uuid')
        self.response = prediction_uuid, self.response



