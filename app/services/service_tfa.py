from decouple import config
from fastapi.responses import JSONResponse, StreamingResponse
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO
import qrcode
import pyotp

class TfaService:
    def __init__(self):
        self.tfa_totp = config("TFA_TOTP")
        self.tfa_hotp = config("TFA_HOTP")

    def totp_generate(self, username, qrcode):
        secret = pyotp.random_base32()
        if qrcode is True:
            uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=self.tfa_totp)
            data = self.qrcode_generate(uri)
        else:
            totp = pyotp.TOTP(secret)
            data = JSONResponse(status_code=200, content={"secret": secret, "code": totp.now()})
        return data

    def totp_verify(self, secret, code):
        totp = pyotp.TOTP(secret)
        message = totp.verify(code)
        return JSONResponse(status_code=200, content={"message": message})

    def hotp_generate(self, username, qrcode):
        secret = pyotp.random_base32()
        if qrcode is True:
            uri = pyotp.hotp.HOTP(secret).provisioning_uri(name=username, issuer_name=self.tfa_hotp, initial_count=0)
            data = self.qrcode_generate(uri)
        else:
            hotp = pyotp.HOTP(secret)
            data = JSONResponse(status_code=200, content={"secret": secret, "code": hotp.at(0), "count": 0})
        return data

    def hotp_regenerate(self, secret, count):
        hotp = pyotp.HOTP(secret)
        data = JSONResponse(status_code=200, content={"secret": secret, "code": hotp.at(count), "count": count})
        return data

    def hotp_verify(self, secret, code, count):
        hotp = pyotp.HOTP(secret)
        message = hotp.verify(code, count)
        return JSONResponse(status_code=200, content={"message": message})

    def qrcode_generate(self, uri):
        image = qrcode.make(uri)
        buffer = BytesIO()
        image.save(buffer, "PNG")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="image/png")

    def qrcode_scan(self, file):
        decocdeQR = decode(Image.open(file))
        uri = decocdeQR[0].data.decode('ascii')
        all_params = uri.split('?')[1]
        secret_paramse = all_params.split('&')[0]
        secret = secret_paramse.split('=')[1]
        return JSONResponse(status_code=200, content={"secret": secret})