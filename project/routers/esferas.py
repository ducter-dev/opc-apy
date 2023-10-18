from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime, timedelta
from ..funciones import obtenerFecha05Reporte, obtenerFecha24Reporte, obtenerTurno05, obtenerTurno24, get_clock

from ..database import Esfera, Horas
from ..schemas import EsferaRequestModel, EsferaResponseModel

from ..opc import OpcServices
from ..logs import LogsServices

from ..middlewares import VerifyTokenRoute
router = APIRouter(prefix='/api/v1/esferas', route_class=VerifyTokenRoute)

@router.post('')
async def register_esfera():
    try:
        
        LogsServices.write('-------- Registrando Esferas --------')
        #   Primero obtenemos los valores de las variables
        PRES_PI_301A = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.PRES_PI_301A')
        TEMP_TI_301A = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.TEMP_TI_301A')
        DENS_DI_NAT_301A = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.DENS_DI_NAT_301A')
        DENS_DI_COR_301A = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.DENS_DI_COR_301A')
        VOL_NAT_301A_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_NAT_301A_ENT')
        VOL_NAT_301A_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_NAT_301A_DEC')
        VOL_COR_301A_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_COR_301A_ENT')
        VOL_COR_301A_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_COR_301A_DEC')
        NIVEL_LI_301A = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.NIVEL_LI_301A')
        PORCENT_301A = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.PORCENT_301A')
        VOL_NAT_DISP_301A = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_NAT_DISP_301A')
        VOL_COR_DISP_301A = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_COR_DISP_301A')
        MASA_NETA_301A_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.MASA_NETA_301A_ENT')
        MASA_NETA_301A_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.MASA_NETA_301A_DEC')
        MASA_DISP_301A_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.MASA_DISP_301A_ENT')
        MASA_DISP_301A_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.MASA_DISP_301A_DEC')
        """
        PRES_PI_301A = 813
        TEMP_TI_301A = 2108
        DENS_DI_NAT_301A = 5114
        DENS_DI_COR_301A = 5191
        VOL_NAT_301A_ENT = 7923
        VOL_NAT_301A_DEC = 249
        VOL_COR_301A_ENT = 7806
        VOL_COR_301A_DEC = 18
        NIVEL_LI_301A = 7332
        PORCENT_301A = 3669
        VOL_NAT_DISP_301A = 0
        VOL_COR_DISP_301A = 0
        MASA_NETA_301A_DEC = 642
        MASA_NETA_301A_ENT = 779
        MASA_DISP_301A_DEC = 627
        MASA_DISP_301A_ENT = 413
        """
        PRES_PI_301B = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.PRES_PI_301B')
        TEMP_TI_301B = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.TEMP_TI_301B')
        DENS_DI_NAT_301B = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.DENS_DI_NAT_301B')
        DENS_DI_COR_301B = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.DENS_DI_COR_301B')
        VOL_NAT_301B_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_NAT_301B_DEC')
        VOL_NAT_301B_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_NAT_301B_ENT')
        VOL_COR_301B_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_COR_301B_DEC')
        VOL_COR_301B_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_COR_301B_ENT')
        NIVEL_LI_301B = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.NIVEL_LI_301B')
        PORCENT_301B = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.PORCENT_301B')
        VOL_NAT_DISP_301B = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_NAT_DISP_301B')
        VOL_COR_DISP_301B = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.VOL_COR_DISP_301B')
        MASA_NETA_301B_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.MASA_NETA_301B_DEC')
        MASA_NETA_301B_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.MASA_NETA_301B_ENT')
        MASA_DISP_301B_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.MASA_DISP_301B_DEC')
        MASA_DISP_301B_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.MASA_DISP_301B_ENT') 
        """
        PRES_PI_301B = 820
        TEMP_TI_301B = 2110
        DENS_DI_NAT_301B = 5110
        DENS_DI_COR_301B = 5110
        VOL_NAT_301B_ENT = 7920
        VOL_NAT_301B_DEC = 240
        VOL_COR_301B_ENT = 7810
        VOL_COR_301B_DEC = 20
        NIVEL_LI_301B = 7330
        PORCENT_301B = 3670
        VOL_NAT_DISP_301B = 0
        VOL_COR_DISP_301B = 0
        MASA_NETA_301B_DEC = 640
        MASA_NETA_301B_ENT = 770
        MASA_DISP_301B_DEC = 620
        MASA_DISP_301B_ENT = 410
        """

        ahora_json = await get_clock()
        ahora = ahora_json['fechaHora']
        ahoraDT = datetime.strptime(ahora, '%Y-%m-%d %H:%M:%S')
        hora = ahoraDT.strftime("%H")
        dateStr = ahoraDT.strftime("%Y-%m-%d")
        fecha05 = obtenerFecha05Reporte(ahoraDT.hour, dateStr)
        fecha24 = obtenerFecha24Reporte(ahoraDT.hour, dateStr)
        turno05 = obtenerTurno05(ahoraDT.hour)
        turno24 = obtenerTurno24(ahoraDT.hour)
        
        """ LogsServices.write(f'fecha05: {fecha05}')
        LogsServices.write(f'fecha24: {fecha24}')
        LogsServices.write(f'turno05: {turno05}')
        LogsServices.write(f'turno24: {turno24}') """

        esferaRegister1 = Esfera.create(
            hora = f"{hora}:00",
            presion = PRES_PI_301A / 100,
            temperatura = TEMP_TI_301A / 100,
            densidad = DENS_DI_NAT_301A / 10000,
            densidadCor = DENS_DI_COR_301A / 10000,
            volumenBlsNat = VOL_NAT_301A_ENT + (VOL_NAT_301A_DEC / 1000),
            volumenBlsCor = VOL_COR_301A_ENT + (VOL_COR_301A_DEC / 1000),
            volumenTon = MASA_NETA_301A_ENT + (MASA_NETA_301A_DEC / 1000),
            porcentaje = PORCENT_301A / 100,
            nivel = NIVEL_LI_301A / 1000,
            volumenNatDisp = VOL_NAT_DISP_301A,
            volumenCorDisp = VOL_COR_DISP_301A,
            volumenTonDisp = MASA_DISP_301A_ENT + (MASA_DISP_301A_DEC / 1000),
            esfera = 1,
            fecha = ahora,
            reporte05 = fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        esferaRegister2 = Esfera.create(
            hora = f"{hora}:00",
            presion = PRES_PI_301B / 100,
            temperatura = TEMP_TI_301B / 100,
            densidad = DENS_DI_NAT_301B / 10000,
            densidadCor = DENS_DI_COR_301B / 10000,
            volumenBlsNat = VOL_NAT_301B_ENT + (VOL_NAT_301B_DEC / 1000),
            volumenBlsCor = VOL_COR_301B_ENT + (VOL_COR_301B_DEC / 1000),
            volumenTon = MASA_NETA_301B_ENT + (MASA_NETA_301B_DEC / 1000),
            porcentaje = PORCENT_301B / 100,
            nivel = NIVEL_LI_301B / 1000,
            volumenNatDisp = VOL_NAT_DISP_301B,
            volumenCorDisp = VOL_COR_DISP_301B,
            volumenTonDisp = MASA_DISP_301B_ENT + (MASA_DISP_301B_DEC / 1000),
            esfera = 2,
            fecha = ahora,
            reporte05 = fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        hours_in_db = Horas.select().where(Horas.id == 1).first()
        hours_in_db.hora = ahoraDT.hour
        hours_in_db.save()
        
        return JSONResponse(
            status_code=201,
            content={"message": 'Esferas registradas correctamente.'}
        )
    except Exception as e:
        LogsServices.write('-------- Error en Esferas --------')
        LogsServices.write(f'Error: {e}')
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )


@router.get('', response_model=List[EsferaResponseModel])
async def get_esferas():
    esferas = Esfera.select()
    return [ esfera for esfera in esferas ]