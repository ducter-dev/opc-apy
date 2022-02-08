from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from ..database import Llenadera
from ..schemas import LlenaderaRequestModel, LlenaderaResponseModel

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