import json
import os

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import generators
import schemas
from apps import app, authorize
import logging

logger = logging.getLogger("uvicorn.app." + __name__)

@app.post(
    "/api/create-content",
    response_model=schemas.Response,
)
async def create_content(
    body: schemas.Body,
    authorized: bool = Depends(authorize),
):
    logger.info("messages: %s", body)
    return {"content": generators.generate(body.messages)}
