from typing import Any, Dict


class KonanCredentials():
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password


class KonanTokens():
    def __init__(self, access: str, refresh: str) -> None:
        self.access = access
        self.refresh = refresh


class KonanPrediction():
    def __init__(self, uuid: str, output: Dict) -> None:
        self.uuid = uuid
        self.output = output
