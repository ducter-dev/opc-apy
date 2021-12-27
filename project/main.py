from fastapi import FastAPI
from .database import User
from .database import tanksWaiting
from .database import tanksInService
from .database import tanksInTrucks
from .database import lastAssign
from .database import database as connection

from .schemas import UserBaseModel

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

@app.post('/users/')
async def register(user: UserBaseModel):
    user = User.create(
        username = user.username,
        password = user.password,
        categoria = user.categoria,
        departamento = user.departamento
    )

    return user.id