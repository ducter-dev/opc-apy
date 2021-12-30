from fastapi import HTTPException
from fastapi import APIRouter

from ..database import User
from ..schemas import UserResponseModel, UserRequestModel, UserRequestPutModel
from typing import List

router = APIRouter(prefix='/api/v1/users')

@router.post('', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El usuario ya se encuentra en uso.')

    hash_password = User.create_password(user.password)
    user = User.create(
        username = user.username,
        password = hash_password,
        categoria = user.categoria,
        departamento = user.departamento
    )

    return user

@router.get('', response_model=List[UserResponseModel])
async def get_users():
    users = User.select()
    return [ user for user in users ]


@router.put('/{user_id}', response_model=UserResponseModel)
async def update_user(user_id: int, user_request: UserRequestPutModel):
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    
    user.username = user_request.username
    user.categoria = user_request.categoria
    user.departamento = user_request.departamento
    user.save()

    return user

@router.delete('/{user_id}', response_model=UserResponseModel)
async def delete_user(user_id: int):
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    user.delete_instance()

    return user