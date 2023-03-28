import requests
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime, timedelta
from ..schemas import FechaReportesRequestModel

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from ..middlewares import VerifyTokenRoute
router = APIRouter(prefix='/api/v1/reportes', route_class=VerifyTokenRoute)

JASPER_SERVER = os.environ.get('JASPER_SERVER')

s = requests.session()

def login():
    try:
        s.cookies.clear()
        url = f"{JASPER_SERVER}/login"
        payload = "j_username=jasperadmin&j_password=jasperadmin"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = s.request("POST", url, data=payload, headers=headers)
        heads = r.headers['Set-Cookie'].split('; ')
        cookieSession = heads[0].split(', ')
        cookieJSession = cookieSession[0].split("=")
        JSESSIONID = cookieJSession[1]
        return JSESSIONID
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )


@router.post('/cargas-diarias')
async def get_cargas_diarias_report(carga: FechaReportesRequestModel):
    try:
        cookie = login()
        url_cargas = f"{JASPER_SERVER}/reports/reportes/cargas/cargasDiarias.pdf?fecha={carga.fecha}"
        querystring = {"fecha":"2023-03-14"}
        payload= ""
        headers = {"cookie": f"userLocale=es_MX; JSESSIONID={cookie}"}
        response = requests.request("GET", url_cargas, data=payload, headers=headers, params=querystring)
        print(response)
        return 
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )