import datetime
from enum import Enum
from functools import total_ordering
from typing import Any, Dict, List, Optional, Union


class KonanCredentials():
    """Credentials to use to authenticate with the Konan API.
    """
    def __init__(self, email: str, password: str) -> None:
        """ Initialize a new KonanCredentials.

        :param email: email address
        :type email: str
        :param password: password
        :type password: str
        """
        self.email = email
        self.password = password


class KonanTokens():
    """API Token retrieved by successfully authenticating with the Konan API.
    """
    def __init__(self, access: str, refresh: str) -> None:
        """ Initialize a new KonanTokens.

        :param access: Konan access token
        :type access: str
        :param refresh: Konan refresh token
        :type refresh: str
        """
        self.access = access
        self.refresh = refresh


class KonanPrediction():
    """Successful prediction registered with the Konan API.
    """
    def __init__(
        self,
        uuid: str,
        output: Dict[str, Any],
        features: Optional[Dict[str, Any]] = None,
        feedback: Optional[Union[str, Dict[str, Any], Any]] = None,
    ) -> None:
        """ Initialize a new KonanPrediction.

        :param uuid: Prediction uuid
        :type uuid: str
        :param output: Live model output
        :type output: Dict
        :param features: features used to make the Prediction, defaults to None
        :type features: Optional[Dict[str, Any]], optional
        :param feedback: Feedback made on the Prediction, defaults to None
        :type feedback: Optional[Union[str, Dict[str, Any], Any]], optional
        """
        self.uuid = uuid
        self.output = output
        self.features = features
        self.feedback = feedback


class KonanDockerCredentials():
    """Credentials to use to authenticate with the Docker ContainerRegistry.
    """
    def __init__(self, username: str, password: str) -> None:
        """ Initialize a new KonanDockerCredentials.

        :param username: username
        :type username: str
        :param password: password
        :type password: str
        """
        self.username = username
        self.password = password


class KonanDockerImage():
    """Docker image to use for Konan Model creation.
    """
    def __init__(self, url: str, exposed_port: int) -> None:
        """ Initialize a new KonanDockerImage.

        :param url: URL of the docker image
        :type url: str
        :param exposed_port: Port number that hte docker image exposes its services at
        :type exposed_port: int
        """
        self.url = url
        self.exposed_port = exposed_port


class KonanModelState(Enum):
    """Different states a KonanModel can be in

    :param Enum: [description]
    :type Enum: [type]
    """
    Live = 'live'  #: Model Live State
    Challenger = 'challenger'  #: Model Challenger State
    Disabled = 'disabled'  #: Model Disabled State
    Other = "other"  #: Model Other State


class KonanModelCreationRequest():
    """Information required to create a new Konan Model.
    """
    def __init__(
        self,
        name: str,
        docker_credentials: Optional[KonanDockerCredentials],
        docker_image: KonanDockerImage,
        state: KonanModelState
    ) -> None:
        """Initialize a new KonanModelCreationRequest.

        :param name: Name of the new Konan Mode.
        :type name: str
        :param docker_credentials: Credentials of the Docker Container Registry to use
        :type docker_credentials: Optional[KonanDockerCredentials]
        :param docker_image: Docker Image to use as the Konan Model
        :type docker_image: KonanDockerImage
        """
        self.name = name
        self.docker_credentials = docker_credentials
        self.docker_image = docker_image
        self.state = state


class KonanProjectCreationRequest():
    """Information required to issue a create a new Konan Project.
    """
    def __init__(
        self,
        name: str,
        description: Optional[str],
    ) -> None:
        """ Initialize a new KonanProjectCreationRequest.

        :param name: Name of the new Konan Project.
        :type name: str
        :param description: Description of the new Konan Project.
        :type description: str
        """
        self.name = name
        self.description = description


class KonanDeploymentCreationRequest(KonanProjectCreationRequest):
    """Information required to issue a create a new Konan Deployment.
    """
    def __init__(
        self,
        name: str,
        description: Optional[str],
        model_creation_request: KonanModelCreationRequest,
    ) -> None:
        """ Initialize a new KonanDeploymentCreationRequest.

        :param name: Name of the new Konan Project.
        :type name: str
        :param description: Description of the new Konan Project.
        :type description: str
        :param model_creation_request: Information required to create a new Konan Model.
        :type model_creation_request: KonanModelCreationRequest
        """
        super().__init__(name=name, description=description)
        self.model_creation_request = model_creation_request


class KonanDeploymentErrorType(Enum):
    """Different error types possibly returned by the Konan API when attempting to create a new Konan Deployment.

    :param Enum: [description]
    :type Enum: [type]
    """
    Image = 'image'  #: Deployment Image Error
    HealthEndpoint = 'health_endpoint'  #: Healthz Error
    ExposedPort = 'exposed_port'  #: Exposed Port Error


class KonanDeploymentError():
    """Error returned by the Konan API when attempting to create a new Konan Deployment.
    """
    def __init__(self, type: KonanDeploymentErrorType, message: str) -> None:
        """ Initialize a new KonanDeploymentError.

        :param type: Type of the error encountered
        :type type: KonanDeploymentErrorType
        :param message: Message of the error encountered
        :type message: str
        """
        self.type = type
        self.message = message


class KonanLiveModelSwitchState():
    """Konan Live Model Switch State
    """
    def __init__(
        self,
        switch_to: KonanModelState,
        new_live_model_uuid: str,
    ) -> None:
        """Initialize a new KonanLiveModelSwitchState

        :param switch_to: state of model to switch to
        :type switch_to: KonanModelState
        :param new_live_model_uuid: UUID of the model to promote to live
        :type new_live_model_uuid: str
        """
        self.switch_to = switch_to
        self.new_live_model_uuid = new_live_model_uuid


@total_ordering
class KonanModel():
    """Konan Model
    """
    def __init__(
        self,
        uuid: str,
        name: str,
        created_at: datetime.datetime,
        state: KonanModelState,
    ) -> None:
        """Initialize a new KonanModel

        :param uuid: UUID of the Konan Mode
        :type uuid: str
        :param name: Name of the Konan Mode
        :type name: str
        :param created_at: Konan Model creation date and time
        :type created_at: datetime.datetime
        :param state: State of the Konan Model
        :type state: KonanModelState
        """
        self.uuid = uuid
        self.name = name
        self.created_at = created_at
        self.state = state

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, KonanModel):
            return False
        __other_model: KonanModel = __o
        return (
            self.uuid == __other_model.uuid
            and self.name == __other_model.name
            and self.created_at == __other_model.created_at
            and self.state == __other_model.state
        )

    def __lt__(self, __o: object) -> bool:
        assert isinstance(__o, KonanModel)
        __other_model: KonanModel = __o
        return self.uuid < __other_model.uuid


class KonanDeployment():
    """Konan Deployment.
    """
    def __init__(
        self,
        uuid: str,
        name: str,
        created_at: datetime.datetime,
    ) -> None:
        """ Initialize a new KonanDeployment.

        :param uuid: UUID of the Konan Deployment
        :type uuid: str
        :param name: Name of the Konan Deployment
        :type name: str
        :param created_at: Konan Deployment creation date and time
        :type created_at: datetime.datetime
        """
        self.uuid = uuid
        self.name = name
        self.created_at = created_at


class KonanDeploymentCreationResponse():
    """Information returned by the Konan API when attempting to create a new Konan Deployment.
    """
    def __init__(
        self,
        deployment: KonanDeployment,
        live_model: KonanModel,
        errors: List[KonanDeploymentError],
        container_logs: str,
    ) -> None:
        """ Initialize a new KonanDeploymentCreationResponse.

        :param deployment: Konan Deployment Created
        :type deployment: KonanDeployment
        :param errors: Errors encountered when attempting to create the new Konan Deployment
        :type errors: List[KonanDeploymentError]
        :param container_logs: Container logs generated when creating the new Konan Deployment
        :type container_logs: str
        """
        self.deployment = deployment
        self.live_model = live_model
        self.errors = errors,
        self.container_logs = container_logs


class KonanTimeWindow():
    """Konan Time Window of certain events.
    """
    def __init__(
        self,
        start_time: datetime.datetime, end_time: datetime.datetime
    ) -> None:
        """ Initialize a new KonanTimeWindow.

        :param start_time: Starting date and time of events to consider
        :type start_time: datetime.datetime
        :param end_time: Ending date and time of events to consider
        :type end_time: datetime.datetime
        """
        self.start_time = start_time
        self.end_time = end_time


class KonanFeedbackSubmission():
    """Konan Feedback to send to the Konan API.
    """
    def __init__(self, prediction_uuid: str, target: Union[Dict, str]) -> None:
        """ Initialize a new KonanFeedbackSubmission.

        :param prediction_uuid: Prediction UUID to provide the Feedback for
        :type prediction_uuid: str
        :param target: Ground Truth Target
        :type target: Union[Dict, str]
        """
        self.prediction_uuid = prediction_uuid
        self.target = target


class KonanFeedbackStatus():
    """Feedback Status returned by the Konan API.
    """
    def __init__(self, prediction_uuid: str, status: int, message: str) -> None:
        """ Initialize a new KonanFeedbackStatus.

        :param prediction_uuid: Prediction UUID
        :type prediction_uuid: str
        :param status: Feedback status integer
        :type status: int
        :param message: Feedback status message
        :type message: str
        """
        self.prediction_uuid = prediction_uuid
        self.status = status
        self.message = message


class KonanFeedbacksResult():
    """Bulk results of the Konan API when submitting Feedbacks.
    """
    def __init__(
        self, feedbacks_status: List[KonanFeedbackStatus],
        success_count: int, failure_count: int, total_count: int
    ) -> None:
        """ Initialize a new KonanFeedbacksResult.

        :param feedbacks_status: Status of all submitted Feedbacks
        :type feedbacks_status: List[KonanFeedbackStatus]
        :param success_count: Number of successfully created Feedbacks
        :type success_count: int
        :param failure_count: Number of failed Feedbacks to create
        :type failure_count: int
        :param total_count: Total number of Feedbacks submitted
        :type total_count: int
        """
        self.feedbacks_status = feedbacks_status
        self.success_count = success_count
        self.failure_count = failure_count
        self.total_count = total_count


class KonanRetrainingJobStatus(Enum):
    """Different states a KonanRetrainingJob can be in.

    :param Enum: [description]
    :type Enum: [type]
    """
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    Other = "other"


class KonanRetrainingJobCreationRequest:
    """Information required to create a new Konan RetrainingJob.
    """
    def __init__(
        self,
        predictions_start_time: Optional[datetime.datetime],
        predictions_end_time: Optional[datetime.datetime],
        append_training_data: Optional[bool],
        resulting_model_name: Optional[str],
        resulting_model_state: Optional[KonanModelState]
    ) -> None:
        """Initialize a new KonanRetrainingJobCreationRequest.

        :param predictions_start_time: The first day from which to consider predictions
        :type predictions_start_time: datetime.datetime
        :param predictions_end_time: The last day to which consider predictions
        :type predictions_end_time: datetime.datetime
        :param append_training_data: whether to include the model's TrainingData in the RetrainingJob
        :type append_training_data: bool
        :param resulting_model_name: the name of the model created as a result of the RetrainingJob
        :type resulting_model_name: str
        :param resulting_model_state: the state of the model created as a result of the RetrainingJob
        :type resulting_model_state: KonanModelState
        """
        self.predictions_start_time = predictions_start_time
        self.predictions_end_time = predictions_end_time
        self.append_training_data = append_training_data
        self.resulting_model_name = resulting_model_name
        self.resulting_model_state = resulting_model_state


class KonanRetrainingJob:
    """Konan RetrainingJob."""
    def __init__(
        self,
        uuid: str,
        created_at: datetime.datetime,
        resulting_model_name: str,
        resulting_model_state: KonanModelState,
        status: KonanRetrainingJobStatus,
        resulting_model: str = None,
        duration: float = None,
        started_at: datetime.datetime = None,
        ended_at: datetime.datetime = None,
        cancelled_at: datetime.datetime = None,
        metrics: str = None,
        test_percentage: float = None,
        train_percentage: float = None,
        eval_percentage: float = None,
    ) -> None:
        """Initialize a new KonanRetrainingJob.

        :param uuid: job UUID
        :type uuid: uuid.uuid4
        :param created_at: job creation date
        :type created_at: datetime.datetime
        :param resulting_model_name: name of the model to be created as result of this RetrainingJob
        :type resulting_model_name: str
        :param resulting_model_state: state of the model to be created as a result of this RetrainingJob
        :type resulting_model_state: KonanModelState
        :param status: job status
        :type status: KonanRetrainingJobStatus
        :param resulting_model: id of the created model as result of this RetrainingJob
        :type resulting_model: str
        :param duration: job duration
        :type duration: int
        :param started_at: job start date
        :type started_at: datetime.datetime
        :param ended_at: job end date
        :type ended_at: datetime.datetime
        :param cancelled_at: job cancellation date
        :type cancelled_at: datetime.datetime
        :param metrics: metrics data resulted from the RetrainingJob
        :type metrics: str
        :param test_percentage: percentage of test data
        :type test_percentage: float
        :param train_percentage: percentage of train data
        :type train_percentage: float
        :param eval_percentage: percentage of evaluation data
        :type eval_percentage: float
        """
        self.uuid = uuid
        self.created_at = created_at
        self.resulting_model_name = resulting_model_name
        self.resulting_model_state = resulting_model_state
        self.status = status
        self.resulting_model = resulting_model
        self.duration = duration
        self.started_at = started_at
        self.ended_at = ended_at
        self.cancelled_at = cancelled_at
        self.metrics = metrics
        self.test_percentage = test_percentage
        self.train_percentage = train_percentage
        self.eval_percentage = eval_percentage
