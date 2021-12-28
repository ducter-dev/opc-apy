from typing import List
from fastapi import FastAPI
from fastapi import HTTPException

from .database import User
from .database import TankWaiting
from .database import TankInService
from .database import TankInTrucks
from .database import TankAssign
from .database import database as connection

from .opc import OpcServices

from .schemas import UserRequestModel
from .schemas import UserResponseModel
from .schemas import UserRequestPutModel

from .schemas import TankWaitingRequestModel
from .schemas import TankWaitingResponseModel
from .schemas import TankWaitingRequestPutModel

from .schemas import TankInServiceRequestModel
from .schemas import TankInServiceResponseModel

from .schemas import TankInTrucksRequestModel
from .schemas import TankInTrucksResponseModel

from .schemas import TankAssignRequestModel
from .schemas import TankAssignResponseModel

app = FastAPI(
    title='SCADA-IRGE',
    description='Api para servir OPC',
    version='1.0'
)


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

@app.post('/tanques/espera', response_model=TankWaitingResponseModel)
async def create_tanque_espera(tankWaiting:TankWaitingRequestModel):
    tankWaiting = TankWaiting.create(
        posicion = tankWaiting.posicion,
        atId = tankWaiting.atId,
        atTipo = tankWaiting.atTipo,
        atName = tankWaiting.atName,
        password = tankWaiting.password,
        embarque = tankWaiting.embarque,
        capacidad = tankWaiting.capacidad,
        conector = tankWaiting.conector,
        horaEntrada = tankWaiting.horaEntrada,
        fechaEntrada = tankWaiting.fechaEntrada
    )

    return tankWaiting


@app.post('/tanques/servicio', response_model=TankInServiceResponseModel)
async def create_tanque_servicio(tankInService:TankInServiceRequestModel):
    tankInService = TankInService.create(
        productoNombre = tankInService.productoNombre,
        productoDescripcion = tankInService.productoDescripcion,
        atID = tankInService.atID,
        atTipo = tankInService.atTipo,
        atName = tankInService.atName,
        claveCarga = tankInService.claveCarga,
        conector = tankInService.conector,
        Embarque = tankInService.Embarque,
        capacidad = tankInService.capacidad,
        estandar = tankInService.estandar,
        commSAP = tankInService.commSAP,
        estatus = tankInService.estatus,
        llenadera = tankInService.llenadera,
        horaEntrada = tankInService.horaEntrada,
        fechaEntrada = tankInService.fechaEntrada
    )

    return tankInService


@app.post('/tanques/despacho', response_model=TankInTrucksResponseModel)
async def create_tanque_despacho(tankInTrucks:TankInTrucksRequestModel):
    tankInTrucks = TankInTrucks.create(
        productoNombre = tankInTrucks.productoNombre,
        productoDescripcion = tankInTrucks.productoDescripcion,
        atID = tankInTrucks.atID,
        atTipo = tankInTrucks.atTipo,
        atName = tankInTrucks.atName,
        conector = tankInTrucks.conector,
        embarque = tankInTrucks.embarque,
        capacidad = tankInTrucks.capacidad,
        estandarCapacidad = tankInTrucks.estandarCapacidad,
        commSAP = tankInTrucks.commSAP,
        respuestaMsgA = tankInTrucks.respuestaMsgA,
        respuestaMsgB = tankInTrucks.respuestaMsgB,
        respuestaMsgI = tankInTrucks.respuestaMsgI,
        atEstatus = tankInTrucks.atEstatus,
        llenadera = tankInTrucks.llenadera,
        folioPLC = tankInTrucks.folioPLC,
        volNatLts = tankInTrucks.volNatLts,
        volNatBls = tankInTrucks.volNatBls,
        volCorLts = tankInTrucks.volCorLts,
        volCorBls = tankInTrucks.volCorBls,
        masa = tankInTrucks.masa,
        masaTons = tankInTrucks.masaTons,
        densidadNat = tankInTrucks.densidadNat,
        densidadCor = tankInTrucks.densidadCor,
        porcentaje = tankInTrucks.porcentaje,
        temperaturaBase = tankInTrucks.temperaturaBase,
        temperatura = tankInTrucks.temperatura,
        presion = tankInTrucks.presion,
        modo = tankInTrucks.modo,
        fechaEntrada = tankInTrucks.fechaEntrada,
        fechaInicio = tankInTrucks.fechaInicio,
        fechaFin = tankInTrucks.fechaFin,
        fechaSalida = tankInTrucks.fechaSalida,
        fechaJornada = tankInTrucks.fechaJornada,
        tipoCarga = tankInTrucks.tipoCarga,
    )

    return tankInTrucks

@app.post('/tanques/servicio/ultimo', response_model=TankAssignResponseModel)
async def create_tanque_servicio_ultimo(tankAssign:TankAssignRequestModel):
    tankAssign = TankAssign.create(
        atNum = tankAssign.atNum,
        atTipo = tankAssign.atTipo,
        atName = tankAssign.atName,
        volProg = tankAssign.volProg,
        conector = tankAssign.conector,
        embarque = tankAssign.embarque,
        password = tankAssign.password,
        fecha = tankAssign.fecha,
        llenadera = tankAssign.llenadera,
        posicion = tankAssign.posicion,
    )

    return tankAssign

@app.get('/users', response_model=List[UserResponseModel])
async def get_users():
    users = User.select()
    return [ user for user in users ]


@app.get('/tanques/espera', response_model=List[TankWaitingResponseModel])
async def get_tanksWaiting():
    tanks = TankWaiting.select()
    return [ tankWaiting for tankWaiting in tanks ]


@app.get('/tanques/servicio', response_model=List[TankInServiceResponseModel])
async def get_tanksInService():
    tanks = TankInService.select()
    return [ tankInService for tankInService in tanks ]


@app.get('/tanques/despacho', response_model=List[TankInTrucksResponseModel])
async def get_tanksInTrucks():
    tanks = TankInTrucks.select()
    return [ tankInTrucks for tankInTrucks in tanks ]


@app.get('/tanques/servicio/ultimo', response_model=List[TankAssignResponseModel])
async def get_tanksAssign():
    tanks = TankAssign.select()
    return [ tankAssign for tankAssign in tanks ]

@app.put('/users/{user_id}', response_model=UserResponseModel)
async def update_user(user_id: int, user_request: UserRequestPutModel):
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    
    user.username = user_request.username
    user.categoria = user_request.categoria
    user.departamento = user_request.departamento
    user.save()

    return user

@app.put('/tanques/espera/{tank_id}', response_model=TankWaitingResponseModel)
async def update_tankWaiting(tank_id: int, tank_request: TankWaitingRequestPutModel):
    tank = TankWaiting.select().where(TankWaiting.id == tank_id).first()

    if tank is None:
        raise HTTPException(status_code=404, detail='Entrada de Tanque no encontrada')
    
    tank.posicion = tank_request.posicion
    tank.atId = tank_request.atId
    tank.atTipo = tank_request.atTipo
    tank.atName = tank_request.atName
    tank.password = tank_request.password
    tank.embarque = tank_request.embarque
    tank.capacidad = tank_request.capacidad
    tank.conector = tank_request.conector
    tank.horaEntrada = tank_request.horaEntrada
    tank.fechaEntrada = tank_request.fechaEntrada
    tank.save()

    return tank


@app.delete('/users/{user_id}', response_model=UserResponseModel)
async def delete_user(user_id: int):
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    user.delete_instance()

    return user


@app.delete('/tanques/espera/{tank_id}', response_model=TankWaitingResponseModel)
async def delete_tankWaiting(tank_id: int):
    tank = TankWaiting.select().where(TankWaiting.id == tank_id).first()

    if tank is None:
        raise HTTPException(status_code=404, detail='Entrada de tanque no encontrada')

    tank.delete_instance()

    return tank

@app.get('/opc/entradasAntena')
async def opc_read():
    numPG = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.ANT_RFENT_NumPG')
    tipoPG = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.ANT_RFENT_TipoAT')
    return {
        'numAT': numPG,
        'tipoAT': tipoPG
    }

@app.get('/opc/bombas/301A')
async def opc_read():
    status = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301A_STATUS')
    mode = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301A_MODE')
    time = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Bombas.BA_301A_TIME')
    return {
        'status': status,
        'mode': mode,
        'time': time
    }

@app.post('/opc/llenadera/folio/{value}')
async def opc_write(value: int):
    tag = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uLLEN01_FOLIO'
    valor = OpcServices.writeOPC(tag, value)
    return {
        'tag': tag,
        'valor': valor
    }