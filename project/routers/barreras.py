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
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_ENT', barrera_request.value)
        estado = "abierta" if request.estado == 1 else "cerrada"
        return JSONResponse(
            status_code=201,
            content={"message": f'La barrera de entrada ha sido {estado}'}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )

@router.get('/entrada')
async def get_getBarreraEntrada():
    try:
        #barrera = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_ENT')
        barrera = 1
        estado = "abierta" if barrera == 1 else "cerrada"
        return JSONResponse(
            status_code=201,
            content={"message": f"La barrera de entrada tiene estado: {estado}"}
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
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_VER', barrera_request.value)
        estado = "abierta" if request.estado == 1 else "cerrada"
        return JSONResponse(
            status_code=201,
            content={"message": f'La barrera de verificacion ha sido {estado}'}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )

@router.get('/verificacion')
async def get_getBarreraVerificacion():
    try:
        #barrera = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_VER')
        barrera = 1
        estado = "abierta" if barrera == 1 else "cerrada"
        return JSONResponse(
            status_code=201,
            content={"message": f"La barrera de verificacion tiene estado: {estado}"}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )

# 
# GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.CIERRA_BAR_SAL