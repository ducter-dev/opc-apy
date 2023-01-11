from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..schemas import BarreraRequesteModel

from ..middlewares import VerifyTokenRoute

from ..opc import OpcServices

router = APIRouter(prefix='/api/v1/barrera', route_class=VerifyTokenRoute)

@router.post('/entrada')
async def post_changeBarreraEntrada(request: BarreraRequesteModel):
    # 1 = Abrir barrera de entrada
    # 2 = Cerrar barrera de entrada
    try:
        estado = OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_ENT', request.estado)
        estadoVal = True if estado == 1 else False
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
        estado = True if barrera == 1 else False
        return JSONResponse(
            status_code=201,
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
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_VER', request.estado)
        estado = True if request.estado == 1 else False
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
        estado = True if barrera == 1 else False
        return JSONResponse(
            status_code=201,
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
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_SAL', request.estado)
        estado = True if request.estado == 1 else False
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
        #barrera = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_SAL')
        barrera = 2
        estado = True if barrera == 1 else False
        return JSONResponse(
            status_code=201,
            content={"estado": estado}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )
