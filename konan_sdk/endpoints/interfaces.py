class KonanEndpointRequest():
    def __init__(self, params=None, data=None):
        self.params = params
        self.data = data


class KonanEndpointResponse():
    def __init__(self, status_code=None, json=None) -> None:
        self.status_code = status_code
        self.json = json
