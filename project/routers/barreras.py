from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..schemas import BarreraRequesteModel

from ..middlewares import VerifyTokenRoute

from ..opc import OpcServices

router = APIRouter(prefix='/api/v1/barrera', route_class=VerifyTokenRoute)

@router.post('/entrada')
async def post_changeBarreraEntrada(request: BarreraRequesteModel):
    # 2 = Abrir barrera de entrada
    # 1 = Cerrar barrera de entrada
    try:
        estadoInt = 2 if request.estado == True else 1
        OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_ENT', estadoInt)
        barrera = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_ENT')
        if barrera is None:
            return JSONResponse(
                status_code=501,
                content={"message": 'No hay comunicación con la barrera de entrada'}
            )
        #estado = 1
        estadoVal = True if barrera == 2 else False
        return JSONResponse(
            status_code=201,
            content={"estado": estadoVal }
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )

@router.get('/entrada')
async def get_getBarreraEntrada():
    try:
        barrera = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_ENT')
        #barrera = 1
        if barrera is None:
            return JSONResponse(
                status_code=501,
                content={"message": 'No hay comunicación con la barrera de entrada'}
            )
        estado = True if barrera == 2 else False
        return JSONResponse(
            status_code=200,
            content={"estado": estado}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )

@router.post('/verificacion')
async def post_changeBarreraVerificacion(request: BarreraRequesteModel):
    # 1 = Abrir barrera de Verificacion
    # 2 = Cerrar barrera de Verificacion
    try:
        estadoInt = 2 if request.estado == True else 1
        OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_VER', estadoInt)
        barrera = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_VER')
        #barrera = 1
        if barrera is None:
            return JSONResponse(
                status_code=501,
                content={"message": 'No hay comunicación con la barrera de verificación'}
            )
        estado = True if barrera == 1 else False
        return JSONResponse(
            status_code=201,
            content={"estado": estado}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )

@router.get('/verificacion')
async def get_getBarreraVerificacion():
    try:
        barrera = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_VER')
        #barrera = 1
        if barrera is None:
            return JSONResponse(
                status_code=501,
                content={"message": 'No hay comunicación con la barrera de verificación'}
            )
        estado = True if barrera == 1 else False
        return JSONResponse(
            status_code=200,
            content={"estado": estado}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )


@router.post('/salida')
async def post_changeBarreraSalida(request: BarreraRequesteModel):
    # 1 = Abrir barrera de salida
    # 2 = Cerrar barrera de salida
    try:
        estadoInt = 2 if request.estado == True else 1
        OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_SAL', estadoInt)
        barrera = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_SAL')
        #barrera = 1
        if barrera is None:
            return JSONResponse(
                status_code=501,
                content={"message": 'No hay comunicación con la barrera de salida'}
            )
        estado = True if barrera == 1 else False
        return JSONResponse(
            status_code=201,
            content={"estado": estado}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )

@router.get('/salida')
async def get_getBarreraSalida():
    try:
        barrera = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_SAL')
        #barrera = 1
        if barrera is None:
            return JSONResponse(
                status_code=501,
                content={"message": 'No hay comunicación con la barrera de salida'}
            )
        estado = True if barrera == 1 else False
        return JSONResponse(
            status_code=200,
            content={"estado": estado}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )
