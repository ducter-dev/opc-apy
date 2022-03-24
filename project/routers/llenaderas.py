from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime, timedelta

from project.opc import OpcServices

from ..database import Llenadera, Folio, Tank, TankAssign, TankWaiting, TanksInService
from ..schemas import LlenaderaRequestModel, LlenaderaResponseModel, EstadoLlenaderaRequesteModel, NumeroLlenaderaRequesteModel, LlenaderaWithEstadoResponseModel, LlenaderaAsignarRequestModel
from ..schemas import FoliosRequestModel, FoliosResponseModel

from ..middlewares import VerifyTokenRoute

router = APIRouter(prefix='/api/v1/llenaderas', route_class=VerifyTokenRoute)

@router.post('', response_model=LlenaderaResponseModel)
async def create_llenadera(llenadera:LlenaderaRequestModel):
    tank = Llenadera.create(
        numero = llenadera.numero,
        conector = llenadera.conector,
        tipo = llenadera.tipo,
    )

    return tank


@router.get('', response_model=List[LlenaderaWithEstadoResponseModel])
async def get_llenaderas():
    llenaderas = Llenadera.select()
    llenMod = []
    for llen in llenaderas:
        if llen.numero < 10:
            estado = 1 #OpcServices.readDataPLC(f'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN0${llen.num}')
        else:
            estado = 0 #OpcServices.readDataPLC(f'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN${llen.num}')
        llen.estado = estado
        llenMod.append(llen)
    return [ llenadera for llenadera in llenMod ]


@router.put('/{llenadera_id}', response_model=LlenaderaResponseModel)
async def edit_llenadera(llenadera_id: int, llenadera_request: LlenaderaRequestModel):
    llenadera = Llenadera.select().where(Llenadera.id == llenadera_id).first()
    if llenadera is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Llenadera no encontrada"}
        )

    llenadera.numero = llenadera_request.numero
    llenadera.conector = llenadera_request.conector
    llenadera.tipo = llenadera_request.tipo
    llenadera.save()
    
    return llenadera


@router.delete('/{llenadera_id}', response_model=LlenaderaResponseModel)
async def delete_llenadera(llenadera_id: int):
    llenadera = Llenadera.select().where(Llenadera.id == llenadera_id).first()
    if llenadera is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Llenadera no encontrada"}
        )

    llenadera.delete_instance()

    return llenadera

# ------------ Estado Llenaderas ------------
@router.post('/estado')
async def post_changeEstado(request: EstadoLlenaderaRequesteModel):
    # 1 = Detener lista de despacho
    # 0 = Liberar lista de despacho
    try:
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_EDOLISTA', request.estado)
        estado = request.estado
        return JSONResponse(
            status_code=201,
            content={"estado": estado}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )

@router.get('/estado')
async def get_getEstado():
    try:
        #estado = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_EDOLISTA')
        estado = 1
        return JSONResponse(
            status_code=201,
            content={"estado": estado}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )

# ------------ Acciones de  Llenaderas ------------
# -> aceptar asignacion
@router.post('/asignacion/aceptar')
async def post_aceptarAsignacion(request: LlenaderaAsignarRequestModel):

    try:
        # 1 Obtener tanque y llenadera
        tanque = Tank.select().where(Tank.id == request.idTanque).first()
        if tanque is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Tanque no encontrado"}
            )
        llenadera = Llenadera.select().where(Llenadera.numero == request.llenadera).first()
        if llenadera is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Llenadera no encontrado"}
            )
        # 2 Aceptar asignacion cgRFVER_ACEPTAASIGNA = 1
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_ACEPTAASIGNA', 1)
        # OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_LLENDISP', request.llenadera)
        # Leer variables
        estadoLlenadera = 0 # OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_EDOLISTA')
        llenaderaDisponible = request.llenadera # OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_LLENDISP')
        asignacionStatus = 0 # OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_STATASIGNA')
        verificacionStatus = 0 # OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_STATVERIF')
        

        # 3 Escribit variables

        if estadoLlenadera == 0 :   # Lista de despacho libre
            if llenaderaDisponible > 0 :    # Hay llenadera disponible
                if asignacionStatus == 0 and verificacionStatus == 0 : # Servidor puede asignar autotanques
                    #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_NUMPG', tank.atName)
                    #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_TIPOAT', tank.atTipo)
                    #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_VOLPROG', tank.capacidad90)
                    #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_CONECTOR', tank.conector)
                    #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_CLAVE', tank.atId)
                    #OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_LISTAPOS', 1)

                    # 4 Actualizar tabla de ultima asignacion
                    now = datetime.now()
                    fecha_base = datetime(now.year, now.month, now.day, 5, 30, 0)
                    fecha05 =  now.strftime("%Y-%m-%d") if now > fecha_base else (now - timedelta(days=1)).strftime("%Y-%m-%d")
                    horaEntrada = now.strftime("%H:%M:%S")
                    fechaEntrada = now.strftime("%Y:%m:%d")

                    ultimaAsignacion = TankAssign.select().where(TankAssign.id == 1).first()
                    if ultimaAsignacion is None:
                        return JSONResponse(
                            status_code=404,
                            content={"message": "Tanque de ultima asignacion no encontrado."}
                        )
                    ultimaAsignacion.posicion = 1
                    ultimaAsignacion.atId = tanque.id
                    ultimaAsignacion.atTipo = tanque.atTipo
                    ultimaAsignacion.atName = tanque.atName
                    ultimaAsignacion.volProg = tanque.capacidad90
                    ultimaAsignacion.conector = tanque.conector
                    ultimaAsignacion.password = tanque.atId
                    ultimaAsignacion.fecha = fechaEntrada
                    ultimaAsignacion.llenadera = llenaderaDisponible
                    ultimaAsignacion.save()

                    # 5 Quitar tanque de la lista de espera
                    tankWaiting = TankWaiting.select().where(TankWaiting.atName == tanque.atName).first()
                    if tankWaiting is None:
                        return JSONResponse(
                            status_code=404,
                            content={"message": "Tanque en lista de espera no encontrado."}
                        )
                    tankWaiting.delete_instance()
                    
                    # 6 Meter tanque a Lista de Servicio
                    tanqueAtServicio = TanksInService.create(
                        productoNombre = "L.P.G.",
                        productoDescripcion = "Gas Licuado de Petroleo",
                        atID = tanque.atId,
                        atTipo =  tanque.atTipo,
                        atName = tanque.atName,
                        claveCarga = tanque.atId,
                        conector = tanque.conector,
                        embarque = 0,
                        capacidad = tanque.capacidad90,
                        estandar = tanque.capacidad90,
                        commSAP = 1,
                        estatus = 1,
                        llenadera = llenaderaDisponible,
                        horaEntrada = horaEntrada,
                        fechaEntrada = fechaEntrada,
                        reporte24 =  fechaEntrada,
                        reporte05 =  fecha05
                    )

                    if tanqueAtServicio is None:
                        return JSONResponse(
                            status_code=404,
                            content={"message": "Tanque en servicio no registrado"}
                        )

                    # 7 cgRFVER_ACEPTAASIGNA = 0
                    # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_ACEPTAASIGNA', 0)

                    # 8 Actualizar posiciones de los demas tanques en lista de espera
                    tanksWaiting = TankWaiting.select()
                    for tank in tanksWaiting:
                        print(f'posicion previa ${tank.posicion}')
                        tank.posicion = tank.posicion - 1
                        print(f'posicion posterior ${tank.posicion}')
                        tank.save()

                    return JSONResponse(
                        status_code=201,
                        content={"message": f"Tanque {tanque.atName} asignado a llenadera {llenaderaDisponible}."}
                    )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )

# -> cancelar asignacion
@router.post('/asignacion/cancelar')
async def post_cancelarAsignacion(request: EstadoLlenaderaRequesteModel):
    # 1 = Cancelar asignacion RFVER_ELIMINAASIGNA

    try:
        # OpcServices.writeOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_ELIMINAASIGNA', request.estado)
        
        return JSONResponse(
            status_code=201,
            content={"message": 'Se ha cancelado la asignacion de la llenadera.'}
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )

# -> reasignar asignacion
@router.post('/asignacion/reasignar')
async def post_reasignarAsignacion(request: NumeroLlenaderaRequesteModel):
    # 1 = Obtener La llenadera disponible del request
    llenadera = request.llenadera
    # 2 Escribir el valor en la llenadera que se elija

    try:
        result = reasignar(llenadera)
        if result == 0 :
            return JSONResponse(
                status_code=402,
                content={"message": 'Llenadera no existente.'}
            )
        #OpcServices.writeOPC(result, 1)
        #OpcServices.weiteOPC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.REASIGNA_LLENADERA',1)
        return JSONResponse(
            status_code=201,
            content={"message": f'Se ha reasignado la llenadera {llenadera}.'}
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )

def reasignar(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN5',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN6',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN7',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN8',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN9',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.ASIGN_LLEN14'
    }
    return tabla_llenaderas.get(llenadera, 0 )


# -> llenadera disponible en variable plc
@router.get('/libres')
async def get_llenadera_disponible():
    try:
        #llenadera_disponible = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_LLENDISP')
        llenadera_plc = 5
        #llenadera5 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN05')
        #llenadera6 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN06')
        #llenadera7 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN07')
        #llenadera8 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN08')
        #llenadera9 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN09')
        #llenadera10 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN10')
        #llenadera11 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN11')
        #llenadera12 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN12')
        #llenadera13 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN13')
        #llenadera14 = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN14')

        llenadera5 = 1
        llenadera6 = 0
        llenadera7 = 1
        llenadera8 = 0
        llenadera9 = 1
        llenadera10 = 1
        llenadera11 = 1
        llenadera12 = 1
        llenadera13 = 0
        llenadera14 = 0

        tabla_llenaderas = {
            "5": llenadera5, 
            "6": llenadera6, 
            "7": llenadera7, 
            "8": llenadera8, 
            "9": llenadera9, 
            "10": llenadera10, 
            "11": llenadera11, 
            "12": llenadera12, 
            "13": llenadera13, 
            "14": llenadera14,
            "plc": llenadera_plc
        }
        return JSONResponse(
            status_code=200,
            content={"data": tabla_llenaderas}
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )

# ------------ Folios Llenaderas ------------
@router.get('/folios', response_model=List[FoliosResponseModel])
async def get_folios():
    folios = Folio.select()
    return [ folio for folio in folios ]


@router.post('/folios', response_model=FoliosResponseModel)
async def create_folio(request: FoliosRequestModel):
    try:
        folio = Folio.create(
            llenadera_id=request.llenadera_id,
            folio = request.folio
        )
        return folio

    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )

@router.put('/folios/{folio_id}', response_model=FoliosResponseModel)
async def update_folio(folio_id: int, request: FoliosRequestModel):
    try:
        folio = Folio.select().where(Folio.id == folio_id).first()
        folio.llenadera_id = request.llenadera_id
        folio.folio = request.folio
        folio.save()
        return folio

    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )

@router.post('/desasignar/{llenadera}')
async def desasignar(llenadera: int):

    try: 

        print(llenadera)
        # obtener si la llenadera esta libre
        strLibre = getPLCLlenaderaLibre(llenadera)
        print(strLibre)
        if strLibre is False:
            return JSONResponse(
                status_code=401,
                content={"message": "Debe proporcionar un numero correcto de llenadera."}
            )
        #libre = OpcServices.readDataPLC(strLibre)
        libre = True
        # obtener el turno de la llenadera
        
        #strTurno = getPLCLlenaderaTurno(llenadera)
        #turno = OpcServices.readDataPLC(strTurno)
        turno = 0

        # si la llenadera esta libre y el turno es menor o igual a cero -> se debe modificar la llenadera
        if libre is True and turno <= 0:
            print('Libre true y turno cero')
            #strDesasignar = OpcServices.readDataPLC(llenadera)
            #OpcServices.writeOPC(strDesasignar)
            return JSONResponse(
                status_code=201,
                content={"message": f"El estatus de la llenadera {llenadera} se ha actualizado."}
            )

        
        # si la llenadera esta libre y el turno es mayor a cero -> enviar mensaje que ya esta deasignada
        elif libre is True and turno > 0:
            return JSONResponse(
                status_code=201,
                content={"message": f"La llenadera {llenadera} ya se encuanetra disponible."}
            )
        # de lo contrario enviar que se realice de forma manual
        else:
            return JSONResponse(
                status_code=201,
                content={"message": f"La llenadera {llenadera} no se encuentra liberada en el SCD, debe resetear la secuencia."}
            )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )
    

def getPLCLlenaderaLibre(llenadera):
    llenaderas = {
        5: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN05",
        6: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN06",
        7: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN07",
        8: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN08",
        9: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN09",
        10: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN10",
        11: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN11",
        12: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN12",
        13: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN13",
        14: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.LIBRE_LLEN14"
    }

    return llenaderas.get(llenadera, False)


def getPLCLlenaderaTurno(llenadera):
    llenaderas = {
        5: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.TURNO_LLEN05",
        6: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.TURNO_LLEN06",
        7: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.TURNO_LLEN07",
        8: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.TURNO_LLEN08",
        9: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.TURNO_LLEN09",
        10: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.TURNO_LLEN10",
        11: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.TURNO_LLEN11",
        12: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.TURNO_LLEN12",
        13: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.TURNO_LLEN13",
        14: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.TURNO_LLEN14"
    }

    return llenaderas.get(llenadera, False)


def getPLCLlenaderaDesasignar(llenadera):
    llenaderas = {
        5: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN05",
        6: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN06",
        7: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN07",
        8: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN08",
        9: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN09",
        10: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN10",
        11: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN11",
        12: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN12",
        13: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN13",
        14: "GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN14"
    }

    return llenaderas.get(llenadera, False)