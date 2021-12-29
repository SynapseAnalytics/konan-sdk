from enum import Enum
from pydantic import BaseModel
from typing import Any, List, Union


class KonanServiceBasePredictionRequest(BaseModel):
    """
    Predict Request serializer for input format validation.
    """
    pass


class KonanServiceBasePredictionResponse(BaseModel):
    """
    Predict Response serializer for output format validation.
    """
    pass


class KonanServiceBaseFeedback(BaseModel):
    """
    Evaluation model for input format validation.
    """
    prediction: KonanServiceBasePredictionResponse
    target: Any


class KonanServiceBaseEvaluateRequest(BaseModel):
    """
    Evaluate Request serializer for input format validation.
    """
    data: List[KonanServiceBaseFeedback]


class KonanServicePredefinedMetricName(str, Enum):
    multi_label_confusion_matrix = 'multi_label_confusion_matrix'
    confusion_matrix = 'confusion_matrix'
    precision = 'precision'
    recall = 'recall'
    f1_score = 'f1_score'
    rmse = 'rmse'
    mae = 'mae'


class KonanServiceEvaluation(BaseModel):
    metric_name: Union[KonanServicePredefinedMetricName, str]
    metric_value: Any

    class Config:
        use_enum_values = True


class KonanServiceBaseEvaluateResponse(BaseModel):
    results: List[KonanServiceEvaluation]
