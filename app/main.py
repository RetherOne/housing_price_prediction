from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.endpoints import limiter, router

app = FastAPI()
app.include_router(router)
app.state.limiter = limiter


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.exception_handler(429)
def rate_limit_handler(request: Request, exc):
    return JSONResponse(
        status_code=429, content={"detail": "Rate limit exceeded"}
    )
