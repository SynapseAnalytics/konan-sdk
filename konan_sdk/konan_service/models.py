import abc

from konan_sdk.konan_service.serializers import (
    KonanServiceBasePredictionRequest, KonanServiceBasePredictionResponse)


class KonanServiceBaseModel(abc.ABC):
    @abc.abstractmethod
    def predict(self, req: KonanServiceBasePredictionRequest) -> KonanServiceBasePredictionResponse:
        """Predicts using the preprocessed_input

        Args:
            req (PredictionRequestClass): raw request data from API

        Returns:
            PredictionResponseClass: prediction.
            This will be the response returned by the API.
        """
        pass
