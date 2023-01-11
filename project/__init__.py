from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

from .routers import user_router, tank_router, auth_router, llenadera_router, bitacora_router, reloj_router, opc_router, barreras_router

from .database import User
from .database import TanksEntry
from .database import TankEntry
from .database import TankWaiting
from .database import TanksInService
from .database import TankInTrucks
from .database import TankAssign
from .database import Tank
from .database import Llenadera
from .database import Bitacora
from .database import RelojPLC
from .database import Folio
from .database import TankExit
from .database import database as connection

from .opc import OpcServices
#from .daemon import OpcDaemon

app = FastAPI(
    title='SCADA-IRGE',
    description='Api para servir OPC',
    version='1.0'
)

origins = [
    'http://10.121.50.126:3000',
    'http://localhost',
    'http://localhost:3000',
    'http://10.121.50.126',
    'http://scada.test'
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
app.include_router(llenadera_router)
app.include_router(bitacora_router)
app.include_router(reloj_router)
app.include_router(barreras_router)

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
    
    connection.create_tables([
        User,
        TanksEntry,
        TankWaiting,
        TanksInService,
        TankInTrucks,
        TankAssign,
        Tank,
        Llenadera,
        Bitacora,
        RelojPLC,
        Folio,
        TankEntry,
        TankExit,
    ])
    
    if OpcServices.conectarOPC():
        print('conectado')
    else:
        print('No conectado')



@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('close')






