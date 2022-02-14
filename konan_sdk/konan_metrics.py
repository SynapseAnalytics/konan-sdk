from abc import ABC, abstractmethod
from typing import Dict, Type, Any


class KonanBaseMetric(ABC):
    """Base class for Konan*Metric classes.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the Konan*Metric.

        :return: Metric name
        :rtype: str
        """
        return ""

    def __init__(self, value: Any, **kwargs):
        """Initialize a new Konan*Metric object.

        :param value: Metric value
        :type value: Any
        """
        self.value = value


class KonanRMSEMetric(KonanBaseMetric):
    """Konan RMSE Metric.
    """
    @property
    def name(self) -> str:
        return "rmse"


class KonanMAEMetric(KonanBaseMetric):
    """Konan MAE Metric.
    """
    @property
    def name(self) -> str:
        return "mae"


class KonanPrecisionMetric(KonanBaseMetric):
    """Konan Precision Metric.
    """
    @property
    def name(self) -> str:
        return "precision"


class KonanRecallMetric(KonanBaseMetric):
    """Konan Recall Metric.
    """
    @property
    def name(self) -> str:
        return "recall"


class KonanF1ScoreMetric(KonanBaseMetric):
    """Konan F1 Score Metric.
    """
    @property
    def name(self) -> str:
        return "f1_score"


class KonanConfusionMatrixMetric(KonanBaseMetric):
    """Konan Confusion Matrix Metric.
    """
    @property
    def name(self) -> str:
        return "confusion_matrix"


class KonanMultiLabelConfusionMatrixMetric(KonanBaseMetric):
    """Konan Multi Label Confusion Matrix Metric.
    """
    @property
    def name(self) -> str:
        return "multi_label_confusion_matrix"


class KonanCustomMetric(KonanBaseMetric):
    """Konan Custom Metric.
    """
    @property
    def name(self) -> str:
        """Return the name of the Konan Custom Metric.

        :return: Custom Konan Metric name
        :rtype: str
        """
        return self.__metric_name

    def __init__(self, value: Any, name="undefined", **kwargs):
        """Initialize a new KonanCustomMetric

        :param value: Metric value
        :type value: Any
        :param name: Metric name, defaults to "undefined"
        :type name: str, optional
        """
        super().__init__(value, **kwargs)
        self.__metric_name = name


KONAN_PREDEFINED_METRICS: Dict[str, Type[KonanBaseMetric]] = {  #: Provides a list of all the Konan predefined metrics
    "rmse": KonanRMSEMetric, "mae": KonanMAEMetric,
    "precision": KonanPrecisionMetric, "recall": KonanRecallMetric,
    "f1_score": KonanF1ScoreMetric,
    "confusion_matrix": KonanConfusionMatrixMetric,
    "multi_label_confusion_matrix": KonanMultiLabelConfusionMatrixMetric
}
