from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from ..database import Bitacora
from ..schemas import BitacoraRequestModel, BitacoraResponseModel

from ..middlewares import VerifyTokenRoute

router = APIRouter(prefix='/api/v1/bitacora', route_class=VerifyTokenRoute)

@router.post('', response_model=BitacoraResponseModel)
async def create_bitacora(bitacora: BitacoraRequestModel):
    try:
        bitacora = Bitacora.create(
            usuario = bitacora.usuario,
            actividad = bitacora.actividad,
            ubicacion = bitacora.ubicacion,
            fecha = bitacora.fecha,
            reporte24 = bitacora.reporte24,
            reporte05 = bitacora.reporte05
        )

        return bitacora
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )


@router.get('', response_model=List[BitacoraResponseModel])
async def get_bitacora():
    bitacoras = Bitacora.select()
    return [ bitacora for bitacora in bitacoras ]


@router.put('/{bitacora_id}', response_model=BitacoraResponseModel)
async def edit_bitacora(bitacora_id: int, bitacora_request: BitacoraRequestModel):
    bitacora = Bitacora.select().where(Bitacora.id == bitacora_id).first()
    if bitacora is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Registro de bitacora no encontrado"}
        )
    bitacora.usuario = bitacora_request.usuario
    bitacora.actividad = bitacora_request.actividad
    bitacora.ubicacion = bitacora_request.ubicacion
    bitacora.fecha = bitacora_request.fecha
    bitacora.reporte24 = bitacora_request.reporte24
    bitacora.reporte05 = bitacora_request.reporte05
    bitacora.save()
    
    return bitacora


@router.delete('/{bitacora_id}', response_model=BitacoraResponseModel)
async def delete_bitacora(bitacora_id: int):
    bitacora = Bitacora.select().where(Bitacora.id == bitacora_id).first()
    if bitacora is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Registro en bitacora no encontrado"}
        )

    bitacora.delete_instance()

    return bitacora