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


@router.post('/bloqueados', response_model=BloqueadosResponseModel)
async def insert_bloqueados(request: BloqueadosRequestModel):
    bloqueado = Bloqueado.create(
        user = request.user,
        fechaBloqueo = request.fechaBloqueo,
        fechaDesbloqueo = request.fechaDesbloqueo,
    )
    return bloqueado


@router.post('/bloqueados/user')
async def insert_bloqueados(request: BloqueadosUserRequestModel):
    try:
        """ Se recibe el usuario en el request, primero se revisa si existe en la BD, si existe contninuamos, 
        si no retornamos que no existe con un status code 400.
        """

        now = datetime.now()
        user_bd = User.select().where(User.username == request.usuario).first()
        print(user_bd)
        if user_bd is None:
            return JSONResponse(
                status_code=400,
                content={"message": "El usuario no existe en nuestros registros."}
            )
        """ Revisamos que el usuario se encuentre en la tabla de bloqueos, si no existe retornamos bloqueado false, 
            y si existe comprobamos que la fecha de desbloqueo ya haya pasado.
        """
        bloqueado = Bloqueado.select().where(Bloqueado.user == user_bd.id).order_by(Bloqueado.id.desc()).first()

        if bloqueado is None:
            return JSONResponse(
                    status_code=200,
                    content={"bloqueado": False}
                )
        else:
            # ahora > fecha de desbloqueo
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
    