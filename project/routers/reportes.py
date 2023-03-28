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
router = APIRouter(prefix='/api/v1/reportes', route_class=VerifyTokenRoute)

JASPER_SERVER = os.environ.get('JASPER_SERVER')

s = requests.session()

@router.post('/cargas-diarias')
async def get_cargas_diarias_report(carga: FechaReportesRequestModel):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        url_cargas = f"{JASPER_SERVER}/rest_v2/reports/reportes/cargas/cargasDiarias.pdf"
        params = {"fecha": carga.fecha}
        
        res = s.get(url=url_cargas, params=params, stream=True)
        res.raise_for_status()
        filename = f"cargas_diarias_{carga.fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )