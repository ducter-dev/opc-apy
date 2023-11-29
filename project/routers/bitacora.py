from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import List

from ..database import Bitacora, User, Evento
from ..schemas import BitacoraRequestModel, BitacoraResponseModel

from ..middlewares import VerifyTokenRoute
from ..funciones import obtenerFecha05Reporte, obtenerFecha24Reporte
from datetime import datetime, timedelta

router = APIRouter(prefix='/api/v1/bitacora', route_class=VerifyTokenRoute)

@router.post('', response_model=BitacoraResponseModel)
async def create_bitacora(bitacora: BitacoraRequestModel, request: Request):
    try:
        now = datetime.now()
        ahora = now.strftime("%Y-%m-%d %H:%M:%S")
        dateStr = now.strftime("%Y-%m-%d")
        fecha05 = obtenerFecha05Reporte(now.hour, dateStr)
        fecha24 = obtenerFecha24Reporte(now.hour, dateStr)
        host = request.client.host

        bitacora = Bitacora.create(
            user = bitacora.user,
            evento = bitacora.evento,
            actividad = bitacora.actividad,
            fecha = ahora,
            ubicacion = host,
            reporte24 = fecha24,
            reporte05 = fecha05
        )
        return bitacora
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )


@router.get('/{fecha}', response_model=List[BitacoraResponseModel])
async def get_bitacora(fecha: str):
    bitacoras = Bitacora.select().join(User, on=(User.id == Bitacora.user_id)).join(Evento, on=(Evento.id == Bitacora.evento_id)).where(Bitacora.reporte05 == fecha).order_by(Bitacora.id.asc())
    return [ bitacora for bitacora in bitacoras ]


@router.put('/{bitacora_id}', response_model=BitacoraResponseModel)
async def edit_bitacora(bitacora_id: int, bitacora_request: BitacoraRequestModel):
    try:
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
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )


@router.delete('/{bitacora_id}', response_model=BitacoraResponseModel)
async def delete_bitacora(bitacora_id: int):
    try:
        bitacora = Bitacora.select().where(Bitacora.id == bitacora_id).first()
        if bitacora is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Registro en bitacora no encontrado"}
            )

        bitacora.delete_instance()

        return bitacora
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )