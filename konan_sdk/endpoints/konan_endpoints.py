from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint


class LoginEndpoint(KonanBaseEndpoint):
    name = 'login'

    @property
    def endpoint_path(self):
        return '/api/auth/login/'

    @property
    def headers(self):
        return {}


class RefreshTokenEndpoint(KonanBaseEndpoint):
    name = 'refresh_token'

    @property
    def endpoint_path(self):
        return '/api/auth/token/refresh/'

    @property
    def headers(self):
        return {}


class PredictionEndpoint(KonanBaseEndpoint):
    name = 'predict'

    def __init__(self, api_url, user, deployment_uuid=None, **kwargs) -> None:

        if deployment_uuid is None:
            raise ValueError("A valid deployment_uuid must be specified")
        super().__init__(api_url=api_url, user=user)

        self.deployment_uuid = deployment_uuid

    @property
    def headers(self):
        return {
            'Authorization': f"Bearer {self.user.access_token}",
            'Content-Type': 'application/json',
        }

    @property
    def endpoint_path(self):
        return f"/deployments/{self.deployment_uuid}/predict/"

    def process_response(self):
        prediction_uuid = self.response.pop('prediction_uuid')
        self.response = prediction_uuid, self.response
