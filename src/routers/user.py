from functools import wraps
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasicCredentials, HTTPBearer
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Annotated, Callable, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ..schemas.user import UserAuthenticate, UserCreate
#from converters import UserConverter
from ..models import User

#import external_api as ext_api
#import utils

router = APIRouter(
    tags=["Users API"]
)

'''
@router.get("/profile")
async def profile(
    s: Annotated[UserService, Depends(UserService)],
    creds: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    user = s.get_current_user(token=creds.credentials)
    return JSONResponse(
        content=jsonable_encoder(UserConverter.to_schema(user)),
        status_code=200
    )
'''


