from fastapi import HTTPException
from fastapi import APIRouter
from typing import List

from ..database import TankAssign, TankInService, TankInTrucks, TankWaiting
from ..schemas import TankAssignRequestModel
from ..schemas import TankAssignResponseModel

from ..schemas import TankInTrucksRequestModel
from ..schemas import TankInTrucksResponseModel

from ..schemas import TankInServiceResponseModel
from ..schemas import TankInServiceRequestModel

from ..schemas import TankWaitingRequestModel
from ..schemas import TankWaitingResponseModel
from ..schemas import TankWaitingRequestPutModel


router = APIRouter(prefix='/api/v1/tanks')

@router.post('/tanques/espera', response_model=TankWaitingResponseModel)
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


@router.post('/tanques/servicio', response_model=TankInServiceResponseModel)
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


@router.post('/tanques/despacho', response_model=TankInTrucksResponseModel)
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

@router.post('/tanques/servicio/ultimo', response_model=TankAssignResponseModel)
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

@router.get('/tanques/espera', response_model=List[TankWaitingResponseModel])
async def get_tanksWaiting():
    tanks = TankWaiting.select()
    return [ tankWaiting for tankWaiting in tanks ]


@router.get('/tanques/servicio', response_model=List[TankInServiceResponseModel])
async def get_tanksInService():
    tanks = TankInService.select()
    return [ tankInService for tankInService in tanks ]


@router.get('/tanques/despacho', response_model=List[TankInTrucksResponseModel])
async def get_tanksInTrucks():
    tanks = TankInTrucks.select()
    return [ tankInTrucks for tankInTrucks in tanks ]


@router.get('/tanques/servicio/ultimo', response_model=List[TankAssignResponseModel])
async def get_tanksAssign():
    tanks = TankAssign.select()
    return [ tankAssign for tankAssign in tanks ]

@router.delete('/tanques/espera/{tank_id}', response_model=TankWaitingResponseModel)
async def delete_tankWaiting(tank_id: int):
    tank = TankWaiting.select().where(TankWaiting.id == tank_id).first()

    if tank is None:
        raise HTTPException(status_code=404, detail='Entrada de tanque no encontrada')

    tank.delete_instance()

    return tank

@router.put('/tanques/espera/{tank_id}', response_model=TankWaitingResponseModel)
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