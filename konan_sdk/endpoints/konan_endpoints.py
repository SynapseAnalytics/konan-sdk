from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint


class LoginEndpoint(KonanBaseEndpoint):
    name = 'login'

    def __init__(self, api_url, user) -> None:
        super().__init__(api_url=api_url, user=user)

    @property
    def endpoint_path(self):
        return  '/api/auth/login/'


class RefreshTokenEndpoint(KonanBaseEndpoint):
    name = 'refresh_token'

    def __init__(self, api_url, user) -> None:
        super().__init__(api_url=api_url, user=user)

    @property
    def endpoint_path(self):
        return  '/api/auth/token/refresh/'



class PredictionEndpoint(KonanBaseEndpoint):
    name = 'predict'

    def __init__(self, deployment_uuid, api_url, user) -> None:
        super().__init__(api_url=api_url, user=user)

        self.deployment_uuid = deployment_uuid
        self.headers = {
                'Authorization': f"Bearer {self.user.access_token}",
                'Content-Type': 'application/json',
            }

    @property
    def endpoint_path(self):
        return f"/deployments/{self.deployment_uuid}/predict/"


    def process_response(self):

        prediction_uuid = self.response.pop('prediction_uuid')
        self.response = prediction_uuid, self.response



