from typing import Callable, Type

from fastapi.types import DecoratedCallable
from fastapi_utils.inferring_router import InferringRouter

from konan_sdk.konan_service.serializers import (
    KonanServiceBasePredictionResponse, KonanServiceBaseEvaluateResponse)


class KonanServiceRouter(InferringRouter):
    def __init__(
        self,
        *,
        predict_response_class: Type = KonanServiceBasePredictionResponse,
        evaluate_response_class: Type = KonanServiceBaseEvaluateResponse,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._predict_response_class = predict_response_class
        self._evaluate_response_class = evaluate_response_class

    def healthz(
        self,
        **kwargs,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.get(
            '/healthz',
            **kwargs
        )

    def predict(
        self,
        **kwargs,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.post(
            '/predict',
            response_model=self._predict_response_class,
            **kwargs,
        )

    def evaluate(
        self,
        **kwargs,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.post(
            '/evaluate',
            response_model=self._evaluate_response_class,
            **kwargs,
        )
