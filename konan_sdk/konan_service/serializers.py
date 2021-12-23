from pydantic import BaseModel


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
