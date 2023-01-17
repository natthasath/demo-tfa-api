from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi.responses import JSONResponse
from app.models.model_tfa import GenerateSchema, ReGenerateSchema, VerifyTotpSchema, VerifyHotpSchema
from app.services.service_tfa import TfaService

router = APIRouter(
    prefix="/tfa",
    tags=["TFA"],
    responses={404: {"message": "Not found"}}
)

@router.post("/totp/generate")
async def totp_generate(data: GenerateSchema = Depends(GenerateSchema)):
    return TfaService().totp_generate(data.email, data.qrcode)

@router.post("/totp/verify")
async def totp_verify(data: VerifyTotpSchema = Depends(VerifyTotpSchema)):
    return TfaService().totp_verify(data.secret, data.code)

@router.post("/hotp/generate")
async def hotp_generate(data: GenerateSchema = Depends(GenerateSchema)):
    return TfaService().hotp_generate(data.email, data.qrcode)

@router.post("/hotp/regenerate")
async def hotp_regenerate(data: ReGenerateSchema = Depends(ReGenerateSchema)):
    return TfaService().hotp_regenerate(data.secret, data.count)

@router.post("/hotp/verify")
async def hotp_verify(data: VerifyHotpSchema = Depends(VerifyHotpSchema)):
    return TfaService().hotp_verify(data.secret, data.code, data.count)

@router.post("/qrcode/scan")
async def qrcode_scan(file: UploadFile):
    return TfaService().qrcode_scan(file.file)