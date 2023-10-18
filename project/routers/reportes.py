import requests
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from datetime import datetime, timedelta, date
from ..schemas import FechaReportesRequestModel
from ..database import BombaReporte, Bomba, PatinData, TankInTrucks, Esfera, BalanceDiario, Patin, ReportePatin, BalanceMensual, ReporteEsferas
import peewee
from peewee import *
from peewee import fn
from ..funciones import obtenerDiaAnterior, obtenerUltimoDiaMes, obtenerUltimoDiaMesOrAhora, obtenerDiaPosterior
from ..logs import LogsServices

import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from ..middlewares import VerifyTokenRoute
router = APIRouter(prefix='/api/v1/reportes')

JASPER_SERVER = os.environ.get('JASPER_SERVER')

s = requests.session()

@router.get('/cargas-diarias/{fecha}/tipo/{tipo}')
async def get_cargas_diarias_report(fecha: str, tipo: int):
    try:
        # buffer = io.BytesIO()
        
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_cargas = f"{JASPER_SERVER}/rest_v2/reports/reportes/cargas/cargasDiarias{tipoRep}.pdf"
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
    

@router.get('/ultimas-cargas/{fecha}/tipo/{tipo}')
async def get_ultimas_cargas_report(fecha: str, tipo: int):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_cargas = f"{JASPER_SERVER}/rest_v2/reports/reportes/cargas/ultimasCargas{tipoRep}.pdf"
        params = {"fecha": fecha}
        
        res = s.get(url=url_cargas, params=params, stream=True)
        res.raise_for_status()
        filename = f"ultimas_cargas_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )


@router.get('/lista-llegada/{fecha}/tipo/{tipo}')
async def get_lista_llegada_report(fecha: str, tipo: int):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_listaLlegada = f"{JASPER_SERVER}/rest_v2/reports/reportes/cargas/lista_llegada{tipoRep}.pdf"
        params = {"fecha": fecha}
        
        res = s.get(url=url_listaLlegada, params=params, stream=True)
        res.raise_for_status()
        filename = f"lista_llegada_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )


@router.get('/despacho-diario/{fecha}/tipo/{tipo}')
async def get_despacho_diario_report(fecha: str, tipo: int):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_despachoDiario = f"{JASPER_SERVER}/rest_v2/reports/reportes/cargas/despachoDiario{tipoRep}.pdf"
        params = {"fecha": fecha}
        
        res = s.get(url=url_despachoDiario, params=params, stream=True)
        res.raise_for_status()
        filename = f"despacho_diario{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

@router.get('/esferas/{esfera}/fecha/{fecha}/tipo/{tipo}')
async def get_esferas_report(esfera: str, fecha: str, tipo: int):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_esferas = f"{JASPER_SERVER}/rest_v2/reports/reportes/esferas/esfera_{esfera}{tipoRep}.pdf"
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
    

@router.get('/patines/{patin}/fecha/{fecha}/tipo/{tipo}')
async def get_patin_report(patin: str, fecha: str, tipo: int):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_report = f"{JASPER_SERVER}/rest_v2/reports/reportes/patines/Patin{patin}{tipoRep}.pdf"
        
        url_patin = url_report
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
    

@router.get('/cromatografo/{croma}/fecha/{fecha}/tipo/{tipo}')
async def get_patin_report(croma: int, fecha: str, tipo: int):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        cromaSt = getCromatografo(croma)
        tipoRep = '_24' if tipo == 24 else ''
        url_croma = f"{JASPER_SERVER}/rest_v2/reports/reportes/cromatografo/{cromaSt}{tipoRep}.pdf"
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
    

@router.get('/bombas/{fecha}/tipo/{tipo}')
async def get_bombas_report(fecha: str, tipo: int):
    try:
        
        # Obtener los registros de las bombas filtrando por fecha
        if tipo == 5:
            registros = Bomba.select().where(Bomba.reporte05 == fecha)
            
        else:
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
        params = {
            "fecha": fecha,
            "tipo": tipo
        }
        
        res = s.get(url=url_bombas, params=params, stream=True)
        res.raise_for_status()
        filename = f"Bombas_{fecha}_{tipo}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)
        return FileResponse(path=path, filename=filename, media_type='application/pdf')
        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

@router.get('/llenaderas/{llenadera}/fecha/{fecha}/tipo/{tipo}')
async def get_llenaderas_report(llenadera: str, fecha: str,  tipo: int):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_esferas = f"{JASPER_SERVER}/rest_v2/reports/reportes/cargas/llenaderas{tipoRep}.pdf"
        params = {
            "llenadera": llenadera,
            "fecha": fecha
        }
        
        res = s.get(url=url_esferas, params=params, stream=True)
        res.raise_for_status()
        filename = f"llenadera_{llenadera}_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

@router.get('/esferas/fecha/{fecha}/tipo/{tipo}')
async def get_esferas_inventario_report(fecha: str,  tipo: int):
    try:
        #   rellenar tabla
        fechaAnt = obtenerDiaAnterior(fecha)
        if (tipo == 5):
            # obtener el primer dato del día
            primerRegA = Esfera.select().where(Esfera.esfera == 1).where(Esfera.reporte05 == fechaAnt).order_by(Esfera.id.desc()).first()
            ultimoRegA = Esfera.select().where(Esfera.esfera == 1).where(Esfera.reporte05 == fecha).order_by(Esfera.id.desc()).first()
            # ultimo dato de hoy
            primerRegB = Esfera.select().where(Esfera.esfera == 2).where(Esfera.reporte05 == fechaAnt).order_by(Esfera.id.desc()).first()
            ultimoRegB = Esfera.select().where(Esfera.esfera == 2).where(Esfera.reporte05 == fecha).order_by(Esfera.id.desc()).first()
        else:
            # obtener el primer dato del día
            primerRegA = Esfera.select().where(Esfera.esfera == 1).where(Esfera.reporte24 == fechaAnt).order_by(Esfera.id.desc()).first()
            ultimoRegA = Esfera.select().where(Esfera.esfera == 1).where(Esfera.reporte05 == fecha).order_by(Esfera.id.desc()).first()
            # ultimo dato de hoy
            primerRegB = Esfera.select().where(Esfera.esfera == 2).where(Esfera.reporte24 == fechaAnt).order_by(Esfera.id.desc()).first()
            ultimoRegB = Esfera.select().where(Esfera.esfera == 2).where(Esfera.reporte05 == fecha).order_by(Esfera.id.desc()).first()
        

        # Hacemos las sumas y las restas
        inicialBls_a = primerRegA.volumenBlsNat
        inicialBls20_a = primerRegA.volumenBlsCor
        inicialTons_a = primerRegA.volumenTon
        actualBls_a = ultimoRegA.volumenBlsNat
        actualBls20_a = ultimoRegA.volumenBlsCor
        actualTons_a = ultimoRegA.volumenTon
        diferenciaBls_a = actualBls_a - inicialBls_a
        diferenciaBls20_a = actualBls20_a - inicialBls20_a
        diferenciaTons_a = actualTons_a - inicialTons_a

        inicialBls_b = primerRegB.volumenBlsNat
        inicialBls20_b = primerRegB.volumenBlsCor
        inicialTons_b = primerRegB.volumenTon 
        actualBls_b = ultimoRegB.volumenBlsNat
        actualBls20_b = ultimoRegB.volumenBlsCor
        actualTons_b = ultimoRegB.volumenTon
        diferenciaBls_b = actualBls_b - inicialBls_b
        diferenciaBls20_b = actualBls20_b - inicialBls20_b
        diferenciaTons_b = actualTons_b - inicialTons_b
        
        
        # guardamos los registros en la bd
        registroEsfera1 = ReporteEsferas.select().where(ReporteEsferas.id == 1).first()
        registroEsfera2 = ReporteEsferas.select().where(ReporteEsferas.id == 2).first()

        registroEsfera1.esfera = 'TE-301A'
        registroEsfera1.inicialBls = inicialBls_a
        registroEsfera1.inicialBls20 = inicialBls20_a
        registroEsfera1.inicialTons = inicialTons_a
        registroEsfera1.actualBls = actualBls_a
        registroEsfera1.actualBls20 = actualBls20_a
        registroEsfera1.actualTons = actualTons_a
        registroEsfera1.diferenciaBls = diferenciaBls_a
        registroEsfera1.diferenciaBls20 = diferenciaBls20_a
        registroEsfera1.diferenciaTons = diferenciaTons_a
        registroEsfera1.save()
    
        registroEsfera2.esfera = 'TE-301B'
        registroEsfera2.inicialBls = inicialBls_b
        registroEsfera2.inicialBls20 = inicialBls20_b
        registroEsfera2.inicialTons = inicialTons_b
        registroEsfera2.actualBls = actualBls_b
        registroEsfera2.actualBls20 = actualBls20_b
        registroEsfera2.actualTons = actualTons_b
        registroEsfera2.diferenciaBls = diferenciaBls_b
        registroEsfera2.diferenciaBls20 = diferenciaBls20_b
        registroEsfera2.diferenciaTons = diferenciaTons_b
        registroEsfera2.save()
        

        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_esferas = f"{JASPER_SERVER}/rest_v2/reports/reportes/esferas/esferas{tipoRep}.pdf"
        params = {
            "fecha": fecha
        }
        
        res = s.get(url=url_esferas, params=params, stream=True)
        res.raise_for_status()
        filename = f"esferas_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )


@router.get('/bitacora/{fecha}/tipo/{tipo}')
async def get_bitacora_report(fecha: str,  tipo: int):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_bitacora = f"{JASPER_SERVER}/rest_v2/reports/reportes/bitacora/bitacora{tipoRep}.pdf"
        params = {
            "fecha": fecha
        }
        
        res = s.get(url=url_bitacora, params=params, stream=True)
        res.raise_for_status()
        filename = f"bitacora{tipoRep}_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

@router.get('/balance-diario/{fecha}/tipo/{tipo}')
async def get_balance_diario_report(fecha: str, tipo: int):
    try:
        # Función para llenar la tabla de balance diario 
        # 1. Obtener los registro iniciales de las 0, 8, y 16
        # 2. Obtener los registro finales de las 8, 16 y 24 hrs
        fechaAnt = obtenerDiaAnterior(fecha)
    
        strTurno1 = '00-08' if tipo == 24 else '05-13'
        strTurno2 = '08-16' if tipo == 24 else '13-21'
        strTurno3 = '16-24' if tipo == 24 else '21-05'

        strTurnos = [strTurno1, strTurno2, strTurno3]
        
        turnos = [1,2,3]
        if tipo == 5:
            dataPatines = PatinData.select().where(PatinData.reporte05 == fecha)
            dataSalidas = TankInTrucks.select().where(TankInTrucks.reporte05 == fecha)
            
        else:
            dataPatines = PatinData.select().where(PatinData.reporte24 == fecha)
            dataSalidas = TankInTrucks.select().where(TankInTrucks.reporte24 == fecha)


        dataReporte = []
        dictTotales = {}
        # Variables para llenar el reporte

        inicial_nat = 0
        inicial_cor = 0
        inicial_tons = 0
        recibo_nat = 0
        recibo_cor = 0
        recibo_tons = 0
        ventas_nat = 0
        ventas_cor = 0
        ventas_tons = 0
        ventas_pgs = 0
        final_nat = 0
        final_cor = 0
        final_tons = 0

        # Ciclo para obtener la data por turnos
        for turno in turnos:
            dictTurno = {}
            if tipo == 5:
                # Filtrando la data de patines
                filtered_arr = [p for p in dataPatines if p.turno05 == turno]
                dictTurno['turno'] = turno
                blsNat_turno_rec = 0
                blsCor_turno_rec = 0
                tons_turno_rec = 0
                blsNat_turno_venta = 0
                blsCor_turno_venta = 0
                tons_turno_venta = 0
                if len(filtered_arr) > 0:
                    for fa in filtered_arr:
                        blsNat_turno_rec = blsNat_turno_rec + fa.volUnc
                        blsCor_turno_rec = blsCor_turno_rec + fa.blsCor
                        tons_turno_rec = tons_turno_rec + fa.ton
                        recibo_nat = recibo_nat + fa.volUnc
                        recibo_cor = recibo_cor + fa.blsCor
                        recibo_tons = recibo_tons + fa.ton

                    dictTurno['recibo_nat'] = blsNat_turno_rec
                    dictTurno['recibo_cor'] = blsCor_turno_rec
                    dictTurno['recibo_tons'] = tons_turno_rec
                else:
                    dictTurno['recibo_nat'] = 0
                    dictTurno['recibo_cor'] = 0
                    dictTurno['recibo_tons'] = 0
                

                # Filtrando la data de salidas
                filter_salidas = [s for s in dataSalidas if s.turno05 == turno]
                if len(filter_salidas) > 0:
                    for fs in filter_salidas:
                        blsNat_turno_venta = blsNat_turno_venta + fs.volNatBls
                        blsCor_turno_venta = blsCor_turno_venta + fs.volCorBls
                        tons_turno_venta = tons_turno_venta + fs.masaTons
                        ventas_nat = ventas_nat + fs.volNatBls
                        ventas_cor = ventas_cor + fs.volCorBls
                        ventas_tons = ventas_tons + fs.masaTons
                    dictTurno['ventas_nat'] = blsNat_turno_venta
                    dictTurno['ventas_cor'] = blsCor_turno_venta
                    dictTurno['ventas_tons'] = tons_turno_venta
                    dictTurno['ventas_pgs'] = len(filter_salidas)
                    ventas_pgs = ventas_pgs + len(filter_salidas)
                else:
                    dictTurno['ventas_nat'] = 0
                    dictTurno['ventas_cor'] = 0
                    dictTurno['ventas_tons'] = 0
                    dictTurno['ventas_pgs'] = 0

                # Leer data de inventarios de esferas inicio
                esferas = [1,2]
                
                tot_volNat_esfera_ini = 0
                tot_volCor_esfera_ini = 0
                tot_tons_esfera_ini = 0
                tot_volNat_esfera_fin = 0
                tot_volCor_esfera_fin = 0
                tot_tons_esfera_fin = 0

                for j in esferas:
                    if turno == 1:
                        dataEsferaInicio = Esfera.select().where(Esfera.reporte05 == fechaAnt, Esfera.esfera == j).order_by(Esfera.id.desc()).first()
                        dictTurno['turno'] = strTurnos[turno - 1]

                        if dataEsferaInicio is None:
                            dictTurno['inicial_nat'] = 0
                            dictTurno['inicial_cor'] = 0
                            dictTurno['inicial_tons'] = 0
                        else:
                            tot_volNat_esfera_ini = tot_volNat_esfera_ini + dataEsferaInicio.volumenBlsNat
                            tot_volCor_esfera_ini = tot_volCor_esfera_ini + dataEsferaInicio.volumenBlsCor
                            tot_tons_esfera_ini = tot_tons_esfera_ini + dataEsferaInicio.volumenTon

                        dictTurno['inicial_nat'] = tot_volNat_esfera_ini
                        dictTurno['inicial_cor'] = tot_volCor_esfera_ini
                        dictTurno['inicial_tons'] = tot_tons_esfera_ini
                        
                        inicial_nat = tot_volNat_esfera_ini
                        inicial_cor = tot_volCor_esfera_ini
                        inicial_tons = tot_tons_esfera_ini

                        dataEsferaFinal = Esfera.select().where(Esfera.reporte05 == fecha, Esfera.turno05 == turno, Esfera.esfera == j).order_by(Esfera.id.desc()).first()

                        if dataEsferaFinal is None:
                            dictTurno['final_nat'] = 0
                            dictTurno['final_cor'] = 0
                            dictTurno['final_tons'] = 0
                        else:
                            tot_volNat_esfera_fin = tot_volNat_esfera_fin + dataEsferaFinal.volumenBlsNat
                            tot_volCor_esfera_fin = tot_volCor_esfera_fin + dataEsferaFinal.volumenBlsCor
                            tot_tons_esfera_fin = tot_tons_esfera_fin + dataEsferaFinal.volumenTon

                        dictTurno['final_nat'] = tot_volNat_esfera_fin
                        dictTurno['final_cor'] = tot_volCor_esfera_fin
                        dictTurno['final_tons'] = tot_tons_esfera_fin
                        

                    elif turno == 2:
                        dataEsferaInicio = Esfera.select().where(Esfera.reporte05 == fecha, Esfera.turno05 == 1, Esfera.esfera == j).order_by(Esfera.id.desc()).first()
                        dictTurno['turno'] = strTurnos[turno - 1]
                        
                        if dataEsferaInicio is None:
                            dictTurno['inicial_nat'] = 0
                            dictTurno['inicial_cor'] = 0
                            dictTurno['inicial_tons'] = 0
                        else:
                            tot_volNat_esfera_ini = tot_volNat_esfera_ini + dataEsferaInicio.volumenBlsNat
                            tot_volCor_esfera_ini = tot_volCor_esfera_ini + dataEsferaInicio.volumenBlsCor
                            tot_tons_esfera_ini = tot_tons_esfera_ini + dataEsferaInicio.volumenTon

                        dictTurno['inicial_nat'] = tot_volNat_esfera_ini
                        dictTurno['inicial_cor'] = tot_volCor_esfera_ini
                        dictTurno['inicial_tons'] = tot_tons_esfera_ini

                        dataEsferaFinal = Esfera.select().where(Esfera.reporte05 == fecha, Esfera.turno05 == turno, Esfera.esfera == j).order_by(Esfera.id.desc()).first()

                        if dataEsferaFinal is None:
                            dictTurno['final_nat'] = 0
                            dictTurno['final_cor'] = 0
                            dictTurno['final_tons'] = 0
                        else:
                            tot_volNat_esfera_fin = tot_volNat_esfera_fin + dataEsferaFinal.volumenBlsNat
                            tot_volCor_esfera_fin = tot_volCor_esfera_fin + dataEsferaFinal.volumenBlsCor
                            tot_tons_esfera_fin = tot_tons_esfera_fin + dataEsferaFinal.volumenTon

                        dictTurno['final_nat'] = tot_volNat_esfera_fin
                        dictTurno['final_cor'] = tot_volCor_esfera_fin
                        dictTurno['final_tons'] = tot_tons_esfera_fin

                    elif turno == 3:
                        dataEsferaInicio = Esfera.select().where(Esfera.reporte05 == fecha, Esfera.turno05 == 2, Esfera.esfera == j).order_by(Esfera.id.desc()).first()
                        dictTurno['turno'] = strTurnos[turno - 1]
                        
                        if dataEsferaInicio is None:
                            dictTurno['inicial_nat'] = 0
                            dictTurno['inicial_cor'] = 0
                            dictTurno['inicial_tons'] = 0
                        else:
                            tot_volNat_esfera_ini = tot_volNat_esfera_ini + dataEsferaInicio.volumenBlsNat
                            tot_volCor_esfera_ini = tot_volCor_esfera_ini + dataEsferaInicio.volumenBlsCor
                            tot_tons_esfera_ini = tot_tons_esfera_ini + dataEsferaInicio.volumenTon

                        dictTurno['inicial_nat'] = tot_volNat_esfera_ini
                        dictTurno['inicial_cor'] = tot_volCor_esfera_ini
                        dictTurno['inicial_tons'] = tot_tons_esfera_ini

                        dataEsferaFinal = Esfera.select().where(Esfera.reporte05 == fecha, Esfera.turno05 == turno, Esfera.esfera == j).order_by(Esfera.id.desc()).first()

                        if dataEsferaFinal is None:
                            dictTurno['final_nat'] = 0
                            dictTurno['final_cor'] = 0
                            dictTurno['final_tons'] = 0
                        else:
                            tot_volNat_esfera_fin = tot_volNat_esfera_fin + dataEsferaFinal.volumenBlsNat
                            tot_volCor_esfera_fin = tot_volCor_esfera_fin + dataEsferaFinal.volumenBlsCor
                            tot_tons_esfera_fin = tot_tons_esfera_fin + dataEsferaFinal.volumenTon
                    
                        final_nat = tot_volNat_esfera_fin
                        final_cor = tot_volCor_esfera_fin
                        final_tons =  tot_tons_esfera_fin

                        dictTurno['final_nat'] = tot_volNat_esfera_fin
                        dictTurno['final_cor'] = tot_volCor_esfera_fin
                        dictTurno['final_tons'] = tot_tons_esfera_fin

                dictTurno['dif_nat'] = tot_volNat_esfera_ini + blsNat_turno_rec - blsNat_turno_venta - tot_volNat_esfera_fin
                dictTurno['dif_cor'] = tot_volCor_esfera_ini + blsCor_turno_rec - blsCor_turno_venta - tot_volCor_esfera_fin
                dictTurno['dif_tons'] = tot_tons_esfera_ini + tons_turno_rec - tons_turno_venta - tot_tons_esfera_fin
                
            else:
                # Filtrando la data de patines
                filtered_arr = [p for p in dataPatines if p.turno24 == turno]
                dictTurno['turno'] = turno
                blsNat_turno_rec = 0
                blsCor_turno_rec = 0
                tons_turno_rec = 0
                blsNat_turno_venta = 0
                blsCor_turno_venta = 0
                tons_turno_venta = 0
                if len(filtered_arr) > 0:
                    for fa in filtered_arr:
                        blsNat_turno_rec = blsNat_turno_rec + fa.volUnc
                        blsCor_turno_rec = blsCor_turno_rec + fa.blsCor
                        tons_turno_rec = tons_turno_rec + fa.ton
                        recibo_nat = blsNat_turno_rec + fa.volUnc
                        recibo_cor = blsCor_turno_rec + fa.blsCor
                        recibo_tons = tons_turno_rec + fa.ton

                    dictTurno['recibo_nat'] = blsNat_turno_rec
                    dictTurno['recibo_cor'] = blsCor_turno_rec
                    dictTurno['recibo_tons'] = tons_turno_rec
                else:
                    dictTurno['recibo_nat'] = 0
                    dictTurno['recibo_cor'] = 0
                    dictTurno['recibo_tons'] = 0
                

                # Filtrando la data de salidas
                filter_salidas = [s for s in dataSalidas if s.turno24 == turno]
                #print(f'Salidas {len(filter_salidas)}')
                if len(filter_salidas) > 0:
                    for fs in filter_salidas:
                        ventas_nat = ventas_nat + fs.volNatBls
                        ventas_cor = ventas_cor + fs.volCorBls
                        ventas_tons = ventas_tons + fs.masaTons
                        blsNat_turno_venta = blsNat_turno_venta + fs.volNatBls
                        blsCor_turno_venta = blsCor_turno_venta + fs.volCorBls
                        tons_turno_venta = tons_turno_venta + fs.masaTons
                    dictTurno['ventas_nat'] = blsNat_turno_venta
                    dictTurno['ventas_cor'] = blsCor_turno_venta
                    dictTurno['ventas_tons'] = tons_turno_venta
                    dictTurno['ventas_pgs'] = len(filter_salidas)
                    ventas_pgs = ventas_pgs + len(filter_salidas)
                else:
                    dictTurno['ventas_nat'] = 0
                    dictTurno['ventas_cor'] = 0
                    dictTurno['ventas_tons'] = 0
                    dictTurno['ventas_pgs'] = 0

                # Leer data de inventarios de esferas inicio
                esferas = [1,2]
                
                tot_volNat_esfera_ini = 0
                tot_volCor_esfera_ini = 0
                tot_tons_esfera_ini = 0
                tot_volNat_esfera_fin = 0
                tot_volCor_esfera_fin = 0
                tot_tons_esfera_fin = 0

                for j in esferas:
                    if turno == 1:
                        dataEsferaInicio = Esfera.select().where(Esfera.reporte24 == fechaAnt, Esfera.esfera == j).order_by(Esfera.id.desc()).first()
                        dictTurno['turno'] = strTurnos[turno - 1]

                        if dataEsferaInicio is None:
                            dictTurno['inicial_nat'] = 0
                            dictTurno['inicial_cor'] = 0
                            dictTurno['inicial_tons'] = 0
                        else:
                            tot_volNat_esfera_ini = tot_volNat_esfera_ini + dataEsferaInicio.volumenBlsNat
                            tot_volCor_esfera_ini = tot_volCor_esfera_ini + dataEsferaInicio.volumenBlsCor
                            tot_tons_esfera_ini = tot_tons_esfera_ini + dataEsferaInicio.volumenTon

                        dictTurno['inicial_nat'] = tot_volNat_esfera_ini
                        dictTurno['inicial_cor'] = tot_volCor_esfera_ini
                        dictTurno['inicial_tons'] = tot_tons_esfera_ini
                        
                        inicial_nat = tot_volNat_esfera_ini
                        inicial_cor = tot_volCor_esfera_ini
                        inicial_tons = tot_tons_esfera_ini

                        dataEsferaFinal = Esfera.select().where(Esfera.reporte24 == fecha, Esfera.turno24 == turno, Esfera.esfera == j).order_by(Esfera.id.desc()).first()

                        if dataEsferaFinal is None:
                            dictTurno['final_nat'] = 0
                            dictTurno['final_cor'] = 0
                            dictTurno['final_tons'] = 0
                        else:
                            tot_volNat_esfera_fin = tot_volNat_esfera_fin + dataEsferaFinal.volumenBlsNat
                            tot_volCor_esfera_fin = tot_volCor_esfera_fin + dataEsferaFinal.volumenBlsCor
                            tot_tons_esfera_fin = tot_tons_esfera_fin + dataEsferaFinal.volumenTon

                        dictTurno['final_nat'] = tot_volNat_esfera_fin
                        dictTurno['final_cor'] = tot_volCor_esfera_fin
                        dictTurno['final_tons'] = tot_tons_esfera_fin
                        

                    elif turno == 2:
                        dataEsferaInicio = Esfera.select().where(Esfera.reporte24 == fecha, Esfera.turno24 == 1, Esfera.esfera == j).order_by(Esfera.id.desc()).first()
                        dictTurno['turno'] = strTurnos[turno - 1]
                        
                        if dataEsferaInicio is None:
                            dictTurno['inicial_nat'] = 0
                            dictTurno['inicial_cor'] = 0
                            dictTurno['inicial_tons'] = 0
                        else:
                            tot_volNat_esfera_ini = tot_volNat_esfera_ini + dataEsferaInicio.volumenBlsNat
                            tot_volCor_esfera_ini = tot_volCor_esfera_ini + dataEsferaInicio.volumenBlsCor
                            tot_tons_esfera_ini = tot_tons_esfera_ini + dataEsferaInicio.volumenTon

                        dictTurno['inicial_nat'] = tot_volNat_esfera_ini
                        dictTurno['inicial_cor'] = tot_volCor_esfera_ini
                        dictTurno['inicial_tons'] = tot_tons_esfera_ini

                        dataEsferaFinal = Esfera.select().where(Esfera.reporte24 == fecha, Esfera.turno24 == turno, Esfera.esfera == j).order_by(Esfera.id.desc()).first()

                        if dataEsferaFinal is None:
                            dictTurno['final_nat'] = 0
                            dictTurno['final_cor'] = 0
                            dictTurno['final_tons'] = 0
                        else:
                            tot_volNat_esfera_fin = tot_volNat_esfera_fin + dataEsferaFinal.volumenBlsNat
                            tot_volCor_esfera_fin = tot_volCor_esfera_fin + dataEsferaFinal.volumenBlsCor
                            tot_tons_esfera_fin = tot_tons_esfera_fin + dataEsferaFinal.volumenTon

                        dictTurno['final_nat'] = tot_volNat_esfera_fin
                        dictTurno['final_cor'] = tot_volCor_esfera_fin
                        dictTurno['final_tons'] = tot_tons_esfera_fin

                    elif turno == 3:
                        dataEsferaInicio = Esfera.select().where(Esfera.reporte24 == fecha, Esfera.turno24 == 2, Esfera.esfera == j).order_by(Esfera.id.desc()).first()
                        dictTurno['turno'] = strTurnos[turno - 1]
                        
                        if dataEsferaInicio is None:
                            dictTurno['inicial_nat'] = 0
                            dictTurno['inicial_cor'] = 0
                            dictTurno['inicial_tons'] = 0
                        else:
                            tot_volNat_esfera_ini = tot_volNat_esfera_ini + dataEsferaInicio.volumenBlsNat
                            tot_volCor_esfera_ini = tot_volCor_esfera_ini + dataEsferaInicio.volumenBlsCor
                            tot_tons_esfera_ini = tot_tons_esfera_ini + dataEsferaInicio.volumenTon

                        dictTurno['inicial_nat'] = tot_volNat_esfera_ini
                        dictTurno['inicial_cor'] = tot_volCor_esfera_ini
                        dictTurno['inicial_tons'] = tot_tons_esfera_ini

                        dataEsferaFinal = Esfera.select().where(Esfera.reporte24 == fecha, Esfera.turno24 == turno, Esfera.esfera == j).order_by(Esfera.id.desc()).first()

                        if dataEsferaFinal is None:
                            dictTurno['final_nat'] = 0
                            dictTurno['final_cor'] = 0
                            dictTurno['final_tons'] = 0
                        else:
                            tot_volNat_esfera_fin = tot_volNat_esfera_fin + dataEsferaFinal.volumenBlsNat
                            tot_volCor_esfera_fin = tot_volCor_esfera_fin + dataEsferaFinal.volumenBlsCor
                            tot_tons_esfera_fin = tot_tons_esfera_fin + dataEsferaFinal.volumenTon
                            final_nat = final_nat + tot_volNat_esfera_fin
                            final_cor = final_cor + tot_volCor_esfera_fin
                            final_tons = final_tons + tot_tons_esfera_fin

                        dictTurno['final_nat'] = tot_volNat_esfera_fin
                        dictTurno['final_cor'] = tot_volCor_esfera_fin
                        dictTurno['final_tons'] = tot_tons_esfera_fin

                dictTurno['dif_nat'] = tot_volNat_esfera_ini + blsNat_turno_rec - blsNat_turno_venta - tot_volNat_esfera_fin
                dictTurno['dif_cor'] = tot_volCor_esfera_ini + blsCor_turno_rec - blsCor_turno_venta - tot_volCor_esfera_fin
                dictTurno['dif_tons'] = tot_tons_esfera_ini + tons_turno_rec - tons_turno_venta - tot_tons_esfera_fin
            
            dataReporte.append(dictTurno)
            dif_nat = inicial_nat + recibo_nat - ventas_nat - final_nat
            dif_cor = inicial_cor + recibo_cor - ventas_cor - final_cor
            dif_tons = inicial_tons + recibo_tons - ventas_tons - final_tons

            dictTotales['turno'] = 'TOTAL'
            dictTotales['inicial_nat'] = inicial_nat
            dictTotales['inicial_cor'] = inicial_cor
            dictTotales['inicial_tons'] = inicial_tons
            dictTotales['recibo_nat'] = recibo_nat
            dictTotales['recibo_cor'] = recibo_cor
            dictTotales['recibo_tons'] = recibo_tons
            dictTotales['ventas_nat'] = ventas_nat
            dictTotales['ventas_cor'] = ventas_cor
            dictTotales['ventas_tons'] = ventas_tons
            dictTotales['ventas_pgs'] = ventas_pgs
            dictTotales['final_nat'] = final_nat
            dictTotales['final_cor'] = final_cor
            dictTotales['final_tons'] = final_tons
            dictTotales['dif_nat'] = dif_nat
            dictTotales['dif_cor'] = dif_cor
            dictTotales['dif_tons'] = dif_tons

        dataReporte.append(dictTotales)
        
        BalanceDiario.truncate_table()
        for rep in dataReporte:
            itemSaved = registerBalanceDiarioItem(rep)

        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_balance = f"{JASPER_SERVER}/rest_v2/reports/reportes/balances/balanceDiario{tipoRep}.pdf"
        params = {
            "fecha": fecha
        }
        
        res = s.get(url=url_balance, params=params, stream=True)
        res.raise_for_status()
        filename = f"balance_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

@router.get('/balance-mensual/{fecha}/tipo/{tipo}')
async def get_balance_mensual_report(fecha: str, tipo: int):
    try:
        # Función para llenar la tabla de balance mensual
        # periodo = '2023-08'
        LogsServices.setNameFile()
        
        # Obtener el último día
        fechaF = obtenerUltimoDiaMesOrAhora(datetime.strptime(fecha, '%Y-%m-%d'))
        ultimoDiaDT = datetime.strptime(fechaF, '%Y-%m-%d')
        dia_fin =ultimoDiaDT.day
        
        fechaAnt = obtenerDiaAnterior(fecha)

        #   Declaramos los arrays donde almacenaremos la data
        dataReporte = []
        dictTotales = {}

        # Variables para llenar el reporte
        inicial_nat = 0
        inicial_cor = 0
        inicial_tons = 0
        recibo_nat = 0
        recibo_cor = 0
        recibo_tons = 0
        ventas_nat = 0
        ventas_cor = 0
        ventas_tons = 0
        ventas_pgs = 0
        final_nat = 0
        final_cor = 0
        final_tons = 0

        # recorremos las fechas
        for i in range(1, dia_fin + 1):
            fechaDT = datetime(ultimoDiaDT.year, ultimoDiaDT.month, i)
            fecha = fechaDT.strftime('%Y-%m-%d')
            fecha_dia = fechaDT.strftime('%d')

            #   inicializamos variables en el ciclo 
            dictFecha = {}

            # obtenemos la data por día
            if tipo == 5:
                dataPatines = PatinData.select().where(PatinData.reporte05 == fecha)
                dataSalidas = TankInTrucks.select().where(TankInTrucks.reporte05 == fecha)
            
            else:
                dataPatines = PatinData.select().where(PatinData.reporte24 == fecha)
                dataSalidas = TankInTrucks.select().where(TankInTrucks.reporte24 == fecha)
            
            dictFecha['dia'] = fecha_dia
            blsNat_fecha_rec = 0
            blsCor_fecha_rec = 0
            tons_fecha_rec = 0
            blsNat_fecha_venta = 0
            blsCor_fecha_venta = 0
            tons_fecha_venta = 0

            #   Recorriendo las entradas
            for dP in dataPatines:
                blsNat_fecha_rec = blsNat_fecha_rec + dP.volUnc
                blsCor_fecha_rec = blsCor_fecha_rec + dP.blsCor
                tons_fecha_rec = tons_fecha_rec + dP.ton
                recibo_nat = recibo_nat + dP.volUnc
                recibo_cor = recibo_cor + dP.blsCor
                recibo_tons = recibo_tons + dP.ton

            dictFecha['recibo_nat'] = blsNat_fecha_rec
            dictFecha['recibo_cor'] = blsCor_fecha_rec
            dictFecha['recibo_tons'] = tons_fecha_rec
            
            #   Recorriendo las salidas
            for dS in dataSalidas:
                blsNat_fecha_venta = blsNat_fecha_venta + dS.volNatBls
                blsCor_fecha_venta = blsCor_fecha_venta + dS.volCorBls
                tons_fecha_venta = tons_fecha_venta + dS.masaTons
                ventas_nat = ventas_nat + dS.volNatBls
                ventas_cor = ventas_cor + dS.volCorBls
                ventas_tons = ventas_tons + dS.masaTons
                
            dictFecha['ventas_nat'] = blsNat_fecha_venta
            dictFecha['ventas_cor'] = blsCor_fecha_venta
            dictFecha['ventas_tons'] = tons_fecha_venta
            dictFecha['ventas_pgs'] = len(dataSalidas)
            ventas_pgs = ventas_pgs + len(dataSalidas)

            # Leer data de inventarios de esferas inicio
            esferas = [1,2]
                
            tot_volNat_esfera_ini = 0
            tot_volCor_esfera_ini = 0
            tot_tons_esfera_ini = 0
            tot_volNat_esfera_fin = 0
            tot_volCor_esfera_fin = 0
            tot_tons_esfera_fin = 0

            if tipo == 5:
                for j in esferas:
                    dataEsferaInicio = Esfera.select().where(Esfera.reporte05 == fecha, Esfera.esfera == j).order_by(Esfera.id.asc()).first()
            
                    if dataEsferaInicio is None:
                        LogsServices.write(f'No se encontró el dato de la esfera - inicio: {fecha}')
                    else:
                        tot_volNat_esfera_ini = tot_volNat_esfera_ini + dataEsferaInicio.volumenBlsNat
                        tot_volCor_esfera_ini = tot_volCor_esfera_ini + dataEsferaInicio.volumenBlsCor
                        tot_tons_esfera_ini = tot_tons_esfera_ini + dataEsferaInicio.volumenTon
                    
                    if i == 1:
                        inicial_nat = tot_volNat_esfera_ini
                        inicial_cor = tot_volCor_esfera_ini
                        inicial_tons = tot_tons_esfera_ini
                    
                    dataEsferaFinal = Esfera.select().where(Esfera.reporte05 == fecha, Esfera.esfera == j).order_by(Esfera.id.desc()).first()

                    if dataEsferaFinal is None:
                        LogsServices.write(f'No se encontró el dato de la esfera - final: {fecha}')
                    else:
                        tot_volNat_esfera_fin = tot_volNat_esfera_fin + dataEsferaFinal.volumenBlsNat
                        tot_volCor_esfera_fin = tot_volCor_esfera_fin + dataEsferaFinal.volumenBlsCor
                        tot_tons_esfera_fin = tot_tons_esfera_fin + dataEsferaFinal.volumenTon
                    
                    if dia_fin == i:
                        final_nat = tot_volNat_esfera_fin
                        final_cor = tot_volCor_esfera_fin
                        final_tons = tot_tons_esfera_fin    
                
                dictFecha['inicial_nat'] = tot_volNat_esfera_ini
                dictFecha['inicial_cor'] = tot_volCor_esfera_ini
                dictFecha['inicial_tons'] = tot_tons_esfera_ini
                dictFecha['final_nat'] = tot_volNat_esfera_fin
                dictFecha['final_cor'] = tot_volCor_esfera_fin
                dictFecha['final_tons'] = tot_tons_esfera_fin
                dictFecha['dif_nat'] = tot_volNat_esfera_fin + blsNat_fecha_venta - tot_volNat_esfera_ini + blsNat_fecha_rec
                dictFecha['dif_cor'] = tot_volCor_esfera_fin + blsCor_fecha_venta - tot_volCor_esfera_ini + blsCor_fecha_rec
                dictFecha['dif_tons'] = tot_tons_esfera_fin + tons_fecha_venta - tot_tons_esfera_ini + tons_fecha_rec

            else:
                for j in esferas:
                    dataEsferaInicio = Esfera.select().where(Esfera.reporte24 == fecha, Esfera.esfera == j).order_by(Esfera.id.asc()).first()
            
                    if dataEsferaInicio is None:
                        LogsServices.write(f'No se encontró el dato de la esfera - inicio: {fecha}')
                    else:
                        tot_volNat_esfera_ini = tot_volNat_esfera_ini + dataEsferaInicio.volumenBlsNat
                        tot_volCor_esfera_ini = tot_volCor_esfera_ini + dataEsferaInicio.volumenBlsCor
                        tot_tons_esfera_ini = tot_tons_esfera_ini + dataEsferaInicio.volumenTon
                    
                    if i == 1:
                        inicial_nat = tot_volNat_esfera_ini
                        inicial_cor = tot_volCor_esfera_ini
                        inicial_tons = tot_tons_esfera_ini

                    dataEsferaFinal = Esfera.select().where(Esfera.reporte24 == fecha, Esfera.esfera == j).order_by(Esfera.id.desc()).first()

                    if dataEsferaFinal is None:
                        LogsServices.write(f'No se encontró el dato de la esfera - final: {fecha}')
                    else:
                        tot_volNat_esfera_fin = tot_volNat_esfera_fin + dataEsferaFinal.volumenBlsNat
                        tot_volCor_esfera_fin = tot_volCor_esfera_fin + dataEsferaFinal.volumenBlsCor
                        tot_tons_esfera_fin = tot_tons_esfera_fin + dataEsferaFinal.volumenTon
                    
                    if dia_fin == i:
                        final_nat = tot_volNat_esfera_fin
                        final_cor = tot_volCor_esfera_fin
                        final_tons = tot_tons_esfera_fin    

                dictFecha['inicial_nat'] = tot_volNat_esfera_ini
                dictFecha['inicial_cor'] = tot_volCor_esfera_ini
                dictFecha['inicial_tons'] = tot_tons_esfera_ini
                dictFecha['final_nat'] = tot_volNat_esfera_fin
                dictFecha['final_cor'] = tot_volCor_esfera_fin
                dictFecha['final_tons'] = tot_tons_esfera_fin
                dictFecha['dif_nat'] = tot_volNat_esfera_fin + blsNat_fecha_venta - tot_volNat_esfera_ini + blsNat_fecha_rec
                dictFecha['dif_cor'] = tot_volCor_esfera_fin + blsCor_fecha_venta - tot_volCor_esfera_ini + blsCor_fecha_rec
                dictFecha['dif_tons'] = tot_tons_esfera_fin + tons_fecha_venta - tot_tons_esfera_ini + tons_fecha_rec

            dataReporte.append(dictFecha)
            dif_nat = final_nat + ventas_nat - inicial_nat + recibo_nat
            dif_cor = final_cor + ventas_cor - inicial_cor + recibo_cor
            dif_tons = final_tons + ventas_tons - inicial_tons + recibo_tons
        
        dictTotales['dia'] = 'TOTAL'
        dictTotales['inicial_nat'] = inicial_nat
        dictTotales['inicial_cor'] = inicial_cor
        dictTotales['inicial_tons'] = inicial_tons
        dictTotales['recibo_nat'] = recibo_nat
        dictTotales['recibo_cor'] = recibo_cor
        dictTotales['recibo_tons'] = recibo_tons
        dictTotales['ventas_nat'] = ventas_nat
        dictTotales['ventas_cor'] = ventas_cor
        dictTotales['ventas_tons'] = ventas_tons
        dictTotales['ventas_pgs'] = ventas_pgs
        dictTotales['final_nat'] = final_nat
        dictTotales['final_cor'] = final_cor
        dictTotales['final_tons'] = final_tons
        dictTotales['dif_nat'] = dif_nat
        dictTotales['dif_cor'] = dif_cor
        dictTotales['dif_tons'] = dif_tons
        
        dataReporte.append(dictTotales)
        
        BalanceMensual.truncate_table()
        for rep in dataReporte:
            itemSaved = registerBalanceMensualItem(rep)
        

        hoy = datetime.now().strftime('%Y-%m-%d')
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_balance = f"{JASPER_SERVER}/rest_v2/reports/reportes/balances/BalanceMensual{tipoRep}.pdf"
        params = {
            "fecha": hoy
        }
        
        res = s.get(url=url_balance, params=params, stream=True)
        res.raise_for_status()
        filename = f"balance_{hoy}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

@router.get('/patin-pares/{fecha}/tipo/{tipo}/patin/{patin}')
async def get_patin_individual_report(fecha: str, tipo: int, patin: int):
    try:

        # Obtener la data de los patines
        dataPatines = None
        if patin == 400:
            if tipo == 5:
                dataPatines = PatinData.select(Patin, fn.SUM(PatinData.ton).alias('toneladas'), fn.SUM(PatinData.blsNat).alias('blsNat'), fn.SUM(PatinData.blsCor).alias('blsCor')).join(Patin).where(
                        PatinData.reporte05 == fecha).group_by(Patin.descripcion)
                
                print(dataPatines)
            else:
                dataPatines = PatinData.select(Patin, fn.SUM(PatinData.ton).alias('toneladas'), fn.SUM(PatinData.blsNat).alias('blsNat'), fn.SUM(PatinData.blsCor).alias('blsCor')).join(Patin).where(
                        PatinData.reporte24 == fecha).group_by(Patin.descripcion)
        else:
            id_patin1 = 0
            id_patin2 = 0
            if patin == 401:
                id_patin1 = 1
                id_patin2 = 2
            else:
                id_patin1 = 3
                id_patin2 = 4
            if tipo == 5:
                dataPatines = PatinData.select(Patin, fn.SUM(PatinData.ton).alias('toneladas'), fn.SUM(PatinData.blsNat).alias('blsNat'), fn.SUM(PatinData.blsCor).alias('blsCor')).join(Patin).where(
                    (PatinData.reporte05 == fecha) & (PatinData.patin == id_patin1) |
                    (PatinData.reporte05 == fecha) & (PatinData.patin == id_patin2)
                ).group_by(Patin.descripcion)
            else:
                dataPatines = PatinData.select(Patin, fn.SUM(PatinData.ton).alias('toneladas'), fn.SUM(PatinData.blsNat).alias('blsNat'), fn.SUM(PatinData.blsCor).alias('blsCor')).join(Patin).where(
                    (PatinData.reporte24 == fecha) & (PatinData.patin == id_patin1) |
                    (PatinData.reporte24 == fecha) & (PatinData.patin == id_patin2)
                ).group_by(Patin.descripcion)

            if dataPatines is None:
                return JSONResponse(
                    status_code=404,
                    content={"message": 'No hay registros'}
                )
            
        ReportePatin.truncate_table()
        for dp in dataPatines.objects():
            print(f'toneladas: {dp.toneladas}')
            print(f'blsNat: {dp.blsNat}')
            print(f'blsCor: {dp.blsCor}')
            print(f'medidor: {dp.descripcion}')
            itemSaved = resgisterReciboPatinItem(dp)


        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        if patin == 400:
            path_report = f"{JASPER_SERVER}/rest_v2/reports/reportes/patines/Patines{tipoRep}.pdf"
        else:
            path_report = f"{JASPER_SERVER}/rest_v2/reports/reportes/patines/Patin{patin}{tipoRep}.pdf"
        print(path_report)
        url_patin = path_report
        params = {
            "fecha": fecha
        }
        
        res = s.get(url=url_patin, params=params, stream=True)
        res.raise_for_status()
        filename = f"patin{patin}_{tipoRep}_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

@router.get('/densidades/{fecha}/tipo/{tipo}')
async def get_bitacora_report(fecha: str,  tipo: int):
    try:
        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        url_densidades = f"{JASPER_SERVER}/rest_v2/reports/reportes/cromatografo/densidades{tipoRep}.pdf"
        params = {
            "fecha": fecha
        }
        
        res = s.get(url=url_densidades, params=params, stream=True)
        res.raise_for_status()
        filename = f"densidades{tipoRep}_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

@router.get('/cromatografo-mensual/{fecha}/croma/{croma}/tipo/{tipo}')
async def get_bitacora_report(fecha: str,  tipo: int, croma: str):
    try:
        fechaDT = datetime.strptime(fecha, '%Y-%m-%d')
        fechaI = date(fechaDT.year, fechaDT.month, 1)
        fechaF = obtenerUltimoDiaMesOrAhora(datetime.strptime(fecha, '%Y-%m-%d'))

        # buffer = io.BytesIO()
        s = requests.session()
        auth = ('jasperadmin', 'jasperadmin')
        url_login = f"{JASPER_SERVER}"
        res = s.get(url=url_login, auth=auth)
        res.raise_for_status()
        tipoRep = '_24' if tipo == 24 else ''
        cromaTipo = f'{croma}_{tipo}'
        cromaSel = getNameCromatografoMensual(cromaTipo)
        pathReport = f"{JASPER_SERVER}/rest_v2/reports/reportes/cromatografo/{cromaSel}.pdf"
        url_densidades = pathReport
        params = {
            "fecha": fecha,
            "fechaI": fechaI,
            "fechaF": fechaF,
        }
        
        res = s.get(url=url_densidades, params=params, stream=True)
        res.raise_for_status()
        filename = f"cromatografo_mensual_{croma}{tipoRep}_{fecha}.pdf"
        path = f'./downloads/{filename}'

        with open(path, 'wb') as f:
            f.write(res.content)

        return FileResponse(path=path, filename=filename, media_type='application/pdf')

        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )


def registerBalanceDiarioItem(item):
    
    itemSaved = BalanceDiario.create(
        turno = item['turno'],
        inicial_nat = item['inicial_nat'],
        inicial_cor = item['inicial_cor'],
        inicial_tons = item['inicial_tons'],
        recibo_nat = item['recibo_nat'],
        recibo_cor = item['recibo_cor'],
        recibo_tons = item['recibo_tons'],
        ventas_nat = item['ventas_nat'],
        ventas_cor = item['ventas_cor'],
        ventas_tons = item['ventas_tons'],
        ventas_pgs = item['ventas_pgs'],
        final_nat = item['final_nat'],
        final_cor = item['final_cor'],
        final_tons = item['final_tons'],
        dif_nat = item['dif_nat'],
        dif_cor = item['dif_cor'],
        dif_tons = item['dif_tons'],
    )

    return itemSaved


def registerBalanceMensualItem(item):
    itemSaved = BalanceMensual.create(
        dia = item['dia'],
        inicial_nat = item['inicial_nat'],
        inicial_cor = item['inicial_cor'],
        inicial_tons = item['inicial_tons'],
        recibo_nat = item['recibo_nat'],
        recibo_cor = item['recibo_cor'],
        recibo_tons = item['recibo_tons'],
        ventas_nat = item['ventas_nat'],
        ventas_cor = item['ventas_cor'],
        ventas_tons = item['ventas_tons'],
        ventas_pgs = item['ventas_pgs'],
        final_nat = item['final_nat'],
        final_cor = item['final_cor'],
        final_tons = item['final_tons'],
        dif_nat = item['dif_nat'],
        dif_cor = item['dif_cor'],
        dif_tons = item['dif_tons'],
    )

    return itemSaved


def resgisterReciboPatinItem(item):
    itemsaved = ReportePatin.create(
        medidor = item.descripcion,
        toneladas = item.toneladas,
        blsNat = item.blsNat,
        blsCor = item.blsCor,
    )

    return itemsaved


def getNameCromatografoMensual(croma):
    tabla_cromas = {
        'irge_5': 'cromatografoIrge_mensual',
        'irge_24': 'cromatografoIrge_mensual_24',
        'c1_5': 'cromatografoC1_mensual',
        'c1_24': 'cromatografoC1_mensual_24',
        'c2_5': 'cromatografoC2_mensual',
        'c2_24': 'cromatografoC2_mensual_24',
        'c3_5': 'cromatografoC3_mensual',
        'c3_24': 'cromatografoC3_mensual_24',

    }
    
    return tabla_cromas.get(croma, 0 )


def getCromatografo(croma):
    tabla_cromas = {
        1: 'cromatografoIrge',
        2: 'cromatografoC1',
        3: 'cromatografoC2',
        4: 'cromatografoC3',
    }
    
    return tabla_cromas.get(croma, 0 )
