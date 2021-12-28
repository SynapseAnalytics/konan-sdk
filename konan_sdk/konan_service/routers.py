from typing import Callable, Type

from fastapi.types import DecoratedCallable
from fastapi_utils.inferring_router import InferringRouter

from konan_sdk.konan_service.serializers import (KonanServiceBasePredictionResponse)


class KonanServiceRouter(InferringRouter):
    def __init__(
        self,
        *,
        predict_response_class: Type = KonanServiceBasePredictionResponse,
        **kwargs,
    ) -> None:
        self._predict_response_class = predict_response_class
        super().__init__(**kwargs)

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
