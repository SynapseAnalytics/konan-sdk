import abc

from konan_sdk.konan_service.serializers import (
    KonanServiceBasePredictionRequest, KonanServiceBasePredictionResponse,
    KonanServiceBaseEvaluateRequest, KonanServiceBaseEvaluateResponse,
)


class KonanServiceBaseModel(abc.ABC):
    @abc.abstractmethod
    def predict(self, req: KonanServiceBasePredictionRequest) -> KonanServiceBasePredictionResponse:
        """Predicts using the preprocessed_input

        :param req: raw request data from API
        :type req: KonanServiceBasePredictionRequest
        :return: This will be the response returned by the API.
        :rtype: KonanServiceBasePredictionResponse
        """
        pass

    @abc.abstractmethod
    def evaluate(self, req: KonanServiceBaseEvaluateRequest) -> KonanServiceBaseEvaluateResponse:
        """Evaluates the model using past predictions and their feedback

        :param req: raw request data from API
        :type req: KonanServiceBaseEvaluateRequest
        :return: This will be the response returned by the API
        :rtype: KonanServiceBaseEvaluateResponse
        """
        pass
