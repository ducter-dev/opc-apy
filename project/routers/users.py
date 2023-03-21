from fastapi import HTTPException
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..database import User, Bloqueado
from ..schemas import UserResponseModel, UserRequestModel, UserRequestPutModel, BloqueadosRequestModel, BloqueadosResponseModel
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


@router.post('/bloqueados', response_model=BloqueadosResponseModel)
async def insert_bloqueados(request: BloqueadosRequestModel):
    bloqueado = Bloqueado.create(
        user = request.user,
        fechaBloqueo = request.fechaBloqueo,
        fechaDesbloqueo = request.fechaDesbloqueo,
    )
    return bloqueado


@router.get('/bloqueados/user/{user_id}')
async def insert_bloqueados(user_id: int):
    try:
        now = datetime.now()
        bloqueado = Bloqueado.select().where(Bloqueado.user == user_id).order_by(Bloqueado.id.desc()).first()
        print(f'now: {now}')
        print(f'bloqueado.fechaDesbloqueo: {bloqueado.fechaDesbloqueo}')
        if now > bloqueado.fechaDesbloqueo:
            return JSONResponse(
                status_code=200,
                content={"bloqueado": False}
            )
        else:
            return JSONResponse(
                status_code=200,
                content={"bloqueado": True}
            )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )
    