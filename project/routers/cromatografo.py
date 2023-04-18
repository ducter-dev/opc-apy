from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime, timedelta
from ..funciones import obtenerFecha05Reporte, obtenerFecha24Reporte, obtenerTurno05, obtenerTurno24

from ..database import Cromatografo, Bitacora
from ..schemas import CromatografoResponseModel

from ..opc import OpcServices

from ..middlewares import VerifyTokenRoute
router = APIRouter(prefix='/api/v1/cromatografo', route_class=VerifyTokenRoute)


@router.post('')
async def register_cromatografo():
    try:
        now = datetime.now()
        ahora = now.strftime("%Y:%m-%d %H:%M:%S")
        hora = now.strftime("%H")
        fecha05 = obtenerFecha05Reporte()
        fecha24 = obtenerFecha24Reporte()
        turno05 = obtenerTurno05(int(hora))
        turno24 = obtenerTurno24(int(hora))

        C6_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.C6_IRGE')
        PROPANO_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PROPANO_IRGE')
        PROPILENO_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.PROPILENO_IRGE')
        IBUTANO_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.IBUTANO_IRGE')
        NBUTANO_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.NBUTANO_IRGE')
        C4_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.C4_IRGE')
        IPENTANO_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.IPENTANO_IRGE')
        NPENTANO_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.NPENTANO_IRGE')
        METANO_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.METANO_IRGE')
        ETILENO_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.ETILENO_IRGE')
        ETANO_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.ETANO_IRGE')
        OLEFINAS_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.OLEFINAS_IRGE')
        DENSIDAD_IRGE = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Cromatografia.DENSIDAD_IRGE')

        cromatografo1 = Cromatografo.create(
            hora = f"{hora}:00",
            cromatografo = 'IRGE',
            corriente = 1,
            c6 = C6_IRGE / 100,
            propano = PROPANO_IRGE / 100,
            propileno = PROPILENO_IRGE / 100,
            iButano = IBUTANO_IRGE / 100,
            nButano = NBUTANO_IRGE / 100,
            c4 = C4_IRGE / 100,
            iPentano = IPENTANO_IRGE / 100,
            nPentano = NPENTANO_IRGE / 100,
            metano = METANO_IRGE / 100,
            etileno = ETILENO_IRGE / 100,
            etano = ETANO_IRGE / 100,
            olefinas = OLEFINAS_IRGE / 100,
            densidad = DENSIDAD_IRGE / 10000,
            pentano = (IPENTANO_IRGE / 100) + (NPENTANO_IRGE / 100),
            fecha = ahora,
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
            content={"message": 'Cromatografo registrados correctamente.'}
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )