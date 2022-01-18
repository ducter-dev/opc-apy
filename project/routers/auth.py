from fastapi import HTTPException
from fastapi import APIRouter
from fastapi.params import Header
from fastapi.security import HTTPBasicCredentials

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

@router.post('/verify/token')
async def verify_token(Authorization: str = Header(None)):
    token = Authorization.split(' ')[1]
    return validate_token(token, output=True)