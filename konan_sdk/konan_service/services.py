from typing import Type

from fastapi import FastAPI, Response
from fastapi_utils.cbv import cbv

from konan_sdk.konan_service.routers import KonanServiceRouter


class KonanService():
    """Class that implements a Konan webservice
    """
    def __init__(
        self,
        predict_request_class: Type,
        predict_response_class: Type,
        model_class: Type,
        *model_args, **model_kwargs,
    ) -> None:
        """Initializes a konan service

        Args:
            predict_request_class (Type): Type of a prediction request.
                Should be a class that inherits from KonanServiceBasePredictionRequest
            predict_response_class (Type): Type of a prediction response.
                Should be a class that inherits from KonanServiceBasePredictionResponse
            model_class (Type): Type of the model that does the prediction.
                Should be a class that inherits from KonanServiceBaseModel.
                Must implement the predict() method
        """
        self.model = model_class(*model_args, **model_kwargs)
        self.app = FastAPI(openapi_url='/docs', docs_url='/swagger')
        router = KonanServiceRouter(predict_response_class=predict_response_class)

        @cbv(router)
        class KonanRoutes():
            __model = self.model

            @router.healthz()
            def healthz(self) -> Response:
                return Response(
                    content="\n",
                    status_code=200, media_type="text/plain"
                )

            @router.predict()
            def predict(self, req: predict_request_class) -> predict_response_class:
                prediction = self.__model.predict(req)
                return prediction

        self.app.include_router(router)

    def __call__(self):
        return self.app
