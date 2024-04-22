from pydantic import BaseModel , EmailStr
from datetime import datetime
from pydantic.types import conint

class PostBase(BaseModel):#used in validation of data.These feilds must be present when an API request is sent

    title:str
    content:str
    published: bool= True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:str
    created_at:datetime
    class Config:
        orm_mode=True


class Post(PostBase):
   
    id:int
    owner_id:int
    owner:UserOut
    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str



        
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str
    class Config:
        orm_mode=True

class TokenData(BaseModel):
    id:str=None

class Vote(BaseModel):
    post_id:int
    dir: conint(ge=0,le=1) # type: ignore

class PostOut(BaseModel):
    Post:Post
    votes:int

    class Config:
        orm_mode=True
    