from fastapi import FastAPI
from fastapi import HTTPException
from .database import User
from .database import tanksWaiting
from .database import tanksInService
from .database import tanksInTrucks
from .database import lastAssign
from .database import database as connection

from .schemas import UserRequestModel
from .schemas import UserResponseModel

app = FastAPI(
    title='SCADA-IRGE',
    description='Api para servir OPC',
    version='1.0'
)


@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
    
    connection.create_tables([User, tanksWaiting, tanksInService, tanksInTrucks, lastAssign])


@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('close')


@app.get('/')
async def index():
    return 'Hola mundo desde FastApi'

@app.post('/users', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, 'El usuario ya se encuentra en uso.')

    hash_password = User.create_password(user.password)
    user = User.create(
        username = user.username,
        password = hash_password,
        categoria = user.categoria,
        departamento = user.departamento
    )

    return user