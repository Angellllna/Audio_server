from pydantic import BaseModel, Field, validator
import re

class TrackCreate(BaseModel):
    name: str = Field(..., min_length=5, max_length=50)

    @validator("name")
    def check_name_and_extension(cls, v):
        if not re.match(r"^.+\.(mp3|wav|ogg)$", v):
            raise ValueError("Назва треку повинна містити розширення .mp3, .wav або .ogg")
        return v


class TrackBase(BaseModel):
    title: str
    filename: str
    author_id: int

class TrackOut(TrackBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str



class PlaylistBase(BaseModel):
    name: str


class PlaylistOut(PlaylistBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True