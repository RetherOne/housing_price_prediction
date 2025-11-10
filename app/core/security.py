import time

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

SECRET_KEY = "super_duper_secret_key"
ALGORITHM = "HS256"
TOKEN_EXPIRED = 120


def create_access_token():
    payload = {
        "sub": "test_data",
        "exp": time.time() + TOKEN_EXPIRED,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


class JWTBearer(HTTPBearer):
    def __call__(self, request: Request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing Bearer token")

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
