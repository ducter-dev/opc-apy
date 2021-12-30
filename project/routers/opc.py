from fastapi import APIRouter
from ..opc import OpcServices

router = APIRouter(prefix='/api/v1/opc')


@router.get('/entradasAntena')
async def opc_read():
    numPG = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.ANT_RFENT_NumPG')
    tipoPG = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.ANT_RFENT_TipoAT')
    return {
        'numAT': numPG,
        'tipoAT': tipoPG
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