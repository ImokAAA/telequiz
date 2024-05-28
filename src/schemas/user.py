from pydantic import BaseModel, EmailStr 


class UserBase(BaseModel):
    telegram_id: int


class UserAuthenticate(BaseModel):
    telegram_id: int
    

class UserCreate(UserBase):
    telegram_id: int


class UserScheme(UserBase):
    telegram_id: int
    role: str

    class Config:
        orm_mode = True