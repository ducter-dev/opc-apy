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
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
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
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )


# --------------- Antena de Salida ---------------
@router.get('/antena/salida')
async def read_antena_salida():

    try:
        numPG = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.ANT_RFSAL_NUMPG')
        tipoPG = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.ANT_RFSAL_TIPOAT')
        
        return JSONResponse(
            status_code=200,
            content={
                'numAT': numPG,
                'tipoAT': tipoPG
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
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


@router.get('/reloj')
async def get_clock_delta():
    year = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Year')
    monthOPC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Month')
    dayOPC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Day')
    hourOPC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Hours')
    minuteOPC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Mins')
    secondOPC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Secs')

    month = convertIntToTimeString(monthOPC)
    day = convertIntToTimeString(dayOPC)
    hour = convertIntToTimeString(hourOPC)
    minute = convertIntToTimeString(minuteOPC)
    second = convertIntToTimeString(secondOPC)


    fecha_hora = f'{year}-{month}-{day} {hour}:{minute}:{second}'
    return {
        'fechaHora': fecha_hora
    }


def convertIntToTimeString(number):

    if number < 10:
        return f'0{number}'
    else:
        return f'{number}'