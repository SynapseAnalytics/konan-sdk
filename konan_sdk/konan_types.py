import datetime
from enum import Enum
from typing import Dict, List, Union


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
    def __init__(self, uuid: str, output: Dict) -> None:
        """ Initialize a new KonanPrediction.

        :param uuid: Prediction uuid
        :type uuid: str
        :param output: Live model output
        :type output: Dict
        """
        self.uuid = uuid
        self.output = output


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


class KonanDeploymentCreationRequest():
    """Information required to issue a create a new Konan Deployment.
    """
    def __init__(
        self, name: str,
        docker_credentials: KonanDockerCredentials,
        docker_image: KonanDockerImage
    ) -> None:
        """ Initialize a new KonanDeploymentCreationRequest.

        :param name: Name of the new Konan Deployment.
        :type name: str
        :param docker_credentials: Credentials of the Docker Container Registry to use
        :type docker_credentials: KonanDockerCredentials
        :param docker_image: Docker Image to use as the Konan Model
        :type docker_image: KonanDockerImage
        """
        self.name = name
        self.docker_credentials = docker_credentials
        self.docker_image = docker_image


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


class KonanDeployment():
    """Konan Deployment.
    """
    def __init__(
        self,
        uuid: str, name: str, created_at: datetime.datetime
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
        errors: List[KonanDeploymentError], container_logs: str
    ) -> None:
        """ Initialize a new KonanDeploymentCreationResponse.

        :param deployment: Konan Deployment Created
        :type deployment: KonanDeployment
        :param errors: Errors encountered when attempting to create the new Konan Deployment
        :type errors: List[KonanDeploymentError]
        :param container_logs: Container logs genered when creating the new Konan Deployment
        :type container_logs: str
        """
        self.deployment = deployment
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
