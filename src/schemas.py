from pydantic import BaseModel, Field, ConfigDict


class TransactionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    amount: float = Field(gt=0, le=1_000_000)
    hour: int = Field(ge=0, le=23)

    distance_from_home_km: float = Field(ge=0)
    distance_from_last_transaction_km: float = Field(ge=0)
    ratio_to_median_purchase_price: float = Field(gt=0)

    used_chip: int = Field(ge=0, le=1)
    used_pin: int = Field(ge=0, le=1)
    online_order: int = Field(ge=0, le=1)

    def to_feature_dict(self):
        return self.model_dump()


class TransactionPrediction(BaseModel):
    fraud_prediction: int
    fraud_probability: float
    risk_level: str
    disclaimer: str


class BatchPredictionRequest(BaseModel):
    transactions: list[TransactionInput] = Field(
        min_length=1,
        max_length=500
    )


class BatchPredictionResponse(BaseModel):
    predictions: list[TransactionPrediction]