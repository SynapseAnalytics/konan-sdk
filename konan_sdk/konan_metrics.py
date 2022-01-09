from abc import ABC, abstractmethod
from typing import Dict, Type, Any


class KonanBaseMetric(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        return ""

    def __init__(self, value: Any, **kwargs):
        self.value = value


class KonanRMSEMetric(KonanBaseMetric):
    @property
    def name(self) -> str:
        return "rmse"


class KonanMAEMetric(KonanBaseMetric):
    @property
    def name(self) -> str:
        return "mae"


class KonanPrecisionMetric(KonanBaseMetric):
    @property
    def name(self) -> str:
        return "precision"


class KonanRecallMetric(KonanBaseMetric):
    @property
    def name(self) -> str:
        return "recall"


class KonanF1ScoreMetric(KonanBaseMetric):
    @property
    def name(self) -> str:
        return "f1_score"


class KonanConfusionMatrixMetric(KonanBaseMetric):
    @property
    def name(self) -> str:
        return "confusion_matrix"


class KonanMultiLabelConfusionMatrixMetric(KonanBaseMetric):
    @property
    def name(self) -> str:
        return "multi_label_confusion_matrix"


class KonanCustomMetric(KonanBaseMetric):
    @property
    def name(self) -> str:
        return self.__metric_name

    def __init__(self, value: Any, name="undefined", **kwargs):
        super().__init__(value, kwargs)
        self.__metric_name = name


KONAN_PREDEFINED_METRICS: Dict[str, Type[KonanBaseMetric]] = {
    "rmse": KonanRMSEMetric, "mae": KonanMAEMetric,
    "precision": KonanPrecisionMetric, "recall": KonanRecallMetric,
    "f1_score": KonanF1ScoreMetric,
    "confusion_matrix": KonanConfusionMatrixMetric,
    "multi_label_confusion_matrix": KonanMultiLabelConfusionMatrixMetric
}
