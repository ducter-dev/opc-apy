from logging import exception
from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
import os
from os.path import join,dirname
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET = os.environ.get('SECRET')

def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

def write_token(data: dict):
    #token = encode(payload={**data, "exp":expire_date(2)}, key=SECRET, algorithm='HS256')
    token = encode(payload={**data}, key=SECRET, algorithm='HS256')
    return token

def validate_token(token, output=False):
    try:
        if output:
            return decode(token, SECRET, algorithms=['HS256'])
        decode(token, SECRET, algorithms=['HS256'])
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Token Invalido"}, status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expirado"}, status_code=401)