
from functools import wraps
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasicCredentials, HTTPBearer
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Annotated, Callable, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ..schemas.user import UserAuthenticate, UserCreate
#from converters import UserConverter
from ..models import User

router = APIRouter(
    tags=["Telegram API"]
)