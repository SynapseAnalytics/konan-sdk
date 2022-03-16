from typing import List

from konan_sdk.konan_types import (
    KonanModel,
    KonanModelState,
)


def find_model_state(
    model_uuid: str,
    models: List[KonanModel],
) -> KonanModelState:
    """Find state of a model give its UUID

    :param model_uuid: UUID of model to return its state
    :type model_uuid: str
    :param models: List of Konan Models
    :type models: List[KonanModel]
    :return: model_state if Model with UUID model_uuid found in models
    Will return None otherwise
    :rtype: KonanModelState
    """
    for model in models:
        if model_uuid == model.uuid:
            return model.state
    return None


def find_live_model(
    models: List[KonanModel],
) -> str:
    """Return UUID of the live model given a List of KonanModels
    Will assume that only 1 Model is live

    :param models: List of Konan Models
    :type models: List[KonanModel]
    :return: live_model_uuid
    :rtype: str
    """
    for model in models:
        if model.state == KonanModelState.Live:
            return model.uuid
    return None
