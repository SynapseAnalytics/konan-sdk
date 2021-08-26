LOGIN_ENDPOINT = "/api/auth/login/"
TOKEN_REFRESH_ENDPOINT = "/api/auth/token/refresh/"


def get_predict_endpoint(api_url, project_uuid: str) -> str:
    return api_url + f"/mlservices/{project_uuid}/predict/"
