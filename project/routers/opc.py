from multiprocessing.dummy import JoinableQueue
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..opc import OpcServices
from ..middlewares import VerifyTokenRoute

router = APIRouter(prefix='/api/v1/opc', route_class=VerifyTokenRoute)

# --------------- Antena de Entrada ---------------
@router.get('/antena/entrada')
async def read_antena_entrada():

    try:
        numPG = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.ANT_RFENT_NumPG')
        tipoPG = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.ANT_RFENT_TipoAT')

        return JSONResponse(
            status_code=200,
            content={
                'numAT': numPG,
                'tipoAT': tipoPG
            }
        )
    except:
        return JSONResponse(
            status_code=404,
            content={
                'message': 'Error, no se pueden leer los datos del OPC'
            }
        )


# --------------- Antena de Verificacion ---------------
@router.get('/antena/verificacion')
async def read_antena_verificacion():

    try:
        numPG = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.ANT_RFVER_NUMPG')
        tipoPG = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.ANT_RFVER_TIPOAT')

        return JSONResponse(
            status_code=200,
            content={
                'numAT': numPG,
                'tipoAT': tipoPG
            }
        )
    except:
        return JSONResponse(
            status_code=404,
            content={
                'message': 'Error, no se pueden leer los datos del OPC'
            }
        )


@router.post('/llenadera/folio/{value}')
async def opc_write(value: int):
    tag = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uLLEN01_FOLIO'
    valor = OpcServices.writeOPC(tag, value)
    return {
        'tag': tag,
        'valor': valor
    }

@router.get('/bombas/301A')
async def opc_read():
    status = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301A_STATUS')
    mode = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301A_MODE')
    time = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301A_TIME')
    return {
        'status': status,
        'mode': mode,
        'time': time
    }

@router.post('/llenadera/folio/{value}')
async def opc_write(value: int):
    tag = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uLLEN01_FOLIO'
    valor = OpcServices.writeOPC(tag, value)
    return {
        'tag': tag,
        'valor': valor
    }