from fastapi import Form
from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import List, Union
import inspect

def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(default = arg.default) if arg.default is not inspect._empty else Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

@form_body
class GenerateSchema(BaseModel):
    email: str = Field(...)
    qrcode: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "username@nida.ac.th",
                "qrcode": True
            }
        }

@form_body
class ReGenerateSchema(BaseModel):
    secret: str = Field(...)
    count: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "secret": "JBSWY3DPEHPK3PXP",
                "count": 1
            }
        }

@form_body
class VerifyTotpSchema(BaseModel):
    secret: str = Field(...)
    code: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "secret": "JBSWY3DPEHPK3PXP",
                "code": "123456"
            }
        }

@form_body
class VerifyHotpSchema(BaseModel):
    secret: str = Field(...)
    code: str = Field(...)
    count: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "secret": "JBSWY3DPEHPK3PXP",
                "code": "123456",
                "count": 0
            }
        }