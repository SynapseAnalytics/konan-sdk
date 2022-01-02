from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint, KonanBaseDeploymentEndpoint


class LoginEndpoint(KonanBaseEndpoint):
    @property
    def name(self) -> str:
        return 'login'

    @property
    def endpoint_path(self) -> str:
        return '/api/auth/login'


class RefreshTokenEndpoint(KonanBaseEndpoint):
    @property
    def name(self) -> str:
        return 'refresh_token'

    @property
    def endpoint_path(self) -> str:
        return '/api/auth/token/refresh'


class PredictionEndpoint(KonanBaseDeploymentEndpoint):
    @property
    def name(self) -> str:
        return 'predict'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/predict'

    def process_response(self):
        prediction_uuid = self.response.pop('prediction_uuid')
        self.response = prediction_uuid, self.response


class FeedbackEndpoint(KonanBaseDeploymentEndpoint):
    @property
    def name(self) -> str:
        return 'feedback'

    @property
    def endpoint_path(self) -> str:
        return super().endpoint_path + '/predictions/feedback'
