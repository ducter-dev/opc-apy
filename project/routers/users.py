from fastapi import HTTPException
from fastapi import APIRouter

from ..database import User
from ..schemas import UserResponseModel, UserRequestModel, UserRequestPutModel
from typing import List
from ..middlewares import VerifyTokenRoute

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