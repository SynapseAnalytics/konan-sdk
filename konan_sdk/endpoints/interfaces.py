class KonanEndpointRequest():
    def __init__(self, params=None, json=None):
        self.params = params
        self.json = json


class KonanEndpointResponse():
    def __init__(self, status_code=None, json=None) -> None:
        self.status_code = status_code
        self.json = json
