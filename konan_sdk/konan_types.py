import datetime
from enum import Enum
from typing import Dict, List, Union


class KonanCredentials():
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password


class KonanTokens():
    def __init__(self, access: str, refresh: str) -> None:
        self.access = access
        self.refresh = refresh


class KonanPrediction():
    def __init__(self, uuid: str, output: Dict) -> None:
        self.uuid = uuid
        self.output = output


class KonanDockerCredentials():
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


class KonanDockerImage():
    def __init__(self, url: str, exposed_port: int) -> None:
        self.url = url
        self.exposed_port = exposed_port


class KonanDeploymentCreationRequest():
    def __init__(
        self, name: str,
        docker_credentials: KonanDockerCredentials,
        docker_image: KonanDockerImage
    ) -> None:
        self.name = name
        self.docker_credentials = docker_credentials
        self.docker_image = docker_image


class KonanDeploymentErrorType(Enum):
    Image = 'image'
    HealthEndpoint = 'health_endpoint'
    ExposedPort = 'exposed_port'


class KonanDeploymentError():
    def __init__(self, type: KonanDeploymentErrorType, message: str) -> None:
        self.type = type
        self.message = message


class KonanDeployment():
    def __init__(
        self,
        uuid: str, name: str, created_at: datetime.datetime
    ) -> None:
        self.uuid = uuid
        self.name = name
        self.created_at = created_at


class KonanDeploymentCreationResponse():
    def __init__(
        self,
        deployment: KonanDeployment,
        errors: List[KonanDeploymentError], container_logs: str
    ) -> None:
        self.deployment = deployment
        self.errors = errors,
        self.container_logs = container_logs


class KonanTimeWindow():
    def __init__(
        self,
        start_time: datetime.datetime, end_time: datetime.datetime
    ) -> None:
        self.start_time = start_time
        self.end_time = end_time


class KonanFeedbackSubmission():
    def __init__(self, prediction_uuid: str, target: Union[Dict, str]) -> None:
        self.prediction_uuid = prediction_uuid
        self.target = target


class KonanFeedbackStatus():
    def __init__(self, prediction_uuid: str, status: int, message: str) -> None:
        self.prediction_uuid = prediction_uuid
        self.status = status
        self.message = message


class KonanFeedbacksResult():
    def __init__(
        self, feedbacks_status: List[KonanFeedbackStatus],
        success_count: int, failure_count: int, total_count: int
    ) -> None:
        self.feedbacks_status = feedbacks_status
        self.success_count = success_count
        self.failure_count = failure_count
        self.total_count = total_count
