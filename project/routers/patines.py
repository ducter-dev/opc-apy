from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime, timedelta
from ..funciones import obtenerFecha05Reporte, obtenerFecha24Reporte, obtenerTurno05, obtenerTurno24, get_clock

from ..database import PatinData, Bitacora, Horas
from ..schemas import PatinRequestModel, PatinResponseModel

from ..opc import OpcServices
from ..logs import LogsServices

from ..middlewares import VerifyTokenRoute
router = APIRouter(prefix='/api/v1/patines', route_class=VerifyTokenRoute)

@router.post('')
async def register_patin():
    try:
        LogsServices.write('----- Iniicando registro de patines ------')
        #   Primero obtenemos los valores de las variables
        ahora_json = await get_clock()
        ahora = ahora_json['fechaHora']
        ahoraDT = datetime.strptime(ahora, '%Y-%m-%d %H:%M:%S')
        hora = ahoraDT.strftime("%H")
        dateStr = ahoraDT.strftime("%Y-%m-%d")

        fecha05 = obtenerFecha05Reporte(ahoraDT.hour, dateStr)
        fecha24 = obtenerFecha24Reporte(ahoraDT.hour, dateStr)
        turno05 = obtenerTurno05(ahoraDT.hour)
        turno24 = obtenerTurno24(ahoraDT.hour)

        DI_401A_NAT_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.DI-401A_NAT_PROM')
        DI_401A_COR_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.DI-401A_COR_PROM')
        FI_401A_VOL_NAT_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401A_VOL_NAT_PROM_DEC')
        FI_401A_VOL_NAT_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401A_VOL_NAT_PROM_ENT')
        FI_401A_MASS_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401A_MASS_PROM_DEC')
        FI_401A_MASS_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401A_MASS_PROM_ENT')
        FQI_401A_MASS_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_MASS_DEC')
        FQI_401A_MASS_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_MASS_ENT')
        FQI_401A_TAM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAM_DEC')
        FQI_401A_TAM_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAM_UNI')
        FQI_401A_TAM_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAM_MIL')
        FQI_401A_TAM_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAM_BIL')
        FQI_401A_TAVC_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAVC_DEC')
        FQI_401A_TAVC_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAVC_UNI')
        FQI_401A_TAVC_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAVC_MIL')
        FQI_401A_TAVC_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAVC_BIL')
        FQI_401A_TAVN_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAVN_DEC')
        FQI_401A_TAVN_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAVN_UNI')
        FQI_401A_TAVN_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAVN_MIL')
        FQI_401A_TAVN_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_TAVN_BIL')
        FQI_401A_VOL_COR_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_VOL_COR_DEC')
        FQI_401A_VOL_COR_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_VOL_COR_ENT')
        FQI_401A_VOL_NAT_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_VOL_NAT_DEC')
        FQI_401A_VOL_NAT_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401A_VOL_NAT_ENT')
        PI_401A_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.PI-401A_PROM')
        TFM_401A_VOL_UNC_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TFM_401A_VOL_UNC_DEC')
        TFM_401A_VOL_UNC_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TFM_401A_VOL_UNC_ENT')
        TI_401A_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TI-401A_PROM')
        FI_401A_VOL_NAT_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401A_VOL_NAT_PROM_DEC')
        FI_401A_VOL_NAT_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401A_VOL_NAT_PROM_ENT')

        patin1 = PatinData.create(
            hora = f"{hora}:00",
            presion = PI_401A_PROM / 100,
            temperatura = TI_401A_PROM / 100,
            densidadNat = DI_401A_NAT_PROM / 10000,
            densidadCor =  DI_401A_COR_PROM / 10000,
            volUnc = TFM_401A_VOL_UNC_ENT + (TFM_401A_VOL_UNC_DEC / 10000),
            blsNat = FQI_401A_VOL_NAT_ENT + (FQI_401A_VOL_NAT_DEC / 10000),
            blsCor = FQI_401A_VOL_COR_ENT + (FQI_401A_VOL_COR_DEC / 10000),
            ton = FQI_401A_MASS_ENT + (FQI_401A_MASS_DEC / 10000),
            totalizadorBlsNat = (FQI_401A_TAVN_BIL * 100000000) + (FQI_401A_TAVN_MIL * 10000) + (FQI_401A_TAVN_UNI * 1) + (FQI_401A_TAVN_DEC / 1000),
            totalizadorBlsCor = (FQI_401A_TAVC_BIL * 100000000) + (FQI_401A_TAVC_MIL * 10000) + (FQI_401A_TAVC_UNI * 1) + (FQI_401A_TAVC_DEC / 1000),
            totalizadorMassTon = (FQI_401A_TAM_BIL * 100000000) + (FQI_401A_TAM_MIL * 10000) + (FQI_401A_TAM_UNI * 1) + (FQI_401A_TAM_DEC / 1000),
            flujoVolumen = FI_401A_VOL_NAT_PROM_ENT + (FI_401A_VOL_NAT_PROM_DEC / 100),
            flujoMasico = FI_401A_MASS_PROM_ENT + (FI_401A_MASS_PROM_DEC / 100),
            patin = 1,
            fecha = ahora,
            reporte05 =  fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        DI_401B_NAT_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.DI-401B_NAT_PROM')
        DI_401B_COR_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.DI-401B_COR_PROM')
        FI_401B_VOL_NAT_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401B_VOL_NAT_PROM_DEC')
        FI_401B_VOL_NAT_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401B_VOL_NAT_PROM_ENT')
        FI_401B_MASS_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401B_MASS_PROM_DEC')
        FI_401B_MASS_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401B_MASS_PROM_ENT')
        FQI_401B_MASS_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_MASS_DEC')
        FQI_401B_MASS_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_MASS_ENT')
        FQI_401B_TAM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAM_DEC')
        FQI_401B_TAM_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAM_UNI')
        FQI_401B_TAM_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAM_MIL')
        FQI_401B_TAM_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAM_BIL')
        FQI_401B_TAVC_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAVC_DEC')
        FQI_401B_TAVC_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAVC_UNI')
        FQI_401B_TAVC_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAVC_MIL')
        FQI_401B_TAVC_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAVC_BIL')
        FQI_401B_TAVN_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAVN_DEC')
        FQI_401B_TAVN_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAVN_UNI')
        FQI_401B_TAVN_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAVN_MIL')
        FQI_401B_TAVN_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_TAVN_BIL')
        FQI_401B_VOL_COR_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_VOL_COR_DEC')
        FQI_401B_VOL_COR_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_VOL_COR_ENT')
        FQI_401B_VOL_NAT_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_VOL_NAT_DEC')
        FQI_401B_VOL_NAT_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-401B_VOL_NAT_ENT')
        PI_401B_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.PI-401B_PROM')
        TFM_401B_VOL_UNC_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TFM_401B_VOL_UNC_DEC')
        TFM_401B_VOL_UNC_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TFM_401B_VOL_UNC_ENT')
        TI_401B_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TI-401B_PROM')
        FI_401B_VOL_NAT_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401B_VOL_NAT_PROM_DEC')
        FI_401B_VOL_NAT_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-401B_VOL_NAT_PROM_ENT')


        patin2 = PatinData.create(
            hora = f"{hora}:00",
            presion = PI_401B_PROM / 100,
            temperatura = TI_401B_PROM / 100,
            densidadNat = DI_401B_NAT_PROM / 10000,
            densidadCor =  DI_401B_COR_PROM / 10000,
            volUnc = TFM_401B_VOL_UNC_ENT + (TFM_401B_VOL_UNC_DEC / 10000),
            blsNat = FQI_401B_VOL_NAT_ENT + (FQI_401B_VOL_NAT_DEC / 10000),
            blsCor = FQI_401B_VOL_COR_ENT + (FQI_401B_VOL_COR_DEC / 10000),
            ton = FQI_401B_MASS_ENT + (FQI_401B_MASS_DEC / 10000),
            totalizadorBlsNat = (FQI_401B_TAVN_BIL * 100000000) + (FQI_401B_TAVN_MIL * 10000) + (FQI_401B_TAVN_UNI * 1) + (FQI_401B_TAVN_DEC / 1000),
            totalizadorBlsCor = (FQI_401B_TAVC_BIL * 100000000) + (FQI_401B_TAVC_MIL * 10000) + (FQI_401B_TAVC_UNI * 1) + (FQI_401B_TAVC_DEC / 1000),
            totalizadorMassTon = (FQI_401B_TAM_BIL * 100000000) + (FQI_401B_TAM_MIL * 10000) + (FQI_401B_TAM_UNI * 1) + (FQI_401B_TAM_DEC / 1000),
            flujoVolumen = FI_401B_VOL_NAT_PROM_ENT + (FI_401B_VOL_NAT_PROM_DEC / 100),
            flujoMasico = FI_401B_MASS_PROM_ENT + (FI_401B_MASS_PROM_DEC / 100),
            patin = 2,
            fecha = ahora,
            reporte05 =  fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )
        
        DI_402A_NAT_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.DI-402A_NAT_PROM')
        DI_402A_COR_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.DI-402A_COR_PROM')
        FI_402A_VOL_NAT_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402A_VOL_NAT_PROM_DEC')
        FI_402A_VOL_NAT_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402A_VOL_NAT_PROM_ENT')
        FI_402A_MASS_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402A_MASS_PROM_DEC')
        FI_402A_MASS_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402A_MASS_PROM_ENT')
        FQI_402A_MASS_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_MASS_DEC')
        FQI_402A_MASS_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_MASS_ENT')
        FQI_402A_TAM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAM_DEC')
        FQI_402A_TAM_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAM_UNI')
        FQI_402A_TAM_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAM_MIL')
        FQI_402A_TAM_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAM_BIL')
        FQI_402A_TAVC_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAVC_DEC')
        FQI_402A_TAVC_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAVC_UNI')
        FQI_402A_TAVC_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAVC_MIL')
        FQI_402A_TAVC_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAVC_BIL')
        FQI_402A_TAVN_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAVN_DEC')
        FQI_402A_TAVN_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAVN_UNI')
        FQI_402A_TAVN_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAVN_MIL')
        FQI_402A_TAVN_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_TAVN_BIL')
        FQI_402A_VOL_COR_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_VOL_COR_DEC')
        FQI_402A_VOL_COR_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_VOL_COR_ENT')
        FQI_402A_VOL_NAT_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_VOL_NAT_DEC')
        FQI_402A_VOL_NAT_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402A_VOL_NAT_ENT')
        PI_402A_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.PI-402A_PROM')
        TFM_402A_VOL_UNC_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TFM_402A_VOL_UNC_DEC')
        TFM_402A_VOL_UNC_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TFM_402A_VOL_UNC_ENT')
        TI_402A_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TI-402A_PROM')
        FI_402A_VOL_NAT_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402A_VOL_NAT_PROM_DEC')
        FI_402A_VOL_NAT_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402A_VOL_NAT_PROM_ENT')


        patin3 = PatinData.create(
            hora = f"{hora}:00",
            presion = PI_402A_PROM / 100,
            temperatura = TI_402A_PROM / 100,
            densidadNat = DI_402A_NAT_PROM / 10000,
            densidadCor =  DI_402A_COR_PROM / 10000,
            volUnc = TFM_402A_VOL_UNC_ENT + (TFM_402A_VOL_UNC_DEC / 10000),
            blsNat = FQI_402A_VOL_NAT_ENT + (FQI_402A_VOL_NAT_DEC / 10000),
            blsCor = FQI_402A_VOL_COR_ENT + (FQI_402A_VOL_COR_DEC / 10000),
            ton = FQI_402A_MASS_ENT + (FQI_402A_MASS_DEC / 10000),
            totalizadorBlsNat = (FQI_402A_TAVN_BIL * 100000000) + (FQI_402A_TAVN_MIL * 10000) + (FQI_402A_TAVN_UNI * 1) + (FQI_402A_TAVN_DEC / 1000),
            totalizadorBlsCor = (FQI_402A_TAVC_BIL * 100000000) + (FQI_402A_TAVC_MIL * 10000) + (FQI_402A_TAVC_UNI * 1) + (FQI_402A_TAVC_DEC / 1000),
            totalizadorMassTon = (FQI_402A_TAM_BIL * 100000000) + (FQI_402A_TAM_MIL * 10000) + (FQI_402A_TAM_UNI * 1) + (FQI_402A_TAM_DEC / 1000),
            flujoVolumen = FI_402A_VOL_NAT_PROM_ENT + (FI_402A_VOL_NAT_PROM_DEC / 100),
            flujoMasico = FI_402A_MASS_PROM_ENT + (FI_402A_MASS_PROM_DEC / 100),
            patin = 3,
            fecha = ahora,
            reporte05 =  fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )
        
        DI_402B_NAT_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.DI-402B_NAT_PROM')
        DI_402B_COR_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.DI-402B_COR_PROM')
        FI_402B_VOL_NAT_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402B_VOL_NAT_PROM_DEC')
        FI_402B_VOL_NAT_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402B_VOL_NAT_PROM_ENT')
        FI_402B_MASS_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402B_MASS_PROM_DEC')
        FI_402B_MASS_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402B_MASS_PROM_ENT')
        FQI_402B_MASS_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_MASS_DEC')
        FQI_402B_MASS_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_MASS_ENT')
        FQI_402B_TAM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAM_DEC')
        FQI_402B_TAM_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAM_UNI')
        FQI_402B_TAM_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAM_MIL')
        FQI_402B_TAM_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAM_BIL')
        FQI_402B_TAVC_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAVC_DEC')
        FQI_402B_TAVC_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAVC_UNI')
        FQI_402B_TAVC_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAVC_MIL')
        FQI_402B_TAVC_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAVC_BIL')
        FQI_402B_TAVN_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAVN_DEC')
        FQI_402B_TAVN_UNI = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAVN_UNI')
        FQI_402B_TAVN_MIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAVN_MIL')
        FQI_402B_TAVN_BIL = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_TAVN_BIL')
        FQI_402B_VOL_COR_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_VOL_COR_DEC')
        FQI_402B_VOL_COR_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_VOL_COR_ENT')
        FQI_402B_VOL_NAT_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_VOL_NAT_DEC')
        FQI_402B_VOL_NAT_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FQI-402B_VOL_NAT_ENT')
        PI_402B_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.PI-402B_PROM')
        TFM_402B_VOL_UNC_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TFM_402B_VOL_UNC_DEC')
        TFM_402B_VOL_UNC_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TFM_402B_VOL_UNC_ENT')
        TI_402B_PROM = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.TI-402B_PROM')
        FI_402B_VOL_NAT_PROM_DEC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402B_VOL_NAT_PROM_DEC')
        FI_402B_VOL_NAT_PROM_ENT = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Patines.FI-402B_VOL_NAT_PROM_ENT')

        patin4 = PatinData.create(
            hora = f"{hora}:00",
            presion = PI_402B_PROM / 100,
            temperatura = TI_402B_PROM / 100,
            densidadNat = DI_402B_NAT_PROM / 10000,
            densidadCor =  DI_402B_COR_PROM / 10000,
            volUnc = TFM_402B_VOL_UNC_ENT + (TFM_402B_VOL_UNC_DEC / 10000),
            blsNat = FQI_402B_VOL_NAT_ENT + (FQI_402B_VOL_NAT_DEC / 10000),
            blsCor = FQI_402B_VOL_COR_ENT + (FQI_402B_VOL_COR_DEC / 10000),
            ton = FQI_402B_MASS_ENT + (FQI_402B_MASS_DEC / 10000),
            totalizadorBlsNat = (FQI_402B_TAVN_BIL * 100000000) + (FQI_402B_TAVN_MIL * 10000) + (FQI_402B_TAVN_UNI * 1) + (FQI_402B_TAVN_DEC / 1000),
            totalizadorBlsCor = (FQI_402B_TAVC_BIL * 100000000) + (FQI_402B_TAVC_MIL * 10000) + (FQI_402B_TAVC_UNI * 1) + (FQI_402B_TAVC_DEC / 1000),
            totalizadorMassTon = (FQI_402B_TAM_BIL * 100000000) + (FQI_402B_TAM_MIL * 10000) + (FQI_402B_TAM_UNI * 1) + (FQI_402B_TAM_DEC / 1000),
            flujoVolumen = FI_402B_VOL_NAT_PROM_ENT + (FI_402B_VOL_NAT_PROM_DEC / 100),
            flujoMasico = FI_402B_MASS_PROM_ENT + (FI_402B_MASS_PROM_DEC / 100),
            patin = 4,
            fecha = ahora,
            reporte05 =  fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        hours_in_db = Horas.select().where(Horas.id == 2).first()
        hours_in_db.hora = ahoraDT.hour
        hours_in_db.save()

        bitacora = Bitacora.create(
            user = 1,
            evento = 9,
            actividad = 'Patines registrados correctamente.',
            fecha = ahora,
            reporte24 = fecha24,
            reporte05 = fecha05
        )
        
        return JSONResponse(
            status_code=201,
            content={"message": 'Patines registrados correctamente.'}
        )
    except Exception as e:
        LogsServices.write('-------- Error en Patines --------')
        LogsServices.write(f'Error: {e}')
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )


@router.get('', response_model=List[PatinResponseModel])
async def get_patines():
    patines = PatinData.select()
    return [ patin for patin in patines ]