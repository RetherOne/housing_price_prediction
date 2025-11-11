import pandas as pd
from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import MODEL_PATH
from app.core.logger import logger
from app.core.security import JWTBearer, create_access_token
from app.schemas.param import Parameters
from app.utils.predict import load_model, predict

ALL_FEATURE = [
    "longitude",
    "latitude",
    "housing_median_age",
    "total_rooms",
    "total_bedrooms",
    "population",
    "households",
    "median_income",
    "ocean_proximity_<1H OCEAN",
    "ocean_proximity_INLAND",
    "ocean_proximity_ISLAND",
    "ocean_proximity_NEAR BAY",
    "ocean_proximity_NEAR OCEAN",
]

router = APIRouter()

model = load_model(MODEL_PATH)


def token_or_ip_key(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return get_remote_address(request)


limiter = Limiter(key_func=token_or_ip_key)


@router.post("/predict", dependencies=[Depends(JWTBearer())])
@limiter.limit("5/minute")
def fortune_teller(request: Request, params: Parameters | list[Parameters]):
    logger.info('Request received for "/predict"')
    if isinstance(params, Parameters):
        items = [params]
    else:
        items = params

    data = [item.model_dump() for item in items]
    df = pd.DataFrame(data)

    df = pd.get_dummies(df).reindex(columns=ALL_FEATURE, fill_value=0)

    y_pred = predict(df, model)
    logger.info("Prediction returned")
    return {"prediction": y_pred.tolist()}


@router.get("/get_token")
@limiter.limit("5/minute")
def get_token(request: Request):
    logger.info('Request received for "/get_token"')
    token = create_access_token()
    logger.info("Issued token")
    return {"access_token": token, "token_type": "bearer"}
