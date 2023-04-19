import requests
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from datetime import datetime, timedelta
from ..schemas import FechaReportesRequestModel
from ..database import BombaReporte, Bomba

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
    

@router.get('/cromatografo/{croma}/fecha/{fecha}')
async def get_patin_report(croma: int, fecha: str):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        cromaSt = getCromatografo(croma)
        url_croma = f"{JASPER_SERVER}/rest_v2/reports/reportes/cromatografo/{cromaSt}.pdf"
        params = {"fecha": fecha}
        
        res = s.get(url=url_croma, params=params, stream=True)
        res.raise_for_status()
        filename = f"{cromaSt}_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    


@router.get('/bombas/{fecha}')
async def get_patin_report(fecha: str):
    try:
        

        # Obtener los registros de las bombas filtrando por fecha
        registros = Bomba.select().where(Bomba.reporte24 == fecha)

        # escribir los registros en bombas_report
        oper_ba301a = ""
        mantto_ba301a = ""
        stat_ba301a = ""
        oper_ba301b = ""
        mantto_ba301b = ""
        stat_ba301b = ""
        oper_ba301c = ""
        mantto_ba301c = ""
        stat_ba301c = ""

        #   Borrar registros de reporte de Bombas
        BombaReporte.truncate_table()

        #   Rellenar resgistros en reporte de bombas
        for i in range(len(registros)):
            
            if (registros[i].bomba == 'BA-301A'):
                oper_ba301a = registros[i].totalTiempoOper
                mantto_ba301a = registros[i].enMantto
                stat_ba301a = registros[i].estatus
            elif (registros[i].bomba == 'BA-301B'):
                oper_ba301b = registros[i].totalTiempoOper
                mantto_ba301b = registros[i].enMantto
                stat_ba301b = registros[i].estatus
            elif (registros[i].bomba == 'BA-301C'):
                oper_ba301c = registros[i].totalTiempoOper
                mantto_ba301c = registros[i].enMantto
                stat_ba301c = registros[i].estatus
            
            if (((i + 1) % 3) == 0):
            
                row = BombaReporte.create(
                    hora = registros[i].hora,
                    oper_ba301a = oper_ba301a,
                    mantto_ba301a = mantto_ba301a,
                    stat_ba301a = stat_ba301a,
                    oper_ba301b = oper_ba301b,
                    mantto_ba301b = mantto_ba301b,
                    stat_ba301b = stat_ba301b,
                    oper_ba301c = oper_ba301c,
                    mantto_ba301c = mantto_ba301c,
                    stat_ba301c = stat_ba301c
                )
                row.save()
                oper_ba301a = ""
                mantto_ba301a = ""
                stat_ba301a = ""
                oper_ba301b = ""
                mantto_ba301b = ""
                stat_ba301b = ""
                oper_ba301c = ""
                mantto_ba301c = ""
                stat_ba301c = ""

        
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()

        url_bombas = f"{JASPER_SERVER}/rest_v2/reports/reportes/bombas/bombas.pdf"
        params = {"fecha": fecha}
        
        res = s.get(url=url_bombas, params=params, stream=True)
        res.raise_for_status()
        filename = f"Bombas_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)
        return FileResponse(path=path, filename=filename, media_type='application/pdf')
        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

def getCromatografo(croma):
    tabla_cromas = {
        1: 'cromatografoIrge',
        2: 'cromatografoC1',
        3: 'cromatografoC2',
        4: 'cromatografoC3',
    }
    
    return tabla_cromas.get(croma, 0 )