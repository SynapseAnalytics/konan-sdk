import datetime
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
