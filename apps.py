import dataclasses
import json
import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


@dataclasses.dataclass
class Config:
    api_key: str
    ckpt_path: str
    device: str
    variant: str


def load_config():
    config_path = "/tmp/config/config.json"
    with open(config_path) as f:
        data = json.load(f)
    return Config(**data)

config = load_config()
logger = logging.getLogger("uvicorn.app." + __name__)

app = FastAPI(
    title="Gemma API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

# CORS回避
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def authorize(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    logger.info("authorization: %s", authorization)
    if authorization.credentials != config.api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
