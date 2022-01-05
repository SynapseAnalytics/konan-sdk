from typing import Any, Dict, Union
from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint, KonanBaseDeploymentEndpoint
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse


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
