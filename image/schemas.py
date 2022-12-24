from enum import Enum

from pydantic import BaseModel, conint, constr
from fastapi import Form


class Size(str, Enum):
    S = '256×256'
    M = '512×512'
    L = '1024×1024'


class ResponseFormat(str, Enum):
    URL = 'url'
    B64_JSON = 'b64_json'


class BaseImageSchema(BaseModel):
    count: conint(gt=0, le=10) = 1
    size: Size = Size.S
    response_format: ResponseFormat = ResponseFormat.URL

    @classmethod
    def as_form(cls, count: int = Form(default=1, gt=0, le=10),
                size: Size = Form(default=Size.S),
                response_format: ResponseFormat = Form(default=ResponseFormat.URL)):
        return cls(count=count, size=size, response_format=response_format)


class CreateImageSchema(BaseImageSchema):
    prompt: constr(max_length=1000)


class ImageURLSchema(BaseModel):
    url: str


class ImageResponseSchema(BaseModel):
    data: list[ImageURLSchema] | dict
