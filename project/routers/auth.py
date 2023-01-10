from fastapi import HTTPException
from fastapi import APIRouter
from fastapi.params import Header
from fastapi.security import HTTPBasicCredentials
from ..schemas import UserResponseModel, UserRequestModel, UserRequestPutModel

from ..tokenServices import validate_token, write_token

from ..database import User
router = APIRouter(prefix='/api/v1/auth')

@router.post('/login')
async def login(credentials: HTTPBasicCredentials):
    user = User.select().where(User.username == credentials.username).first()
    if user is None:
        raise HTTPException(404, 'El usuario no existe.')
    
    user_valid = User.validate_password(credentials.password, user.password)
    if user_valid is False:
        raise HTTPException(404, 'Error, debe revisar sus credenciales.')
    user_dict = {
        "id": user.id,
        "username": user.username,
        "categoria": user.categoria,
        "departamento": user.departamento
    }
    print(user_dict)
    data_dic = {
        "ok": True,
        "token": write_token(user_dict)
    }
    return data_dic

@router.post('/register', response_model=UserResponseModel)
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


@router.post('/verify/token')
async def verify_token(Authorization: str = Header(None)):
    token = Authorization.split(' ')[1]
    return validate_token(token, output=True)