from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from ..database import RelojPLC
from ..schemas import RelojPLCRequestModel, RelojPLCResponseModel

from ..middlewares import VerifyTokenRoute

router = APIRouter(prefix='/api/v1/relojPLC', route_class=VerifyTokenRoute)

@router.post('', response_model=RelojPLCResponseModel)
async def create_relojPLC(relojPlc: RelojPLCRequestModel):
    try:
        reloj = RelojPLC.create(
            year = relojPlc.year,
            month = relojPlc.month,
            day = relojPlc.day,
            hours = relojPlc.hours,
            mins = relojPlc.mins,
            secs = relojPlc.secs
        )

        return reloj
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )


@router.get('', response_model=List[RelojPLCResponseModel])
async def get_relojPLC():
    relojPlcs = RelojPLC.select()
    return [ relojPlc for relojPlc in relojPlcs ]


@router.put('/{relojPlc_id}', response_model=RelojPLCResponseModel)
async def edit_bitacora(relojPlc_id: int, relojPlc_request: RelojPLCRequestModel):
    relojPlc = RelojPLC.select().where(RelojPLC.id == relojPlc_id).first()
    if relojPlc is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Registro de reloj PLC no encontrado"}
        )
    relojPlc.year = relojPlc_request.year
    relojPlc.month = relojPlc_request.month
    relojPlc.day = relojPlc_request.day
    relojPlc.hours = relojPlc_request.hours
    relojPlc.mins = relojPlc_request.mins
    relojPlc.secs = relojPlc_request.secs
    relojPlc.save()
    
    return relojPlc


@router.delete('/{relojPlc_id}', response_model=RelojPLCResponseModel)
async def delete_bitacora(relojPlc_id: int):
    relojPlc = RelojPLC.select().where(RelojPLC.id == relojPlc_id).first()
    if relojPlc is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Registro en reloj PLC no encontrado"}
        )

    relojPlc.delete_instance()

    return relojPlc