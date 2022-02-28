from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from project.opc import OpcServices

from ..database import Llenadera
from ..schemas import LlenaderaRequestModel, LlenaderaResponseModel, EstadoLlenaderaRequesteModel, NumeroLlenaderaRequesteModel

from ..middlewares import VerifyTokenRoute

router = APIRouter(prefix='/api/v1/llenaderas', route_class=VerifyTokenRoute)

@router.post('', response_model=LlenaderaResponseModel)
async def create_llenadera(llenadera:LlenaderaRequestModel):
    tank = Llenadera.create(
        numero = llenadera.numero,
        conector = llenadera.conector,
        tipo = llenadera.tipo,
    )

    return tank


@router.get('', response_model=List[LlenaderaResponseModel])
async def get_llenaderas():
    llenaderas = Llenadera.select()
    return [ llenadera for llenadera in llenaderas ]


@router.put('/{llenadera_id}', response_model=LlenaderaResponseModel)
async def edit_llenadera(llenadera_id: int, llenadera_request: LlenaderaRequestModel):
    llenadera = Llenadera.select().where(Llenadera.id == llenadera_id).first()
    if llenadera is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Llenadera no encontrada"}
        )

    llenadera.numero = llenadera_request.numero
    llenadera.conector = llenadera_request.conector
    llenadera.tipo = llenadera_request.tipo
    llenadera.save()
    
    return llenadera


@router.delete('/{llenadera_id}', response_model=LlenaderaResponseModel)
async def delete_llenadera(llenadera_id: int):
    llenadera = Llenadera.select().where(Llenadera.id == llenadera_id).first()
    if llenadera is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Llenadera no encontrada"}
        )

    llenadera.delete_instance()

    return llenadera

# ------------ Estado Llenaderas ------------
@router.post('/estado')
async def post_changeEstado(request: EstadoLlenaderaRequesteModel):
    # 1 = Detener lista de despacho
    # 0 = Liberar lista de despacho
    try:
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_EDOLISTA', request.estado)
        estado = "detenida" if request.estado == 1 else "liberada"
        return JSONResponse(
            status_code=201,
            content={"message": f'La llenadera ha sido {estado}'}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )

@router.get('/estado')
async def get_getEstado():
    try:
        #barrera = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_EDOLISTA')
        barrera = 1
        estado = "detenida" if barrera == 1 else "liberada"
        return JSONResponse(
            status_code=201,
            content={"message": f"La llenadera tiene estado: {estado}"}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )

# ------------ Acciones de  Llenaderas ------------
# -> aceptar asignacion
@router.post('/asignacion/aceptar')
async def post_aceptarAsignacion(request: EstadoLlenaderaRequesteModel):
    # 1 = Aceptar asignacion cgRFVER_ACEPTAASIGNA

    try:
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_ACEPTAASIGNA', request.estado)
        
        return JSONResponse(
            status_code=201,
            content={"message": 'La llenadera ha aceptado la asignacion.'}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )

# -> cancelar asignacion
@router.post('/asignacion/cancelar')
async def post_cancelarAsignacion(request: EstadoLlenaderaRequesteModel):
    # 1 = Cancelar asignacion RFVER_ELIMINAASIGNA

    try:
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_ELIMINAASIGNA', request.estado)
        
        return JSONResponse(
            status_code=201,
            content={"message": 'Se ha cancelado la asignacion de la llenadera.'}
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )

# -> reasignar asignacion
@router.post('/asignacion/reasignar')
async def post_reasignarAsignacion(request: NumeroLlenaderaRequesteModel):
    # 1 = Obtener La llenadera disponible del request
    llenadera = request.llenadera
    # 2 Escribir el valor en la llenadera que se elija

    try:
        result = reasignar(llenadera)
        if result == 0 :
            return JSONResponse(
                status_code=402,
                content={"message": 'Llenadera no existente.'}
            )
        #OpcServices.writeOPC(result, 1)
        return JSONResponse(
            status_code=201,
            content={"message": f'Se ha reasignado la llenadera {llenadera}.'}
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )

def reasignar(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN5',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN6',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN7',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN8',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN9',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN14'
    }
    return tabla_llenaderas.get(llenadera, 0 )

# -> siguiente asignacion
@router.post('/asignacion/siguiente')
async def post_siguienteAsignacion(request: EstadoLlenaderaRequesteModel):
    # 1 = Siguiente asignacion RFVER_SIGLLENADERA

    try:
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_SIGLLENADERA', request.estado)
        
        return JSONResponse(
            status_code=201,
            content={"message": 'Ha seleccionado otra llenadera para asignar.'}
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )