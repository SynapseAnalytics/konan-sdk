
import json
import sys
from typing import Optional, Dict, Union, Tuple

import requests
from loguru import logger

from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint
from konan_sdk.endpoints.utils import get_predict_endpoint

class PredictionEndpoint(KonanBaseEndpoint):

    def __init__(self, api_url, user) -> None:
        super().__init__(name="predict", api_url=api_url, user=user)

    def post(self, deployment_uuid: str, input_data: Union[Dict, str]) -> Tuple[str, Dict]:

            api_url = get_predict_endpoint(api_url=self.api_url, deployment_uuid=deployment_uuid)

            data = super().post(api_url=api_url, payload=input_data)
            prediction_uuid = data.pop('prediction_uuid')

            return prediction_uuid, data['output']

