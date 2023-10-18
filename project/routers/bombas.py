from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime, timedelta
from ..funciones import obtenerFecha05Reporte, obtenerFecha24Reporte, obtenerTurno05, obtenerTurno24, get_clock

from ..database import Bomba, Bitacora, Horas
from ..schemas import BombaResponseModel

from ..opc import OpcServices

from fastapi_pagination import paginate
from fastapi_pagination.links import Page

from ..middlewares import VerifyTokenRoute
router = APIRouter(prefix='/api/v1/bombas', route_class=VerifyTokenRoute)


@router.post('')
async def register_bomba():
    try:
        #   Primero obtenemos los valores de las variables
        print('register Bomba')
        ahora_json = await get_clock()
        ahora = ahora_json['fechaHora']
        ahoraDT = datetime.strptime(ahora, '%Y-%m-%d %H:%M:%S')
        dateStr = ahoraDT.strftime("%Y-%m-%d")
        hora = ahoraDT.strftime("%H")
        fecha05 = obtenerFecha05Reporte(ahoraDT.hour, dateStr)
        fecha24 = obtenerFecha24Reporte(ahoraDT.hour, dateStr)
        turno05 = obtenerTurno05(ahoraDT.hour)
        turno24 = obtenerTurno24(ahoraDT.hour)

        BA_301A_STATUS = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301A_STATUS')
        BA_301A_MODE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301A_MODE')
        BA_301A_TIME = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301A_TIME')
        BA_301B_STATUS = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301B_STATUS')
        BA_301B_MODE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301B_MODE')
        BA_301B_TIME = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301B_TIME')
        BA_301C_STATUS = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301C_STATUS')
        BA_301C_MODE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301C_MODE')
        BA_301C_TIME = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301C_TIME')

        minOper1 = round((BA_301A_TIME / 10000) * 60)
        totTiempoOper1 = f"{BA_301A_MODE}:0{round(minOper1)}" if round(minOper1) < 10 else f"{BA_301A_MODE}:{round(minOper1)}"
        print(f'BA_301A_MODE: {BA_301A_MODE}')
        print(f"minOper1 {minOper1}")
        print(f'totTiempoOper1: {totTiempoOper1}')

        minOper2 = round((BA_301B_TIME / 10000) * 60)
        totTiempoOper2 = f"{BA_301B_MODE}:0{round(minOper2)}" if round(minOper2) < 10 else f"{BA_301B_MODE}:{round(minOper2)}"
        print(f'BA_301B_MODE: {BA_301B_MODE}')
        print(f"minOper2 {minOper2}")
        print(f'totTiempoOper2: {totTiempoOper2}')

        minOper3 = round((BA_301C_TIME / 10000) * 60)
        totTiempoOper3 = f"{BA_301C_MODE}:0{round(minOper3)}" if round(minOper3) < 10 else f"{BA_301C_MODE}:{round(minOper3)}"
        print(f'BA_301C_MODE: {BA_301C_MODE}')
        print(f"minOper3: {minOper3}")
        print(f'totTiempoOper3: {totTiempoOper3}')



        bomba1 = Bomba.create(
            hora = f"{hora}:00",
            bomba = 'BA-301A',
            estatus = getStatus(BA_301A_STATUS),
            totalHorasOper = BA_301A_MODE,
            totalMinsOper = minOper1,
            totalTiempoOper = totTiempoOper1,
            horasOper = 0,
            minsOper = 0,
            enOper = 0,
            horasMantto = '0:00',
            minsMantto = 0,
            enMantto = '0:00',
            horasDisp = 0,
            minsDisp = 0,
            enDisp = '0:00',
            horasNoDisp = 0,
            minsNoDisp = 0,
            enNoDisp = '0:00',
            fecha = ahora,
            reporte05 =  fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        bomba2 = Bomba.create(
            hora = f"{hora}:00",
            bomba = 'BA-301B',
            estatus = getStatus(BA_301B_STATUS),
            totalHorasOper = BA_301B_MODE,
            totalMinsOper = minOper2,
            totalTiempoOper = totTiempoOper2,
            horasOper = 0,
            minsOper = 0,
            enOper = 0,
            horasMantto = '0:00',
            minsMantto = 0,
            enMantto = '0:00',
            horasDisp = 0,
            minsDisp = 0,
            enDisp = '0:00',
            horasNoDisp = 0,
            minsNoDisp = 0,
            enNoDisp = '0:00',
            fecha = ahora,
            reporte05 =  fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        bomba3 = Bomba.create(
            hora = f"{hora}:00",
            bomba = 'BA-301C',
            estatus = getStatus(BA_301C_STATUS),
            totalHorasOper = BA_301A_MODE,
            totalMinsOper = minOper3,
            totalTiempoOper = totTiempoOper3,
            horasOper = 0,
            minsOper = 0,
            enOper = 0,
            horasMantto = '0:00',
            minsMantto = 0,
            enMantto = '0:00',
            horasDisp = 0,
            minsDisp = 0,
            enDisp = '0:00',
            horasNoDisp = 0,
            minsNoDisp = 0,
            enNoDisp = '0:00',
            fecha = ahora,
            reporte05 =  fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        hours_in_db = Horas.select().where(Horas.id == 4).first()
        hours_in_db.hora = int(hora)
        hours_in_db.save()

        return JSONResponse(
            status_code=201,
            content={"message": "Bombas insertadas correctamente."}
        )


    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )


#@router.get('', response_model=Page[BombaResponseModel])
@router.get('', response_model=List[BombaResponseModel])
async def get_bombas():
    try:
        bombas = Bomba.select()
        return [ bomba for bomba in bombas ]
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )


def getStatus(estado):
    tabla_status = {
        0: 'Fuera de Operación',
        1: 'AUTOMATICO',
        2: 'LOCAL',
        3: 'INDEFINIDO',
    }
    
    return tabla_status.get(estado, 0 )