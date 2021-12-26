from konan_sdk.endpoints.base_endpoint import KonanBaseEndpoint


class LoginEndpoint(KonanBaseEndpoint):
    def __init__(self, api_url, user) -> None:
        super().__init__(api_url=api_url, user=user)
        self.name = 'login'
        self.endpoint_path = '/api/auth/login/'


class RefreshTokenEndpoint(KonanBaseEndpoint):
    def __init__(self, api_url, user) -> None:
        super().__init__(api_url=api_url, user=user)
        self.name = 'refresh_token'
        self.endpoint_path = '/api/auth/token/refresh/'


class PredictionEndpoint(KonanBaseEndpoint):

    def __init__(self, deployment_uuid, api_url, user) -> None:
        super().__init__( api_url=api_url, user=user)

        self.name = 'predict'
        self.endpoint_path = f"/deployments/{deployment_uuid}/predict/"
        self.deployment_uuid = deployment_uuid
        self.headers = {
                'Authorization': f"Bearer {self.user.access_token}",
                'Content-Type': 'application/json',
            }


    def process_response(self):

        prediction_uuid = self.response.pop('prediction_uuid')
        self.response = prediction_uuid, self.response



