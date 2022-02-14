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
    prediction: KonanServiceBasePredictionResponse  #: Past prediction output
    target: Any  #: Target value provided by the /feeback Konan API


class KonanServiceBaseEvaluateRequest(BaseModel):
    """
    Evaluate Request serializer for input format validation.
    """
    data: List[KonanServiceBaseFeedback]  #: List of past predictions along side their feedbacks


class KonanServicePredefinedMetricName(str, Enum):
    """
    Enum for Konan's predefined metrics.
    """
    multi_label_confusion_matrix = 'multi_label_confusion_matrix'  #: Multi label confusion matrix
    confusion_matrix = 'confusion_matrix'  #: Confusion Matrix
    precision = 'precision'  #: Precision
    recall = 'recall'  #: Recall
    f1_score = 'f1_score'  #: F1 Score
    rmse = 'rmse'  #: RMSE
    mae = 'mae'  #: MAE


class KonanServiceEvaluation(BaseModel):
    """
    A Konan Model's evaluation
    """
    metric_name: Union[KonanServicePredefinedMetricName, str]  #: Name of the metric
    metric_value: Any  #: Value of the metric

    class Config:
        use_enum_values = True


class KonanServiceBaseEvaluateResponse(BaseModel):
    """
    Evaluate Response serializer for output format validation.
    """
    results: List[KonanServiceEvaluation]  #: List of evaluations returned by the model
