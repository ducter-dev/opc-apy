from fastapi import HTTPException
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..database import User, Bloqueado
from ..schemas import UserResponseModel, UserRequestModel, UserRequestPutModel, BloqueadosRequestModel, BloqueadosResponseModel, BloqueadosUserRequestModel
from typing import List
from ..middlewares import VerifyTokenRoute
from datetime import datetime, timedelta

router = APIRouter(prefix='/api/v1/users', route_class=VerifyTokenRoute)


@router.get('', response_model=List[UserResponseModel])
async def get_users():
    users = User.select()
    return [ user for user in users ]
        

@router.delete('/{user_id}', response_model=UserResponseModel)
async def delete_user(user_id: int):
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    user.delete_instance()

    return user


@router.get('/bloqueados', response_model=List[BloqueadosResponseModel])
async def get_bloqueados():
    bloqueados = Bloqueado.select().join(User, on=(User.id == Bloqueado.user_id))
    return [ user for user in bloqueados ]


