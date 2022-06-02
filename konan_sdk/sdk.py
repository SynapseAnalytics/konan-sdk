import datetime
import sys
from loguru import logger
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union
)

from konan_sdk.auth import KonanAuth
from konan_sdk.endpoints.konan_endpoints import (
    CreateDeploymentEndpoint,
    CreateModelEndpoint,
    DeleteDeployment,
    DeleteModelEndpoint,
    EvaluateEndpoint,
    FeedbackEndpoint,
    GetModelsEndpoint,
    PredictionEndpoint,
    SwitchLiveModelEndpoint,
    SwitchNonLiveModelEndpoint,
)
from konan_sdk.konan_metrics import KonanBaseMetric
from konan_sdk.konan_types import (
    KonanDeploymentCreationRequest,
    KonanDeploymentCreationResponse,
    KonanDockerCredentials,
    KonanDockerImage,
    KonanFeedbackSubmission,
    KonanFeedbacksResult,
    KonanLiveModelSwitchState,
    KonanModel,
    KonanModelCreationRequest,
    KonanModelState,
    KonanTimeWindow,
)
from konan_sdk.konan_utils.models import (
    find_live_model,
    find_model_state,
)


class KonanSDK:
    """konan-sdk's main class for API integration.
    """
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
        :type email: str
        :param password: password of registered user
        :type password: str
        """
        self.auth = KonanAuth(self.auth_url, email, password)
        self.auth.login()

    def create_deployment(
        self,
        name: str,
        docker_credentials: KonanDockerCredentials,
        docker_image: KonanDockerImage,
        model_name: str = None,
    ) -> KonanDeploymentCreationResponse:
        """Call the create deployment function

        :param name: name of the deployment to create
        :type name: str
        :param docker_credentials: credentials for the docker registry to use
        :type docker_credentials: KonanDockerCredentials
        :param docker_image: docker image information
        :type docker_image: KonanDockerImage
        :param model_name: name of the live model to create, defaults to None
        If left as None, will default to the name of the deployment
        :type model_name: str, optional
        :return: konan_deployment_creation_response
        :rtype: KonanDeploymentCreationResponse
        """
        # Default model_name to name of deployment if not passed
        model_name = model_name or name

        # check user performed login
        self.auth._post_login_checks()

        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        deployment_creation_response = CreateDeploymentEndpoint(
            self.api_url,
            user=self.auth.user
        ).request(
            KonanDeploymentCreationRequest(
                name,
                KonanModelCreationRequest(
                    model_name,
                    docker_credentials,
                    docker_image,
                )
            )
        )
        return deployment_creation_response

    def create_model(
        self,
        deployment_uuid: str,
        name: str,
        docker_credentials: KonanDockerCredentials,
        docker_image: KonanDockerImage,
    ) -> KonanModel:
        """Call the create model function

        :param deployment_uuid: uuid of the deployment to create the model in
        :type deployment_uuid: str
        :param name: name of the model to create
        :type name: str
        :param docker_credentials: credentials for the docker registry to use
        :type docker_credentials: KonanDockerCredentials
        :param docker_image: docker image information
        :type docker_image: KonanDockerImage
        :return: konan_model
        :rtype: KonanModel
        """
        # check user performed login
        self.auth._post_login_checks()

        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        konan_model = CreateModelEndpoint(
            self.api_url,
            user=self.auth.user,
            deployment_uuid=deployment_uuid,
        ).request(
            KonanModelCreationRequest(
                name,
                docker_credentials,
                docker_image,
            )
        )
        return konan_model

    def get_models(
        self,
        deployment_uuid: str,
    ) -> List[KonanModel]:
        """Call the get models function

        :param deployment_uuid: uuid of the deployment to get its models
        :type deployment_uuid: str
        :return: konan_models
        :rtype: List[KonanModel]
        """
        # check user performed login
        self.auth._post_login_checks()

        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        konan_models = GetModelsEndpoint(
            self.api_url,
            user=self.auth.user,
            deployment_uuid=deployment_uuid,
        ).request(None)

        return konan_models

    def _switch_nonlive_model(
        self,
        model_uuid: str,
        switch_to: KonanModelState,
    ) -> None:
        # check user performed login
        self.auth._post_login_checks()
        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        return SwitchNonLiveModelEndpoint(
            self.api_url,
            user=self.auth.user,
            model_uuid=model_uuid,
        ).request(
            switch_to,
        )

    def _switch_live_model(
        self,
        deployment_uuid: str,
        live_model_uuid: str,
        switch_to: KonanModelState,
        models: List[KonanModel],
        new_live_model_uuid: str = None,
    ) -> None:
        assert live_model_uuid, (
            f"Unable to find live model of deployment with uuid {deployment_uuid}",
        )
        assert new_live_model_uuid, (
            f"Attempting to demote live model with uuid {live_model_uuid}",
            " and no model to promote specified",
        )
        assert live_model_uuid != new_live_model_uuid, (
            f"Attempting to demote live model with uuid {live_model_uuid}",
            " and model to promote instead is the same",
        )
        # Get the state of the model to be promoted
        new_live_model_current_state = find_model_state(new_live_model_uuid, models)
        assert new_live_model_current_state, (
            f"Attempting to demote live model with uuid {live_model_uuid}",
            f" and model to promote instead with uuid {new_live_model_uuid}",
            " not found",
            f" within the models of deployment with uuid {deployment_uuid}",
        )
        # check user performed login
        self.auth._post_login_checks()
        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        return SwitchLiveModelEndpoint(
            self.api_url,
            user=self.auth.user,
            deployment_uuid=deployment_uuid,
        ).request(
            KonanLiveModelSwitchState(
                switch_to,
                new_live_model_uuid,
            ),
        )

    def switch_model_state(
        self,
        deployment_uuid: str,
        model_uuid: str,
        switch_to: KonanModelState,
        new_live_model_uuid: str = None,
    ) -> None:
        """Switch the sate of a Konan Model

        If model_uuid is the UUID of the current Live model then:
        - it will be demoted to Challenger, and
        - the parameter new_live_model_uuid is required

        :param deployment_uuid: UUID of deployment
        :type deployment_uuid: str
        :param model_uuid: UUID of model to switch
        :type model_uuid: str
        :param switch_to: new state to switch mode to. Must be different from the model's current state
        :type switch_to: KonanModelState
        :param new_live_model_uuid: _description_, defaults to None.
        Required only if model_uuid is the UUID of the current Live model
        :type new_live_model_uuid: str, optional
        :return: None
        :rtype: None
        """
        # Retrieve list of models linked with this deployment
        models = self.get_models(deployment_uuid)

        live_model_uuid = find_live_model(
            models=models,
        )
        model_state = find_model_state(model_uuid, models)

        assert model_state, (
            f"Model with uuid {model_uuid} not found",
            f" within the models of Deployment with uuid {deployment_uuid}",
        )
        assert model_state != switch_to, (
            f"Model with uuid {model_uuid} already at {switch_to} state",
        )
        if model_state == KonanModelState.Live:
            return self._switch_live_model(
                deployment_uuid=deployment_uuid,
                live_model_uuid=model_uuid,
                switch_to=switch_to,
                models=models,
                new_live_model_uuid=new_live_model_uuid,
            )
        elif switch_to == KonanModelState.Live:
            return self._switch_live_model(
                deployment_uuid=deployment_uuid,
                live_model_uuid=live_model_uuid,
                switch_to=KonanModelState.Challenger,
                models=models,
                new_live_model_uuid=model_uuid,
            )
        else:
            # check user performed login
            self.auth._post_login_checks()
            # Check if access token is valid and retrieve a new one if needed
            self.auth.auto_refresh_token()
            return SwitchNonLiveModelEndpoint(
                self.api_url,
                user=self.auth.user,
                model_uuid=model_uuid,
            ).request(
                switch_to,
            )

    def predict(
        self,
        deployment_uuid: str, input_data: Union[Dict, str]
    ) -> Tuple[str, Dict]:
        """Call the predict function for a given deployment

        :param deployment_uuid: uuid of deployment to use for prediction
        :type deployment_uuid: str
        :param input_data: data to pass to the model
        :type input_data: Union[Dict, str]
        :return: A tuple of prediction uuid and the prediction output
        :rtype: Tuple[str, Dict]
        """
        # check user performed login
        self.auth._post_login_checks()

        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        prediction = PredictionEndpoint(
            self.api_url,
            deployment_uuid=deployment_uuid, user=self.auth.user
        ).request(input_data)
        return prediction.uuid, prediction.output

    def evaluate(
        self, deployment_uuid: str,
        start_time: datetime.datetime, end_time: datetime.datetime
    ) -> List[KonanBaseMetric]:
        """Call the evaluate function for a given deployment

        :param deployment_uuid: uuid of deployment to use for evaluation
        :type deployment_uuid: str
        :param start_time: use predictions made at or after this time
        :type start_time: datetime.datetime
        :param end_time: use predictions made before or at this time
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
        ).request(KonanTimeWindow(start_time, end_time))

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
        ).request(feedbacks)
        return feedbacks_result

    def delete_model(
        self,
        model_uuid: str,
    ) -> bool:
        """Call the delete function for a given model
        WARNING: Using this method with a valid mode_uuid will DELETE it!!
        :param model_uuid: uuid of model to delete
        :type model_uuid: str
        :return: success
        :rtype: bool
        """
        # check user performed login
        self.auth._post_login_checks()

        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        delete_model_result = DeleteModelEndpoint(
            self.api_url,
            user=self.auth.user,
            model_uuid=model_uuid,
        ).request(None)
        return delete_model_result

    def delete_deployment(
        self,
        deployment_uuid: str,
    ) -> bool:
        """Call the delete function for a given deployment
        WARNING: Using this method with a valid deployment_uuid will DELETE it!!
        :param deployment_uuid: uuid of deployment to delete
        :type deployment_uuid: str
        :return: success
        :rtype: bool
        """

        # check user performed login
        self.auth._post_login_checks()

        # Check if access token is valid and retrieve a new one if needed
        self.auth.auto_refresh_token()

        delete_deployment_result = DeleteDeployment(
            self.api_url,
            deployment_uuid=deployment_uuid,
            user=self.auth.user
        ).request(None)
        return delete_deployment_result
