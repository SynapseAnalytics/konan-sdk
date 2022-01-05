from typing import Dict, Union


class FeedbackSubmission():
    def __init__(self, prediction_uuid: str, target: Union[Dict, str]) -> None:
        self.prediction_uuid = prediction_uuid
        self.target = target


class FeedbackStatus():
    def __init__(self, prediction_uuid: str, status: int, message: str) -> None:
        self.prediction_uuid = prediction_uuid
        self.status = status
        self.message = message
