from fastapi import FastAPI

from .routers import user_router, tank_router, opc_router, auth_router

from .database import User
from .database import TankWaiting
from .database import TankInService
from .database import TankInTrucks
from .database import TankAssign
from .database import database as connection

from .opc import OpcServices

app = FastAPI(
    title='SCADA-IRGE',
    description='Api para servir OPC',
    version='1.0'
)

app.include_router(user_router)
app.include_router(tank_router)
app.include_router(opc_router)
app.include_router(auth_router)

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
    
    connection.create_tables([User, TankWaiting, TankInService, TankInTrucks, TankAssign])
    
    if OpcServices.conectarOPC():
        print('conectado')
    else:
        print('No conectado')

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('close')






