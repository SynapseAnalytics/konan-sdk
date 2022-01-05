import datetime
from typing import Any, Dict, List, Union
from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint, KonanBaseDeploymentEndpoint
from konan_sdk.endpoints.interfaces import KonanEndpointRequest, KonanEndpointResponse
from konan_sdk.konan_types.konan_metrics import KonanBaseMetric, KonanCustomMetric, PredefinedMetrics


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


class EvaluateEndpoint(KonanBaseDeploymentEndpoint):
    @property
    def name(self) -> str:
        return 'evaluate'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/evaluate'

    class RequestObject():
        def __init__(self, start_time: datetime.datetime, end_time: datetime.datetime) -> None:
            self.start_time = start_time
            self.end_time = end_time

    class ResponseObject():
        def __init___(self, metrics: List[KonanBaseMetric], error: str = None) -> None:
            self.metrics = metrics
            self.error = error

    def prepare_request(self, request_object: RequestObject) -> KonanEndpointRequest:
        return KonanEndpointRequest(data={
            'start_time': request_object.start_time.isoformat(),
            'end_time': request_object.end_time.isoformat()
        })

    def process_response(self, endpoint_response: KonanEndpointResponse) -> ResponseObject:
        predfined_metrics_dict = endpoint_response.json['metrics'].get("predefined", dict())
        custom_metrics_list = endpoint_response.json['metrics'].get("custom", list())

        metrics: List[KonanBaseMetric] = [
            PredefinedMetrics.get(metric_name, KonanCustomMetric)(predfined_metrics_dict[metric_name], name=metric_name)
            for metric_name in predfined_metrics_dict.keys()
        ] + [
            KonanCustomMetric(metric_dict["metric_value"], name=metric_dict["metric_name"])
            for metric_dict in custom_metrics_list
        ]

        return EvaluateEndpoint.ResponseObject(metrics, endpoint_response.json.get("error", None))
