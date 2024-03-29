from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# import all you need from fastapi-pagination
from fastapi_pagination import add_pagination

import time
from .logs import LogsServices

from .routers import user_router, tank_router, auth_router, llenadera_router, bitacora_router, reloj_router, opc_router, barreras_router
from .routers import report_router, esfera_router, patin_router, croma_router, bomba_router

from .database import User
from .database import TanksEntry
from .database import TankEntry
from .database import TankWaiting
from .database import TanksInService
from .database import TankInTrucks
from .database import TankAssign
from .database import Tank
from .database import Llenadera
from .database import Evento
from .database import Bitacora
from .database import RelojPLC
from .database import Folio
from .database import TankExit
from .database import Bloqueado
from .database import Caducidad
from .database import Esfera
from .database import Patin
from .database import PatinData
from .database import Cromatografo
from .database import Bomba
from .database import BombaReporte
from .database import BalanceDiario
from .database import ReportePatin
from .database import Densidad
from .database import BalanceMensual
from .database import ReporteEsferas
from .database import database as connection

from .opc import OpcServices
#from .daemon import OpcDaemon

app = FastAPI(
    title='SCADA-IRGE',
    description='Api para servir SCADA IRGE',
    version='1.0'
)

@app.middleware("http")
async def verify_connexion(request: Request, call_next):
    print('checando middleware')
    if connection.is_closed():
        connection.connect()
    
    response = await call_next(request)
    print('Enviando response')
    connection.is_closed()
    return response
    

origins = [
    'http://10.121.50.126:3000',
    'http://localhost',
    'http://localhost:3000',
    'http://10.121.50.126',
    'http://scada.test',
    'http://10.122.50.96',
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
app.include_router(report_router)
app.include_router(esfera_router)
app.include_router(patin_router)
app.include_router(croma_router)
app.include_router(bomba_router)



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
        Evento,
        Bitacora,
        RelojPLC,
        Folio,
        TankEntry,
        TankExit,
        Bloqueado,
        Caducidad,
        Esfera,
        Patin,
        PatinData,
        Cromatografo,
        Bomba,
        BombaReporte,
        BalanceDiario,
        BalanceMensual,
        ReportePatin,
        Densidad,
        ReporteEsferas,
    ])
    LogsServices.setNameFile()
    LogsServices.write('Iniciando api')

    if OpcServices.conectarOPC():
        print('conectado')
        LogsServices.write('Conectando a OPC Server.')
    else:
        print('No conectado')
        LogsServices.write('No se pudo conectara OPC Server.')


add_pagination(app)
@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('close')

@app.exception_handler(Exception)
async def exeception_handler(request, exc):
    # Manejar la excepción aquí
    LogsServices.setNameFile()
    LogsServices.write(str(exc))
    return {"error": str(exc)}





