from typing import List, Type

from fastapi import FastAPI, Response
from fastapi_utils.cbv import cbv

from konan_sdk.konan_service.routers import KonanServiceRouter
from konan_sdk.konan_service.serializers import (
    KonanServiceBaseFeedback, KonanServiceBaseEvaluateRequest, KonanServiceBaseEvaluateResponse
)


class KonanService():
    """Class that implements a Konan webservice
    """
    def __init__(
        self,
        predict_request_class: Type,
        predict_response_class: Type,
        model_class: Type,
        feedback_target_class: Type = None,
        evaluate_response_class: Type = KonanServiceBaseEvaluateResponse,
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
                Must implement the predict() and evaluate() methods
            feedback_target_class (Type, optional): Type of feedback target.
                Defaults to value of predict_response_class if None.
            evaluate_response_class (Type, optional): Type of an evaluation response.
                Should be a class that inherits from KonanServiceBaseEvaluateResponse.
                Defaults to KonanServiceBaseEvaluateResponse.
        """
        self.model = model_class(*model_args, **model_kwargs)
        self.app = FastAPI(openapi_url='/docs', docs_url='/swagger')
        feedback_target_class = feedback_target_class or predict_response_class

        class ServiceFeedback(KonanServiceBaseFeedback):
            prediction: predict_response_class
            target: feedback_target_class

        class ServiceEvaluateRequest(KonanServiceBaseEvaluateRequest):
            data: List[ServiceFeedback]

        router = KonanServiceRouter(
            predict_response_class=predict_response_class,
            evaluate_response_class=evaluate_response_class,
        )

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

            @router.evaluate()
            def evaluate(self, req: ServiceEvaluateRequest) -> evaluate_response_class:
                evaluation = self.__model.evaluate(req)
                return evaluation

        self.app.include_router(router)

    def __call__(self):
        return self.app
