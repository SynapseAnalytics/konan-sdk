from typing import Any, Dict, List, Union
from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint, KonanBaseDeploymentEndpoint
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse
from konan_sdk.konan_types.konan_feedback import FeedbackStatus, FeedbackSubmission


class LoginEndpoint(KonanBaseEndpoint):
    @property
    def name(self) -> str:
        return 'login'

    @property
    def endpoint_path(self) -> str:
        return '/api/auth/login'

    class RequestObject():
        def __init__(self, email: str, password: str) -> None:
            self.email = email
            self.passord = password

    class ResponseObject():
        def __init__(self, access_token: str, refresh_token: str) -> None:
            self.access_token = access_token
            self.refresh_token = refresh_token

    def prepare_request(self, request_object: RequestObject) -> KonanEndpointRequest:
        return KonanEndpointRequest(data={'email': request_object.email, 'password': request_object.passord})

    def process_response(self, endpoint_response: KonanEndpointResponse) -> ResponseObject:
        return LoginEndpoint.ResponseObject(access_token=endpoint_response.json['access'], refresh_token=endpoint_response.json['refresh'])


class RefreshTokenEndpoint(KonanBaseEndpoint):
    @property
    def name(self) -> str:
        return 'refresh_token'

    @property
    def endpoint_path(self) -> str:
        return '/api/auth/token/refresh'

    class RequestObject():
        def __init__(self, refresh_token: str) -> None:
            self.refresh_token = refresh_token

    class ResponseObject():
        def __init__(self, access_token: str) -> None:
            self.access_token = access_token

    def prepare_request(self, request_object: RequestObject) -> KonanEndpointRequest:
        return KonanEndpointRequest(data={'refresh': request_object.refresh_token})

    def process_response(self, endpoint_response: KonanEndpointResponse) -> ResponseObject:
        return RefreshTokenEndpoint.ResponseObject(access_token=endpoint_response.json['access'])


class PredictionEndpoint(KonanBaseDeploymentEndpoint):
    @property
    def name(self) -> str:
        return 'predict'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/predict'

    class RequestObject():
        def __init__(self, input_data: Union[Dict, str]) -> None:
            self.input_data = input_data

    class ResponseObject():
        def __init__(self, prediction_uuid: str, output: Any) -> None:
            self.prediction_uuid = prediction_uuid
            self.output = output

    def prepare_request(self, request_object: RequestObject) -> KonanEndpointRequest:
        return KonanEndpointRequest(data=request_object.input_data)

    def process_response(self, endpoint_response: KonanEndpointResponse) -> ResponseObject:
        return PredictionEndpoint.ResponseObject(prediction_uuid=endpoint_response.json['prediction_uuid'], output=endpoint_response.json['output'])


class FeedbackEndpoint(KonanBaseDeploymentEndpoint):
    @property
    def name(self) -> str:
        return 'feedback'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/predictions/feedback'

    class RequestObject():
        def __init__(self, feedbacks: List[FeedbackSubmission]) -> None:
            self.feedbacks = feedbacks

    class ResponseObject():
        def __init__(self, feedbacks_results: List[FeedbackStatus], failure_num: int, success_num: int, total_num: int) -> None:
            self.feedbacks_results = feedbacks_results
            self.failure_num = failure_num
            self.success_num = success_num
            self.total_num = total_num

    def prepare_request(self, request_object: RequestObject) -> KonanEndpointRequest:
        return KonanEndpointRequest(
            data={
                "feedback": [
                    {
                        "prediction_uuid": feedback.prediction_uuid,
                        "target": feedback.target,
                    } for feedback in request_object.feedbacks
                ]
            }
        )

    def process_response(self, endpoint_response: KonanEndpointResponse) -> ResponseObject:
        return FeedbackEndpoint.ResponseObject(
            [
                FeedbackStatus(
                    feedback_result['prediction_uuid'], feedback_result['status'], feedback_result['message']
                ) for feedback_result in endpoint_response.json["data"]
            ], endpoint_response.json["failure"], endpoint_response.json["success"], endpoint_response.json["total"]
        )
