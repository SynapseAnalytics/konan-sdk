import datetime
import sys
from loguru import logger
from typing import Dict, List, Optional, Tuple, Union

from konan_sdk.auth import KonanAuth
from konan_sdk.endpoints.konan_endpoints import (
    PredictionEndpoint,
    EvaluateEndpoint,
    FeedbackEndpoint,
)
from konan_sdk.konan_metrics import KonanBaseMetric
from konan_sdk.konan_types import (
    KonanFeedbackSubmission,
    KonanFeedbacksResult,
    KonanTimeWindow,
)


class KonanSDK:
    def __init__(
        self, auth_url="https://auth.konan.ai", api_url="https://api.konan.ai",
        verbose=False
    ):
        self.auth_url = auth_url
        self.api_url = api_url

        self.auth: Optional[KonanAuth] = None

        if not verbose:
            logger.remove()
            logger.add(sys.stderr, level="INFO")

    def login(self, email: str, password: str) -> None:
        """Login to Konan with user credentials

        :param email: email of registered user
        :param password: password of registered user
        """
        self.auth = KonanAuth(self.auth_url, email, password)
        self.auth.login()

    def predict(
        self,
        deployment_uuid: str, input_data: Union[Dict, str]
    ) -> Tuple[str, Dict]:
        """Call the predict function for a given deployment

        :param deployment_uuid: uuid of deployment to use for prediction
        :param input_data: data to pass to the model
        :return: A tuple of prediction uuid and the prediction output
        """
        # check user performed login
        self.auth._post_login_checks()

        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        prediction = PredictionEndpoint(
            self.api_url,
            deployment_uuid=deployment_uuid, user=self.auth.user
        ).post(input_data)
        return prediction.uuid, prediction.output

    def evaluate(
        self, deployment_uuid: str,
        start_time: datetime.datetime, end_time: datetime.datetime
    ) -> List[KonanBaseMetric]:
        """Call the evaluate function for a given deployment

        :param deployment_uuid: uuid of deployment to use for evaluation
        :type deployment_uuid: str
        :param start_time: use predictins made at or after this time
        :type start_time: datetime.datetime
        :param end_time: use predictins made before or at this time
        :type end_time: datetime.datetime
        :return: A model evaluation object
        :rtype: EvaluateEndpoint.ResponseObject
        """
        # check user performed login
        self.auth._post_login_checks()

        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        model_metrics = EvaluateEndpoint(
            self.api_url,
            deployment_uuid=deployment_uuid, user=self.auth.user
        ).post(KonanTimeWindow(start_time, end_time))

        return model_metrics

    def feedback(
        self, deployment_uuid: str,
        feedbacks: List[KonanFeedbackSubmission]
    ) -> KonanFeedbacksResult:
        """Call the feedback function for a given deployment

        :param deployment_uuid: uuid of deployment to use for prediction
        :type deployment_uuid: str
        :param feedbacks: feedback objects to register with the deployment
        :type feedbacks: List[KonanFeedbackSubmission]
        :return: feedback result
        :rtype: KonanFeedbacksResult
        """
        # check user performed login
        self.auth._post_login_checks()

        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        feedbacks_result = FeedbackEndpoint(
            self.api_url,
            deployment_uuid=deployment_uuid, user=self.auth.user
        ).post(feedbacks)
        return feedbacks_result
