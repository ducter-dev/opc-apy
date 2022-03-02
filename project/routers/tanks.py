from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from ..database import Tank, TankAssign, TankInService, TankInTrucks, TankWaiting, TankEntry

from ..schemas import TankEntryRequestModel, TankEntryResponseModel

from ..schemas import TankWaitingRequestModel, TankWaitingResponseModel, TankWaitingRequestPutModel, TankWaitingRequestPosicionPutModel

from ..schemas import TankInServiceResponseModel, TankInServiceRequestModel

from ..schemas import TankAssignRequestModel, TankAssignResponseModel

from ..schemas import TankInTrucksRequestModel, TankInTrucksResponseModel

from ..schemas import TankRequestModel, TankResponseModel

from ..middlewares import VerifyTokenRoute

from ..opc import OpcServices

router = APIRouter(prefix='/api/v1/tanques', route_class=VerifyTokenRoute)

# ---------------- Tanques ---------------------

@router.post('', response_model=TankResponseModel)
async def create_tanque(tank:TankRequestModel):
    tank = Tank.create(
        atId = tank.atId,
        atTipo = tank.atTipo,
        atName = tank.atName,
        conector = tank.conector,
        capacidad90 = tank.capacidad90,
        transportadora = tank.transportadora,
    )

    return tank

@router.get('', response_model=List[TankResponseModel])
async def get_tanks():
    tanks = Tank.select()
    return [ tank for tank in tanks ]

@router.put('/{tank_id}', response_model=TankResponseModel)
async def edit_tank(tank_id: int, tank_request: TankRequestModel):
    tank = Tank.select().where(Tank.id == tank_id).first()
    if tank is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Tanque no encontrado"}
        )
    tank.atId = tank_request.atId
    tank.atTipo = tank_request.atTipo
    tank.atName = tank_request.atName
    tank.conector = tank_request.conector
    tank.capacidad90 = tank_request.capacidad90
    tank.transportadora = tank_request.transportadora
    tank.save()
    
    return tank

@router.delete('/{tank_id}', response_model=TankResponseModel)
async def delete_tank(tank_id: int):
    tank = Tank.select().where(Tank.id == tank_id).first()
    if tank is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Tanque no encontrado"}
        )

    tank.delete_instance()

    return tank


@router.post('/llamar/{tank_id}')
async def call_tank(tank_id: int):
    try:
        tank = Tank.select().where(Tank.id == tank_id).first()
        if tank is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Tanque no encontrado"}
            )
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.Sig_Asigna_NumPG', tank.atId)
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.Sig_Asigna_TipoAT', tank.atTipo)
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.SIGUIENTE_ASIGN', 1)
        return JSONResponse(
            status_code=201,
            content={"message": f"El Tanque {tank.atName} ha sido mandado a llamar."}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )

@router.post('/alarmar')
async def alarm_tanks():
    try:
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.HABILITA_ALARMA', 1)
        return JSONResponse(
            status_code=201,
            content={"message": "Se ha habilitado la alarma sonora."}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )
    

# ---------------- Lista de Entrada ---------------------

@router.post('/entrada', response_model=TankEntryResponseModel)
async def create_tanque_entrada(tankEntry: TankEntryRequestModel):
    tank = TankEntry.create(
        posicion = tankEntry.posicion,
        atId = tankEntry.atId,
        atTipo = tankEntry.atTipo,
        atName = tankEntry.atName,
        capacidad = tankEntry.capacidad,
        conector = tankEntry.conector,
        horaEntrada = tankEntry.horaEntrada,
        fechaEntrada = tankEntry.fechaEntrada,
        reporte24 = tankEntry.reporte24,
        reporte05 = tankEntry.reporte05
    )

    return tank

@router.get('/entrada', response_model=List[TankEntryResponseModel])
async def get_tanksEntries():
    tanks = TankEntry.select()
    return [ tank for tank in tanks ]


# ---------------- Lista de Espera ---------------------

@router.post('/espera', response_model=TankWaitingResponseModel)
async def create_tanque_espera(tankWaiting: TankWaitingRequestModel):
    try:
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
            fechaEntrada = tankWaiting.fechaEntrada,
            reporte24 = tankWaiting.reporte24,
            reporte05 = tankWaiting.reporte05
        )

        return tankWaiting
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )

@router.get('/espera', response_model=List[TankWaitingResponseModel])
async def get_tanksWaiting():
    tanks = TankWaiting.select().order_by(TankWaiting.posicion)
    return [ tankWaiting for tankWaiting in tanks ]

@router.delete('/espera/{tank_id}', response_model=TankWaitingResponseModel)
async def delete_tankWaiting(tank_id: int):
    tank = TankWaiting.select().where(TankWaiting.id == tank_id).first()

    if tank is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Entrada de tanque no encontrada"}
        )

    tank.delete_instance()

    return tank

@router.put('/espera/{tank_id}', response_model=TankWaitingResponseModel)
async def update_tankWaiting(tank_id: int, tank_request: TankWaitingRequestModel):
    tank = TankWaiting.select().where(TankWaiting.id == tank_id).first()

    if tank is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Registro de Tanque en lista de espera no encontrada"}
        )
    
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
    tank.reporte24 = tank_request.reporte24
    tank.reporte05 = tank_request.reporte05
    tank.save()

    return tank

@router.post('/espera/cambio-posicion/{tank_id}', response_model=TankWaitingResponseModel)
async def post_tankWaitingchangePosition(tank_id: int, tank_request: TankWaitingRequestPosicionPutModel):
    # Obtener datos del tanque seleccionado
    tankSelect = TankWaiting.select().where(TankWaiting.id == tank_id).first()
    
    # Traer los tanques desde la posicion del tanque seleccionado hasta la nueva posicion
    tanks = TankWaiting.select().where(TankWaiting.posicion < tankSelect.posicion, TankWaiting.posicion >= tank_request.posicion)
    
    # Recorrer los tanques y aumentar 1 en la posicion
    for tank in tanks:
        tank.posicion = tank.posicion + 1
        tank.save()
    
    # Actualizar el tanque seleccionado a la nueva posicion 
    tankSelect.posicion = tank_request.posicion
    tankSelect.save()

    return tankSelect

@router.post('/espera/llamar/{tank_id}')
async def post_tankWaitingCall(tank_id: int):
    # Obtener datos del tanque seleccionado
    tankSelect = TankWaiting.select().where(TankWaiting.id == tank_id).first()
    
    # Escribir en las variables del opc
    # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.Sig_Asigna_NumPG', tankSelect.atId)
    # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.Sig_Asigna_TipoAT', tankSelect.atTipo)
    # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.SIGUIENTE_ASIGN', 1)
    return JSONResponse(
        status_code=201,
        content={ "message": f'Se ha mandado a llamar al autotanque {tankSelect.atName} que estaba en la posicion {tankSelect.posicion}' }
    )

@router.post('/espera/borrar')
async def post_tankWaitingDelete():
    # Obtener datos del tanque seleccionado
    tanks = TankWaiting.select()
    for tank in tanks:
        tank.delete_instance()

    return JSONResponse(
        status_code=201,
        content={ "message": 'Se ha Borrado la Lista de Espera' }
    )


# ---------------- Lista de Servicio ---------------------

@router.post('/servicio', response_model=TankInServiceResponseModel)
async def create_tanque_servicio(tankInService:TankInServiceRequestModel):
    tankInService = TankInService.create(
        productoNombre = tankInService.productoNombre,
        productoDescripcion = tankInService.productoDescripcion,
        atID = tankInService.atID,
        atTipo = tankInService.atTipo,
        atName = tankInService.atName,
        claveCarga = tankInService.claveCarga,
        conector = tankInService.conector,
        embarque = tankInService.embarque,
        capacidad = tankInService.capacidad,
        estandar = tankInService.estandar,
        commSAP = tankInService.commSAP,
        estatus = tankInService.estatus,
        llenadera = tankInService.llenadera,
        horaEntrada = tankInService.horaEntrada,
        fechaEntrada = tankInService.fechaEntrada,
        reporte24 = tankInService.reporte24,
        reporte05 = tankInService.reporte05
    )

    return tankInService

@router.get('/servicio', response_model=List[TankInServiceResponseModel])
async def get_tanksInService():
    tanks = TankInService.select()
    return [ tankInService for tankInService in tanks ]

@router.get('/servicio/ultimo', response_model=List[TankAssignResponseModel])
async def get_tanksAssign():
    tanks = TankAssign.select()
    return [ tankAssign for tankAssign in tanks ]

@router.post('/servicio/ultimo', response_model=TankAssignResponseModel)
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


# ---------------- Lista de Salida ---------------------
@router.post('/salida', response_model=TankInTrucksResponseModel)
async def create_tanque_despacho(tankInTrucks:TankInTrucksRequestModel):
    tank = TankInTrucks.create(
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
        reporte24 = tankInTrucks.reporte24,
        reporte05 = tankInTrucks.reporte05,
        tipoCarga = tankInTrucks.tipoCarga
    )

    return tank

@router.get('/salida', response_model=List[TankInTrucksResponseModel])
async def get_tanksInTrucks():
    tanks = TankInTrucks.select()
    return [ tankInTrucks for tankInTrucks in tanks ]

@router.put('/salida/{tank_id}', response_model=TankInTrucksResponseModel)
async def update_tankInTrucks(tank_id: int, tank_request: TankInTrucksRequestModel):
    tank = TankInTrucks.select().where(TankInTrucks.id == tank_id).first()

    if tank is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Registro de Tanque en lista de salida no encontrada"}
        )
    
    tank.productoNombre = tank_request.productoNombre
    tank.productoDescripcion = tank_request.productoDescripcion
    tank.atID = tank_request.atID
    tank.atTipo = tank_request.atTipo
    tank.atName = tank_request.atName
    tank.conector = tank_request.conector
    tank.embarque = tank_request.embarque
    tank.capacidad = tank_request.capacidad
    tank.estandarCapacidad = tank_request.estandarCapacidad
    tank.commSAP = tank_request.commSAP
    tank.respuestaMsgA = tank_request.respuestaMsgA
    tank.respuestaMsgB = tank_request.respuestaMsgB
    tank.respuestaMsgI = tank_request.respuestaMsgI
    tank.atEstatus = tank_request.atEstatus
    tank.llenadera = tank_request.llenadera
    tank.folioPLC = tank_request.folioPLC
    tank.volNatLts = tank_request.volNatLts
    tank.volNatBls = tank_request.volNatBls
    tank.volCorLts = tank_request.volCorLts
    tank.volCorBls = tank_request.volCorBls
    tank.masa = tank_request.masa
    tank.masaTons = tank_request.masaTons
    tank.densidadNat = tank_request.densidadNat
    tank.densidadCor = tank_request.densidadCor
    tank.porcentaje = tank_request.porcentaje
    tank.temperaturaBase = tank_request.temperaturaBase
    tank.temperatura = tank_request.temperatura
    tank.presion = tank_request.presion
    tank.modo = tank_request.modo
    tank.fechaEntrada = tank_request.fechaEntrada
    tank.fechaInicio = tank_request.fechaInicio
    tank.fechaFin = tank_request.fechaFin
    tank.reporte24 = tank_request.reporte24
    tank.reporte05 = tank_request.reporte05
    tank.tipoCarga = tank_request.tipoCarga
    tank.save()

    return tank

@router.delete('/salida/{tank_id}', response_model=TankInTrucksResponseModel)
async def delete_tankInTrucks(tank_id: int):
    tank = TankInTrucks.select().where(TankInTrucks.id == tank_id).first()

    if tank is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Salida de tanque no encontrada"}
        )

    tank.delete_instance()

    return tank
