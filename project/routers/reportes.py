import requests
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from datetime import datetime, timedelta
from ..schemas import FechaReportesRequestModel

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from ..middlewares import VerifyTokenRoute
router = APIRouter(prefix='/api/v1/reportes')

JASPER_SERVER = os.environ.get('JASPER_SERVER')

s = requests.session()

@router.get('/cargas-diarias/{fecha}')
async def get_cargas_diarias_report(fecha: str):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        url_cargas = f"{JASPER_SERVER}/rest_v2/reports/reportes/cargas/cargasDiarias.pdf"
        params = {"fecha": fecha}
        
        res = s.get(url=url_cargas, params=params, stream=True)
        res.raise_for_status()
        filename = f"cargas_diarias_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    


@router.get('/esferas/{esfera}/fecha/{fecha}')
async def get_esferas_report(esfera: str, fecha: str):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        url_esferas = f"{JASPER_SERVER}/rest_v2/reports/reportes/esferas/esfera_{esfera}.pdf"
        params = {"fecha": fecha}
        
        res = s.get(url=url_esferas, params=params, stream=True)
        res.raise_for_status()
        filename = f"esfera_{esfera}_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

@router.get('/patines/{patin}/fecha/{fecha}')
async def get_patin_report(patin: str, fecha: str):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        url_patin = f"{JASPER_SERVER}/rest_v2/reports/reportes/patines/Patin{patin}.pdf"
        params = {"fecha": fecha}
        
        res = s.get(url=url_patin, params=params, stream=True)
        res.raise_for_status()
        filename = f"Patin{patin}_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    
