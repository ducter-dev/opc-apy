from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime, timedelta
from ..funciones import obtenerFecha05Reporte, obtenerFecha24Reporte, obtenerTurno05, obtenerTurno24, get_clock

from ..database import Cromatografo, Bitacora, Densidad, Horas
from ..schemas import CromatografoResponseModel, DensidadResponseModel

from ..opc import OpcServices
from ..logs import LogsServices

from ..middlewares import VerifyTokenRoute
router = APIRouter(prefix='/api/v1/cromatografo', route_class=VerifyTokenRoute)


TE_301A_REGISTRO_SPARE_3 = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.TE_301A_REGISTRO_SPARE_3'
TE_301B_REGISTRO_SPARE_3 = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.TE_301B_REGISTRO_SPARE_3'
PRES_PI_301A = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.PRES_PI_301A'
PRES_PI_301B = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.PRES_PI_301B'
DENS_DI_NAT_301A = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.DENS_DI_NAT_301A'
DENS_DI_NAT_301B = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Esferas.DENS_DI_NAT_301B'
PODER_CALOR = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PODER_CALOR'
DENSIDAD_IRGE = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.DENSIDAD_IRGE'
ETANO_IRGE = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.ETANO_IRGE'
METANO_IRGE = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.METANO_IRGE'
PROPANO_IRGE = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PROPANO_IRGE'
IBUTANO_IRGE = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.IBUTANO_IRGE'
NBUTANO_IRGE = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.NBUTANO_IRGE'
IPENTANO_IRGE = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.IPENTANO_IRGE'
NPENTANO_IRGE = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.NPENTANO_IRGE'
PROPILENO_IRGE = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PROPILENO_IRGE'
C4_IRGE = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.C4_IRGE'
DENS_ETANO_60 = 0.355994
DENS_METANO_60 = 0.42236
DENS_PROPANO_60 = 0.507025
DENS_I_BUTANO_60 = 0.562827
DENS_N_BUTANO_60 = 0.584127
DENS_I_PENTANO_60 = 0.624285
DENS_N_PENTANO_60 = 0.631054
DENS_PROPILENO_60 = 0.70053
DENS_1_BUTENO_60 = 0.62562

@router.post('')
async def register_cromatografo():
    try:
        LogsServices.write('----- Iniicando registro de croma ------')
        ahora_json = await get_clock()
        ahora = ahora_json['fechaHora']
        ahoraDT = datetime.strptime(ahora, '%Y-%m-%d %H:%M:%S')
        hora = ahoraDT.strftime("%H")
        dateStr = ahoraDT.strftime("%Y-%m-%d")
        fecha05 = obtenerFecha05Reporte(ahoraDT.hour, dateStr)
        fecha24 = obtenerFecha24Reporte(ahoraDT.hour, dateStr)
        turno05 = obtenerTurno05(ahoraDT.hour)
        turno24 = obtenerTurno24(ahoraDT.hour)

        c6_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.C6_IRGE')
        pROPANO_IRGE = OpcServices.readDataPLC(PROPANO_IRGE)
        pROPILENO_IRGE = OpcServices.readDataPLC(PROPILENO_IRGE)
        iBUTANO_IRGE = OpcServices.readDataPLC(IBUTANO_IRGE)
        nBUTANO_IRGE = OpcServices.readDataPLC(NBUTANO_IRGE)
        c4_IRGE = OpcServices.readDataPLC(C4_IRGE)
        iPENTANO_IRGE = OpcServices.readDataPLC(IPENTANO_IRGE)
        nPENTANO_IRGE = OpcServices.readDataPLC(NPENTANO_IRGE)
        mETANO_IRGE = OpcServices.readDataPLC(METANO_IRGE)
        eTILENO_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.ETILENO_IRGE')
        eTANO_IRGE = OpcServices.readDataPLC(ETANO_IRGE)
        oLEFINAS_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.OLEFINAS_IRGE')
        dENSIDAD_IRGE = OpcServices.readDataPLC(DENSIDAD_IRGE)
        """ LogsServices.write(f'C6_IRGE: {c6_IRGE}')
        LogsServices.write(f'PROPANO_IRGE: {pROPANO_IRGE}')
        LogsServices.write(f'PROPILENO_IRGE: {pROPILENO_IRGE}')
        LogsServices.write(f'IBUTANO_IRGE: {iBUTANO_IRGE}')
        LogsServices.write(f'NBUTANO_IRGE: {nBUTANO_IRGE}')
        LogsServices.write(f'C4_IRGE: {c4_IRGE}')
        LogsServices.write(f'IPENTANO_IRGE: {iPENTANO_IRGE}')
        LogsServices.write(f'NPENTANO_IRGE: {nPENTANO_IRGE}')
        LogsServices.write(f'METANO_IRGE: {mETANO_IRGE}')
        LogsServices.write(f'ETILENO_IRGE: {eTILENO_IRGE}')
        LogsServices.write(f'ETANO_IRGE: {eTANO_IRGE}')
        LogsServices.write(f'OLEFINAS_IRGE: {oLEFINAS_IRGE}')
        LogsServices.write(f'DENSIDAD_IRGE: {dENSIDAD_IRGE}') """


        cromatografo1 = Cromatografo.create(
            hora = f"{hora}:00",
            cromatografo = 'IRGE',
            corriente = 1,
            c6 = c6_IRGE / 100,
            propano = pROPANO_IRGE / 100,
            propileno = pROPILENO_IRGE / 100,
            iButano = iBUTANO_IRGE / 100,
            nButano = nBUTANO_IRGE / 100,
            c4 = c4_IRGE / 100,
            iPentano = iPENTANO_IRGE / 100,
            nPentano = nPENTANO_IRGE / 100,
            metano = mETANO_IRGE / 100,
            etileno = eTILENO_IRGE / 100,
            etano = eTANO_IRGE / 100,
            olefinas = oLEFINAS_IRGE / 100,
            densidad = dENSIDAD_IRGE / 10000,
            pentano = (iPENTANO_IRGE / 100) + (nPENTANO_IRGE / 100),
            reporte05 = fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        C6_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.C6_EB4_STR1')
        PROPANO_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PROPANO_EB4_STR1')
        PROPILENO_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PROPILENO_EB4_STR1')
        IBUTANO_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.IBUTANO_EB4_STR1')
        NBUTANO_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.NBUTANO_EB4_STR1')
        C4_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.C4_EB4_STR1')
        IPENTANO_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.IPENTANO_EB4_STR1')
        NPENTANO_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.NPENTANO_EB4_STR1')
        METANO_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.METANO_EB4_STR1')
        ETILENO_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.ETILENO_EB4_STR1')
        ETANO_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.ETANO_EB4_STR1')
        OLEFINAS_EB4_STR1 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.OLEFINAS_EB4_STR1')
        cromatografo2 = Cromatografo.create(
            hora = f"{hora}:00",
            cromatografo = 'EB04',
            corriente = 1,
            c6 = C6_EB4_STR1 / 100,
            propano = PROPANO_EB4_STR1 / 100,
            propileno = PROPILENO_EB4_STR1 / 100,
            iButano = IBUTANO_EB4_STR1 / 100,
            nButano = NBUTANO_EB4_STR1 / 100,
            c4 = C4_EB4_STR1 / 100,
            iPentano = IPENTANO_EB4_STR1 / 100,
            nPentano = NPENTANO_EB4_STR1 / 100,
            metano = METANO_EB4_STR1 / 100,
            etileno = ETILENO_EB4_STR1 / 100,
            etano = ETANO_EB4_STR1 / 100,
            olefinas = OLEFINAS_EB4_STR1 / 100,
            fecha = ahora,
            reporte05 = fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        C6_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.C6_EB4_STR2')
        PROPANO_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PROPANO_EB4_STR2')
        PROPILENO_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PROPILENO_EB4_STR2')
        IBUTANO_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.IBUTANO_EB4_STR2')
        NBUTANO_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.NBUTANO_EB4_STR2')
        C4_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.C4_EB4_STR2')
        IPENTANO_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.IPENTANO_EB4_STR2')
        NPENTANO_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.NPENTANO_EB4_STR2')
        METANO_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.METANO_EB4_STR2')
        ETILENO_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.ETILENO_EB4_STR2')
        ETANO_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.ETANO_EB4_STR2')
        OLEFINAS_EB4_STR2 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.OLEFINAS_EB4_STR2')

        cromatografo3 = Cromatografo.create(
            hora = f"{hora}:00",
            cromatografo = 'EB04',
            corriente = 2,
            c6 = C6_EB4_STR2 / 100,
            propano = PROPANO_EB4_STR2 / 100,
            propileno = PROPILENO_EB4_STR2 / 100,
            iButano = IBUTANO_EB4_STR2 / 100,
            nButano = NBUTANO_EB4_STR2 / 100,
            c4 = C4_EB4_STR2 / 100,
            iPentano = IPENTANO_EB4_STR2 / 100,
            nPentano = NPENTANO_EB4_STR2 / 100,
            metano = METANO_EB4_STR2 / 100,
            etileno = ETILENO_EB4_STR2 / 100,
            etano = ETANO_EB4_STR2 / 100,
            olefinas = OLEFINAS_EB4_STR2 / 100,
            fecha = ahora,
            reporte05 = fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        C6_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.C6_EB4_STR3')
        PROPANO_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PROPANO_EB4_STR3')
        PROPILENO_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PROPILENO_EB4_STR3')
        IBUTANO_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.IBUTANO_EB4_STR3')
        NBUTANO_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.NBUTANO_EB4_STR3')
        C4_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.C4_EB4_STR3')
        IPENTANO_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.IPENTANO_EB4_STR3')
        NPENTANO_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.NPENTANO_EB4_STR3')
        METANO_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.METANO_EB4_STR3')
        ETILENO_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.ETILENO_EB4_STR3')
        ETANO_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.ETANO_EB4_STR3')
        OLEFINAS_EB4_STR3 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.OLEFINAS_EB4_STR3')

        cromatografo4 = Cromatografo.create(
            hora = f"{hora}:00",
            cromatografo = 'EB04',
            corriente = 3,
            c6 = C6_EB4_STR3 / 100,
            propano = PROPANO_EB4_STR3 / 100,
            propileno = PROPILENO_EB4_STR3 / 100,
            iButano = IBUTANO_EB4_STR3 / 100,
            nButano = NBUTANO_EB4_STR3 / 100,
            c4 = C4_EB4_STR3 / 100,
            iPentano = IPENTANO_EB4_STR3 / 100,
            nPentano = NPENTANO_EB4_STR3 / 100,
            metano = METANO_EB4_STR3 / 100,
            etileno = ETILENO_EB4_STR3 / 100,
            etano = ETANO_EB4_STR3 / 100,
            olefinas = OLEFINAS_EB4_STR3 / 100,
            fecha = ahora,
            reporte05 = fecha05,
            turno05 = turno05,
            reporte24 = fecha24,
            turno24 = turno24
        )

        hours_in_db = Horas.select().where(Horas.id == 3).first()
        hours_in_db.hora = ahoraDT.hour
        hours_in_db.save()
        
        bitacora = Bitacora.create(
            user = 1,
            evento = 9,
            actividad = 'Cromotógrafo registrado correctamente.',
            fecha = ahora,
            reporte24 = fecha24,
            reporte05 = fecha05
        )
        
        return JSONResponse(
            status_code=201,
            content={"message": 'Cromatografo registrado correctamente.'}
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )
    

@router.post('/densidades', response_model= DensidadResponseModel)
async def register_densidad():
    try:
        LogsServices.write(f'-----Iniciando Registro ---- de Densidades')
        ahora_json = await get_clock()
        ahora = ahora_json['fechaHora']
        ahoraDT = datetime.strptime(ahora, '%Y-%m-%d %H:%M:%S')
        hora = ahoraDT.strftime("%H")
        dateStr = ahoraDT.strftime("%Y-%m-%d")
        fecha05 = obtenerFecha05Reporte(ahoraDT.hour, dateStr)
        fecha24 = obtenerFecha24Reporte(ahoraDT.hour, dateStr)
        # leer variables 
        preSupEsf1 = OpcServices.readDataPLC(TE_301A_REGISTRO_SPARE_3) / 100
        preSupEsf2 = OpcServices.readDataPLC(TE_301B_REGISTRO_SPARE_3) / 100
        preInfEsf1 = OpcServices.readDataPLC(PRES_PI_301A) / 100
        preInfEsf2 = OpcServices.readDataPLC(PRES_PI_301B) / 100
        densNatEsf1 = OpcServices.readDataPLC(DENS_DI_NAT_301A) / 10000
        densNatEsf2 = OpcServices.readDataPLC(DENS_DI_NAT_301B) / 10000
        densitometro = OpcServices.readDataPLC(PODER_CALOR) / 10000
        cromatografo = OpcServices.readDataPLC(DENSIDAD_IRGE) / 10000
        """ LogsServices.write(f'preSupEsf1: {preSupEsf1}')
        LogsServices.write(f'preSupEsf2: {preSupEsf2}')
        LogsServices.write(f'preInfEsf1: {preInfEsf1}')
        LogsServices.write(f'preInfEsf2: {preInfEsf2}')
        LogsServices.write(f'densNatEsf1: {densNatEsf1}')
        LogsServices.write(f'densNatEsf2: {densNatEsf2}')
        LogsServices.write(f'densitometro: {densitometro}')
        LogsServices.write(f'cromatografo: {cromatografo}') """
        
        # datos para analisis
        eTANO_IRGE = OpcServices.readDataPLC(ETANO_IRGE)
        mETANO_IRGE = OpcServices.readDataPLC(METANO_IRGE)
        pROPANO_IRGE = OpcServices.readDataPLC(PROPANO_IRGE)
        iBUTANO_IRGE = OpcServices.readDataPLC(IBUTANO_IRGE)
        nBUTANO_IRGE = OpcServices.readDataPLC(NBUTANO_IRGE)
        iPENTANO_IRGE = OpcServices.readDataPLC(IPENTANO_IRGE)
        nPENTANO_IRGE = OpcServices.readDataPLC(NPENTANO_IRGE)
        pROPILENO_IRGE = OpcServices.readDataPLC(PROPILENO_IRGE)
        c4_IRGE = OpcServices.readDataPLC(C4_IRGE)
        """ LogsServices.write(f'eTANO_IRGE: {eTANO_IRGE}')
        LogsServices.write(f'mETANO_IRGE: {mETANO_IRGE}')
        LogsServices.write(f'pROPANO_IRGE: {pROPANO_IRGE}')
        LogsServices.write(f'iBUTANO_IRGE: {iBUTANO_IRGE}')
        LogsServices.write(f'nBUTANO_IRGE: {nBUTANO_IRGE}')
        LogsServices.write(f'iPENTANO_IRGE: {iPENTANO_IRGE}')
        LogsServices.write(f'nPENTANO_IRGE: {nPENTANO_IRGE}')
        LogsServices.write(f'pROPILENO_IRGE: {pROPILENO_IRGE}')
        LogsServices.write(f'c4_IRGE: {c4_IRGE}') """
        

        analisisCrom = (eTANO_IRGE / 10000) * DENS_ETANO_60
        #analisisCrom = (analisisCrom + (mETANO_IRGE) / 10000) * DENS_METANO_60
        #analisisCrom = (analisisCrom + (pROPANO_IRGE) / 10000) * DENS_PROPANO_60
        #analisisCrom = (analisisCrom + (iBUTANO_IRGE) / 10000) * DENS_I_BUTANO_60
        #analisisCrom = (analisisCrom + (nBUTANO_IRGE) / 10000) * DENS_N_BUTANO_60
        #analisisCrom = (analisisCrom + (iPENTANO_IRGE) / 10000) * DENS_I_PENTANO_60
        #analisisCrom = (analisisCrom + (nPENTANO_IRGE) / 10000) * DENS_N_PENTANO_60
        #analisisCrom = (analisisCrom + (pROPILENO_IRGE) / 10000) * DENS_PROPILENO_60
        #analisisCrom = (analisisCrom + (c4_IRGE) / 10000) * DENS_1_BUTENO_60

        analisisCrom = analisisCrom + ((mETANO_IRGE) / 10000) * DENS_METANO_60
        analisisCrom = analisisCrom + ((pROPANO_IRGE) / 10000) * DENS_PROPANO_60
        analisisCrom = analisisCrom + ((iBUTANO_IRGE) / 10000) * DENS_I_BUTANO_60
        analisisCrom = analisisCrom + ((nBUTANO_IRGE) / 10000) * DENS_N_BUTANO_60
        analisisCrom = analisisCrom + ((iPENTANO_IRGE) / 10000) * DENS_I_PENTANO_60
        analisisCrom = analisisCrom + ((nPENTANO_IRGE) / 10000) * DENS_N_PENTANO_60
        analisisCrom = analisisCrom + ((pROPILENO_IRGE) / 10000) * DENS_PROPILENO_60
        analisisCrom = analisisCrom + ((c4_IRGE) / 10000) * DENS_1_BUTENO_60
        # registrar dats

        LogsServices.write(f'analisisCrom: {analisisCrom}')

        densidadSaved = Densidad.create(
            hora = hora,
            presSupEsf1 = preSupEsf1,
            presInfEsf1 = preInfEsf1,
            presSupEsf2 = preSupEsf2,
            presInfEsf2 = preInfEsf2,
            densNatEsf1 = densNatEsf1,
            densNatEsf2 = densNatEsf2,
            densitometro = densitometro,
            cromatografo = cromatografo,
            analisisCrom = analisisCrom,
            reporte05 = fecha05,
            reporte24 = fecha24
        )

        
        hours_in_db = Horas.select().where(Horas.id == 5).first()
        hours_in_db.hora = ahoraDT.hour
        hours_in_db.save()

        return JSONResponse(
            status_code=201,
            content={"message": "Densidades registradas correctamente."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )