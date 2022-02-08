from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user_router, tank_router, opc_router, auth_router

from .database import User
from .database import TankWaiting
from .database import TankInService
from .database import TankInTrucks
from .database import TankAssign
from .database import Tank
from .database import Llenaderas
from .database import database as connection

from .opc import OpcServices

app = FastAPI(
    title='SCADA-IRGE',
    description='Api para servir OPC',
    version='1.0'
)

origins = [
    'http://10.121.50.126:3000',
    'http://localhost',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(tank_router)
app.include_router(opc_router)
app.include_router(auth_router)

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
    
    connection.create_tables([User, TankWaiting, TankInService, TankInTrucks, TankAssign, Tank, Llenaderas])
    
    #if OpcServices.conectarOPC():
        #print('conectado')
    #else:
        #print('No conectado')

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('close')






