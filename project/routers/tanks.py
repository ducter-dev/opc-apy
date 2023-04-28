from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime, timedelta
from ..logs import LogsServices

from ..database import Tank, TankAssign, TankExit, TanksInService, TankInTrucks, TankWaiting, TanksEntry, TankEntry

from ..schemas import TanksEntryRequestModel, TanksEntryResponseModel, TanksLastEntryResponseModel

from ..schemas import TankWaitingRequestModel, TankWaitingResponseModel, TankWaitingRequestPutModel, TankWaitingRequestPosicionPutModel

from ..schemas import TanksInServiceResponseModel, TanksInServiceRequestModel, TanksLastAssignResponseModel, TanksLastExitResponseModel

from ..schemas import TankAssignRequestModel, TankAssignResponseModel

from ..schemas import TankInTrucksRequestModel, TankInTrucksResponseModel

from ..schemas import TankRequestModel, TankResponseModel, TankSingleRequestModel

from ..middlewares import VerifyTokenRoute

from ..funciones import obtenerFecha05Reporte, obtenerFecha24Reporte, obtenerTurno05, obtenerTurno24

from ..opc import OpcServices

router = APIRouter(prefix='/api/v1/tanques', route_class=VerifyTokenRoute)


path_Sig_Asigna_NumPG = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.Sig_Asigna_NumPG'
path_Sig_Asigna_TipoAT = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.Sig_Asigna_TipoAT'
path_SIGUIENTE_ASIGN = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.SIGUIENTE_ASIGN'

# ---------------- Tanques ---------------------

@router.post('', response_model=TankResponseModel)
async def create_tanque(tank_request:TankRequestModel):
    tank = Tank.create(
        atId = tank_request.atId,
        atTipo = tank_request.atTipo,
        atName = tank_request.atName,
        conector = tank_request.conector,
        capacidad90 = tank_request.capacidad90,
        transportadora = tank_request.transportadora,
    )

    return tank

@router.get('', response_model=List[TankResponseModel])
async def get_tanks():
    tanks = Tank.select()
    return [ tank for tank in tanks ]


@router.get('/detalle/{tank_id}', response_model=TankResponseModel)
async def get_tanks_id(tank_id: int):
    tank = Tank.select().where(Tank.id == tank_id).first()
    return tank



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


@router.post('/llamar')
async def call_tank():
    try:
        LogsServices.write('----------- Llamar Tanque --------------')
        tank = Tank.select().where(Tank.id == tank_id).first()
        if tank is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Tanque no encontrado"}
            )
        
        LogsServices.write(f'tanque_id: {tank.atId}')
        LogsServices.write(f'tanque_tipo: {tank.atTipo}')
        OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.Sig_Asigna_NumPG', tank.atId)
        OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.Sig_Asigna_TipoAT', tank.atTipo)
        OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.SIGUIENTE_ASIGN', 1)
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
        LogsServices.write('----------- Alarmar Tanques --------------')
        OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.HABILITA_ALARMA', 1)
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

@router.post('/entrada', response_model=TanksEntryResponseModel)
#@router.post('/entrada')
async def create_tanque_entrada(tank_request: TanksEntryRequestModel):
    
    try:
        #   Escribiendo datos de Entrada Manulmente

        #   Checar si existe el autotanque si no se crea uno nuevo
        tank = Tank.select().where(Tank.atId == tank_request.atId, Tank.atTipo == tank_request.atTipo ).first()

        if tank is None:
            tank = Tank.create(
                atId = tank_request.atId,
                atTipo = tank_request.atTipo,
                atName = tank_request.atName,
                conector = tank_request.conector,
                capacidad90 = tank_request.capacidad,
                transportadora = 0
            )
        
        now = datetime.now()
        fecha_base = datetime(now.year, now.month, now.day, 5, 0, 0)
        #   Se valida la hora con respecto a la hora base para determinar la fecha de jornada, si fecha base es mayor a la hora actual se resta 1 día.
        fecha05 = obtenerFecha05Reporte()
        fechaEntrada = now.strftime("%Y-%m-%d")
        horaEntrada = now.strftime("%H:%M-%S")
        
        TanksEntry.create(
            posicion = tank_request.posicion,
            atId = tank.atId,
            atTipo = tank.atTipo,
            atName = tank.atName,
            capacidad = tank.capacidad90,
            conector = tank.conector,
            horaEntrada = horaEntrada,
            fechaEntrada = fechaEntrada,
            reporte24 = fechaEntrada,
            reporte05 = fecha05
        )
        entryInserted = TanksEntry.select().order_by(TanksEntry.id.desc()).first()
        LogsServices.write(f'entryInserted: {entryInserted.id}: {entryInserted.atId} | {entryInserted.atName} | {entryInserted.conector} | {entryInserted.capacidad} | {entryInserted.fechaEntrada} {entryInserted.horaEntrada}')
        
        #   Se actualiza el registro de ultima entrada.
        lastEntry = TankEntry.select().where(TankEntry.id == 1).first()
        fechaE = f"{entryInserted.fechaEntrada} {entryInserted.horaEntrada}:00"
        
        lastEntry.atId = entryInserted.atId
        lastEntry.atTipo = entryInserted.atTipo
        lastEntry.atName = entryInserted.atName
        lastEntry.capacidad = entryInserted.capacidad
        lastEntry.conector = entryInserted.conector
        lastEntry.fechaEntrada = fechaE
        lastEntry.save()
        LogsServices.write(f'lastEntry: {lastEntry.id}: {lastEntry.atId} | {lastEntry.atName} | {lastEntry.atTipo} | {lastEntry.conector} | {lastEntry.capacidad} | {lastEntry.fechaEntrada}')

        return entryInserted

    except Exception as e:
        LogsServices.write(f'Error: {e}')
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )

    
@router.get('/entrada/fecha/{fecha}', response_model=List[TanksEntryResponseModel])
async def get_tanksEntries(fecha: str):
    tanks = TanksEntry.select().where(TanksEntry.reporte05 == fecha)
    return [ tank for tank in tanks ]


@router.get('/entrada/ultima', response_model=TanksLastEntryResponseModel)
async def get_tanksEntries():
    entry = TankEntry.select().where(TankEntry.id == 1).first()
    if entry is None:
        return JSONResponse(
        status_code=200,
        content={"data": entry}
        )
    return entry


@router.post('/entrada/ultima', response_model=TanksLastEntryResponseModel)
async def post_tanksEntries(tank: TanksEntryRequestModel):
    try:
        entry = TankEntry.select().where(TankEntry.id == 1).first()

        entry.atId = tank.atId
        entry.atTipo = tank.atTipo
        entry.atName = tank.atName
        entry.capacidad = tank.capacidad
        entry.conector = tank.conector
        entry.fechaEntrada = tank.fechaEntrada
        entry.save()

        if entry is None:
            return JSONResponse(
            status_code=200,
            content={"data": entry}
            )
        return entry
    
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )


# ---------------- Lista de Espera ---------------------

@router.post('/espera')
async def create_tanque_espera(tank_request: TanksEntryRequestModel):
    try:
        # Escribiendo datos de Entrada Manulmente
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFMAN_WRITING', 1)

        # Checar si existe el autotanque
        tank = Tank.select().where(Tank.atId == tank_request.atId, Tank.atTipo == tank_request.atTipo ).first()

        if tank is None:
            tank = Tank.create(
                atId = tank_request.atId,
                atTipo = tank_request.atTipo,
                atName = tank_request.atName,
                conector = tank_request.conector,
                capacidad90 = tank_request.capacidad,
                transportadora = 0
            )
        # Entrada Manual de Autotanque
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFMAN_NUMPG',tank.atName)
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFMAN_TIPOAT',tank.atTipo)
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFMAN_TIPO_CON',tank.conector)
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFMAN_CLAVE',tank.atId)
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFMAN_VOLAUTOR',tank.capacidad)

        now = datetime.now()
        
        #   Se valida la hora con respecto a la hora base para determinar la fecha de jornada, si fecha base es mayor a la hora actual se resta 1 día.
        fecha05 = obtenerFecha05Reporte()
        horaEntrada = now.strftime("%H:%M:%S")
        fechaEntrada = now.strftime("%Y-%m-%d")

        tankWaiting = TankWaiting.create(
            posicion = tank_request.posicion,
            atId = tank.atId,
            atTipo = tank.atTipo,
            atName = tank.atName,
            password = tank.atId,
            embarque = 0,
            capacidad = tank.capacidad90,
            conector = tank.conector,
            horaEntrada = horaEntrada,
            fechaEntrada = fechaEntrada,
            reporte24 = fechaEntrada,
            reporte05 = fecha05
        )

        # Empezar a escribir manualmente
        #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFMAN_WRITING', 1)
        LogsServices.write(f'tankWaiting: {tankWaiting.id}: {tankWaiting.atId} | {tankWaiting.atName} | {tankWaiting.atTipo} | {tankWaiting.conector} | {tankWaiting.capacidad} | {tankWaiting.fechaEntrada} {tankWaiting.horaEntrada}')
        response = {
            "id": tankWaiting.id,
            "posicion": tankWaiting.posicion,
            "atId": tankWaiting.atId,
            "atName": tankWaiting.atName,
            "atTipo": tankWaiting.atTipo,
            "embarque": tankWaiting.embarque,
            "capacidad": tankWaiting.capacidad,
            "conector": tankWaiting.conector,
            "horaEntrada": tankWaiting.horaEntrada,
            "fechaEntrada": tankWaiting.fechaEntrada,
            "reporte24": tankWaiting.reporte24,
            "reporte05": tankWaiting.reporte05,
        }
        return response

    except Exception as e:
        LogsServices.write(f'Error: {e}')
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


@router.post('/espera/mover-inicio', response_model=TankWaitingResponseModel)
async def post_tankWaitingchangePosition(tank_request: TankWaitingRequestPosicionPutModel):
    # Obtener datos del tanque seleccionado
    tankSelect = TankWaiting.select().where(TankWaiting.atName == tank_request.tanque).first()
    
    # Traer los tanques desde la posicion del tanque seleccionado hasta la nueva posicion
    tanks = TankWaiting.select().where(TankWaiting.id != tankSelect.id)

    if len(tanks) == 0:
        return JSONResponse(
           status_code=200,
            content={ "message": 'Sólo existe un tanque en la lista.' }
        )
    
    # Recorrer los tanques y aumentar 1 en la posicion
    for i in range(len(tanks)):
        tanks[i].posicion = i + 2
        tanks[i].save()
    
    # Actualizar el tanque seleccionado a la nueva posicion 
    tankSelect.posicion = 1
    tankSelect.save()

    return tankSelect


@router.post('/espera/llamar')
async def post_tankWaitingCall(req: TankSingleRequestModel):
    # Obtener datos del tanque seleccionado
    LogsServices.write('----------------- Llamando Tanque -----------------')
    LogsServices.write(f'req.tanque: {req.tanque}')
    tankSelect = TankWaiting.select().where(TankWaiting.atName == req.tanque).first()
    if tankSelect is None:
        return JSONResponse(
            status_code=404,
            content={ "message": 'No se encontró el tanque en la lista de espera.' }
            )
    
    LogsServices.write(f'tankSelect: {tankSelect.atName}')
    # Escribir en las variables del opc

    OpcServices.writeOPC(path_Sig_Asigna_NumPG, tankSelect.atId)
    OpcServices.writeOPC(path_Sig_Asigna_TipoAT, tankSelect.atTipo)
    OpcServices.writeOPC(path_SIGUIENTE_ASIGN, 1)
    
    LogsServices.write(f'path_Sig_Asigna_NumPG: {OpcServices.readDataPLC(path_Sig_Asigna_NumPG)}') 
    LogsServices.write(f'path_Sig_Asigna_TipoAT: {OpcServices.readDataPLC(path_Sig_Asigna_TipoAT)}') 
    LogsServices.write(f'path_SIGUIENTE_ASIGN: {OpcServices.readDataPLC(path_SIGUIENTE_ASIGN)}')
    

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

@router.post('/servicio', response_model=TanksInServiceResponseModel)
async def create_tanque_servicio(Tank:TanksInServiceRequestModel):
    try:
        TankCreated = TanksInService.create(
            productoNombre = Tank.productoNombre,
            productoDescripcion = Tank.productoDescripcion,
            atID = Tank.atID,
            atTipo = Tank.atTipo,
            atName = Tank.atName,
            claveCarga = Tank.claveCarga,
            conector = Tank.conector,
            embarque = Tank.embarque,
            capacidad = Tank.capacidad,
            estandar = Tank.estandar,
            commSAP = Tank.commSAP,
            estatus = Tank.estatus,
            llenadera = Tank.llenadera,
            horaEntrada = Tank.horaEntrada,
            fechaEntrada = Tank.fechaEntrada,
            reporte24 = Tank.reporte24,
            reporte05 = Tank.reporte05
        )

        return TankCreated
    
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )
    

@router.get('/servicio/fecha/{fecha}', response_model=List[TanksInServiceResponseModel])
async def get_tanksInService(fecha: str):
    tanks = TanksInService.select().where(TanksInService.reporte05 == fecha)
    return [ TanksInService for TanksInService in tanks ]

@router.get('/servicio/ultimo', response_model=TanksLastAssignResponseModel)
async def get_tanksLastAssign():
    tank = TankAssign.select().where(TankAssign.id == 1).first()
    return tank

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
        atId = tankInTrucks.atId,
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


@router.get('/salida/fecha/{fecha}', response_model=List[TankInTrucksResponseModel])
async def get_tanksInTrucks(fecha: str):
    tanks = TankInTrucks.select().where(TankInTrucks.reporte05 == fecha)
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
    tank.atId = tank_request.atId
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


@router.get('/salida/ultima', response_model=TanksLastExitResponseModel)
async def get_tanksLastAssign():
    tank = TankExit.select().where(TankExit.id == 1).first()
    return tank