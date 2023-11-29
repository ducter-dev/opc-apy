from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime, timedelta

from project.opc import OpcServices

from ..database import Llenadera, Folio, Tank, TankAssign, TankWaiting, TanksInService, TankInTrucks, TankExit
from ..schemas import LlenaderaRequestModel, LlenaderaResponseModel, EstadoLlenaderaRequesteModel, NumeroLlenaderaRequesteModel, LlenaderaWithEstadoResponseModel, LlenaderaAsignarRequestModel, TanksInServiceResponseModel
from ..schemas import FoliosRequestModel, FoliosResponseModel
from ..funciones import obtenerFecha05Reporte, obtenerFecha24Reporte, obtenerTurno05, obtenerTurno24
from ..logs import LogsServices

from ..middlewares import VerifyTokenRoute

router = APIRouter(prefix='/api/v1/llenaderas', route_class=VerifyTokenRoute)

path_llenaderaDisponible = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_LLENDISP'
path_aceptaAsignacion = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_ACEPTAASIGNA'
path_statusVerificado = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_STATVERIF'
path_estadoListaDespacho = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_EDOLISTA'
path_statusAsignacion = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_STATASIGNA'
path_ver_numPG = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_NUMPG'
path_ver_tipoAT = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_TIPOAT'
path_ver_clave = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_CLAVE'
path_ver_volProg = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_VOLPROG'
path_ver_conector = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_CONECTOR'
path_ver_listaPos = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_LISTAPOS'
path_siguienteAsinacion = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_SIGLLENADERA'
path_cancelarAsignacion = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.RFVER_ELIMINAASIGNA'
path_reasignarLlenadera = 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.REASIGNA_LLENADERA'

@router.post('', response_model=LlenaderaResponseModel)
async def create_llenadera(llenadera:LlenaderaRequestModel):
    llenadera = Llenadera.create(
        numero = llenadera.numero,
        conector = llenadera.conector,
        tipo = llenadera.tipo,
    )

    return llenadera


@router.get('', response_model=List[LlenaderaResponseModel])
async def get_llenaderas():
    LogsServices.setNameFile()
    llenaderas = Llenadera.select()
    return [ llenadera for llenadera in llenaderas ]


@router.put('/{llenadera_id}', response_model=LlenaderaResponseModel)
async def edit_llenadera(llenadera_id: int, llenadera_request: LlenaderaRequestModel):
    try:
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
    except Exception as e:
        return JSONResponse(
        status_code=401,
        content={"message": e}
    )

@router.delete('/{llenadera_id}', response_model=LlenaderaResponseModel)
async def delete_llenadera(llenadera_id: int):
    try:
        llenadera = Llenadera.select().where(Llenadera.id == llenadera_id).first()
        if llenadera is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Llenadera no encontrada"}
            )

        llenadera.delete_instance()

        return llenadera
    except Exception as e:
        return JSONResponse(
        status_code=401,
        content={"message": e}
    )
    

# ------------ Estado Llenaderas ------------
@router.post('/estado')
async def post_changeEstado(request: EstadoLlenaderaRequesteModel):
    # 1 = Detener lista de despacho
    # 0 = Liberar lista de despacho
    try:
        LogsServices.setNameFile()
        OpcServices.writeOPC(path_estadoListaDespacho, request.estado)
        estado = request.estado
        return JSONResponse(
            status_code=201,
            content={"estado": estado}
        )
    except Exception as e:
        return JSONResponse(
        status_code=401,
        content={"message": str(e)}
    )

@router.get('/estado')
async def get_getEstado():
    try:
        LogsServices.setNameFile()
        estado = OpcServices.readDataPLC(path_estadoListaDespacho)
        return JSONResponse(
            status_code=200,
            content={"estado": estado}
        )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )


# ------------ Acciones de  Llenaderas ------------
# -> aceptar asignaciones
@router.post('/asignacion/aceptar')
async def post_aceptarAsignaciones():
    try:
        LogsServices.setNameFile()
        OpcServices.writeOPC(path_aceptaAsignacion, 1)
        return JSONResponse(
            status_code=201,
            content={"estado": True}
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={
                "estado": False,
                "message": str(e)
            }
        )
    

@router.post('/asignacion/siguiente')
async def post_aceptarAsignaciones():
    try:
        LogsServices.setNameFile()
        OpcServices.writeOPC(path_siguienteAsinacion, 1)
        return JSONResponse(
            status_code=201,
            content={"estado": True}
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={
                "estado": False,
                "message": str(e)
            }
        )



@router.post('/asignacion/verificar')
async def post_aceptarAsignaciones():
    try:
        LogsServices.setNameFile()
        OpcServices.writeOPC(path_statusVerificado, 0)
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={
                "estado": False,
                "message": str(e)
            }
        )


# -> asignar
@router.post('/asignacion/preasignar')
async def post_realizarAsignacion(request: LlenaderaAsignarRequestModel):

    try:
        # 1 Obtener tanque y llenadera
        LogsServices.setNameFile()
        LogsServices.write("------------Iniciando Preaasignacion---------------")
        if OpcServices.activo == False :
            return JSONResponse(
                status_code=501,
                content={"message": "Servidor Opc No encontrado"}
            )
        
        tanque = Tank.select().where(Tank.atName == request.tanque).first()
        if tanque is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Tanque no encontrado"}
            )

        inicialTanque = '' if tanque.atTipo == 0 else tanque.atTipo
        LogsServices.write(f"tanque.atTipo: {tanque.atTipo}")
        LogsServices.write(f"inicialTanque: {inicialTanque}")
        tipoAT = f'{inicialTanque}{tanque.atId}'
        LogsServices.write(f"tipoAT: {tipoAT}")
        OpcServices.writeOPC(path_statusVerificado, 0)

        # Variables que se usan en asignacion
        llenaderaDisponible = OpcServices.readDataPLC(path_llenaderaDisponible)
        LogsServices.write(f"llenaderaDisponible: {llenaderaDisponible}")

        llenadera = Llenadera.select().where(Llenadera.numero == llenaderaDisponible).first()
        if llenadera is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Llenadera no encontrado"}
            )
        
        # Leer variables
        OpcServices.writeOPC(path_estadoListaDespacho, 0)
        asignacionStatus = OpcServices.readDataPLC(path_statusAsignacion)
        verificacionStatus = OpcServices.readDataPLC(path_statusVerificado)
        listaDespacho = OpcServices.readDataPLC(path_estadoListaDespacho)
        LogsServices.write(f"listaDespacho: {listaDespacho}")
        LogsServices.write(f"asignacionStatus: {asignacionStatus}")
        LogsServices.write(f"verificacionStatus: {verificacionStatus}")
        
        if listaDespacho == 0:
            LogsServices.write('Lista de Despacho Libre')
            LogsServices.write(f'listaDespacho: {listaDespacho}')
            if llenaderaDisponible > 0:
                if asignacionStatus == 0 & verificacionStatus == 0:
                    print('Servidor puede asignar tanques')
                    LogsServices.write(f"asignacionStatus: {asignacionStatus}")

                    # Escribir variables en los registros de la plc
                    OpcServices.writeOPC(path_ver_numPG, tanque.atId)
                    OpcServices.writeOPC(path_ver_tipoAT, tanque.atTipo)
                    OpcServices.writeOPC(path_ver_clave, tanque.atId)
                    OpcServices.writeOPC(path_ver_volProg, tanque.capacidad90)
                    OpcServices.writeOPC(path_ver_conector, tanque.conector)
                    OpcServices.writeOPC(path_ver_listaPos, 1)
                    OpcServices.writeOPC(path_statusAsignacion, 1)
                    OpcServices.writeOPC(path_ver_listaPos, 1)
                    OpcServices.writeOPC(path_statusVerificado, 1)
                    
                    LogsServices.write("------Preasignacion-------")
                    LogsServices.write(f"llenederaDisp: {OpcServices.readDataPLC(path_llenaderaDisponible)}")
                    LogsServices.write(f"path_ver_numPG: {OpcServices.readDataPLC(path_ver_numPG)}")
                    LogsServices.write(f"path_ver_tipoAT: {OpcServices.readDataPLC(path_ver_tipoAT)}")
                    LogsServices.write(f"path_ver_clave: {OpcServices.readDataPLC(path_ver_clave)}")
                    LogsServices.write(f"path_ver_volProg: {OpcServices.readDataPLC(path_ver_volProg)}")
                    LogsServices.write(f"path_ver_conector: {OpcServices.readDataPLC(path_ver_conector)}")
                    LogsServices.write(f"path_ver_numPG: {OpcServices.readDataPLC(path_ver_numPG)}")
                    LogsServices.write(f"path_aceptaAsignacion: {OpcServices.readDataPLC(path_aceptaAsignacion)}")

                    LogsServices.write(f"tanque.atId: {tanque.atId}")
                    LogsServices.write(f"tipoAT: {tipoAT}")
                    LogsServices.write(f"tanque.capacidad90: {tanque.capacidad90}")
                    LogsServices.write(f"tanque.conector: {tanque.conector}")

                    LogsServices.write(f'Tanque preasignado: {tanque.atId} | {tipoAT} | {tanque.conector} | {tanque.capacidad90} en llenadera {llenaderaDisponible}')
                    LogsServices.write('-------------------------------')

                    return JSONResponse(
                        status_code=201,
                        content={
                            "message": 'Autotanque Preasignado',
                        }
                    )

        if asignacionStatus == 0:
            LogsServices.write(f'asignacionStatus: Tanque NO ha sido asignado')
            return JSONResponse(
                status_code=404,
                content={
                    "message": "Tanque NO ha sido asignado"
                    
                }
            )

        if verificacionStatus == 0:
            LogsServices.write(f'verificacionStatus: Tanque NO ha sido verificado por el sistema')
            return JSONResponse(
                status_code=404,
                content={
                    "message": "Tanque NO ha sido verificado por el sistema"
                }
            )
        
        if (asignacionStatus == 1 & verificacionStatus == 1):
            # Removiendo tanque de monitor de asignacion
            # Se mete tanque a servicio
            #OpcServices.writeOPC(path_llenaderaDisponible, 0)
            OpcServices.writeOPC(path_statusAsignacion, 0)
            LogsServices.write(f'asignacionStatus: 1')
            LogsServices.write(f'verificacionStatus 1')
            LogsServices.write(f'path_statusAsignacion: 0')
            LogsServices.write(f'path_llenaderaDisponible: 0')
            return JSONResponse(
                status_code=201,
                content={
                    "message": 'Preasignado',
                }
            )

    except Exception as e:
        LogsServices.write(f'Error: {e}')
        return JSONResponse(
        status_code=501,
        content={"message": str(e)}
    )


@router.post('/asignacion/asignar', response_model=TanksInServiceResponseModel)
async def post_asignarLlenadera(request: LlenaderaAsignarRequestModel):
    
    try: 
        # Poner llenadera ocupada y con tipo de pg
        #llenaderaDisponible = 14
        LogsServices.write("------------Asignar---------------")
        tanque = Tank.select().where(Tank.atName == request.tanque).first()
        if tanque is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Tanque no encontrado"}
            )
        LogsServices.write(f"tanque: {tanque.atId}")
        llenaderaDisponible = OpcServices.readDataPLC(path_llenaderaDisponible)
        LogsServices.write(f"llenaderaDisponible: {llenaderaDisponible}")
        pathLlenaderaLibre =  getPLCLlenaderaLibre(llenaderaDisponible)
        pathLlenaderaTipo = getPLCLlenaderaTipo(llenaderaDisponible)
        pathAsigLlenadera = getPathAsignarLlenadera(llenaderaDisponible)
        pathNipLlenadera = getPLCNipLlenadera(llenaderaDisponible)
        pathPGLlenadra = getPLCPGLlenadera(llenaderaDisponible)
        LogsServices.write(f"llenadera: {llenaderaDisponible}")
        
        """
        idAT = OpcServices.readDataPLC(path_ver_clave)
        tipoAT = OpcServices.readDataPLC(path_ver_tipoAT)
        numPG = OpcServices.readDataPLC(path_ver_numPG)
        volProg = OpcServices.readDataPLC(path_ver_volProg)
        conector = OpcServices.readDataPLC(path_ver_conector)
        """
        
        

        inicialTanque = '' if tanque.atTipo == 0 else tanque.atTipo
        print(inicialTanque)
        tipoAT = int(f'{inicialTanque}{tanque.atId}')
        print(tipoAT)
            
        idAT = tanque.atId
        tipoAT = tipoAT
        numPG = tanque.atName
        volProg = tanque.capacidad90
        conector =tanque.conector
        
        LogsServices.write("------------Encontrado---------------")
        LogsServices.write(f"idAT: {idAT}")
        LogsServices.write(F"tipoAT: {tipoAT}")
        LogsServices.write(F"numPG: {numPG}")
        LogsServices.write(F"volProg: {volProg}")
        LogsServices.write(F"conector: {conector}")

        OpcServices.writeOPC(path_aceptaAsignacion, 1)
        OpcServices.writeOPC(pathAsigLlenadera, 1)
        OpcServices.writeOPC(pathNipLlenadera, idAT)
        OpcServices.writeOPC(pathPGLlenadra, idAT)
        OpcServices.writeOPC(pathLlenaderaTipo, tipoAT)
        OpcServices.writeOPC(pathLlenaderaLibre, 0)
        OpcServices.writeOPC(path_statusAsignacion, 0)

        #   Se valida la hora con respecto a la hora base para determinar la fecha de jornada, si fecha base es mayor a la hora actual se resta 1 día.
        now = datetime.now()
        horaEntrada = now.strftime("%H:%M:%S")
        fechaEntrada = now.strftime("%Y-%m-%d")
        ahora = now.strftime("%Y-%m-%d %H:%M:%S")
        dateStr = now.strftime("%Y-%m-%d")
        fecha05 = obtenerFecha05Reporte(now.hour, dateStr)

        #   Agregar la tanque a última asignación 
        ultimaAsignacion = TankAssign.select().where(TankAssign.id == 1).first()
        if ultimaAsignacion is None:
            LogsServices.write('Error: Tanque de ultima asignacion no encontrado.')
            return JSONResponse(
                status_code=404,
                content={"message": "Tanque de ultima asignacion no encontrado."}
            )
        

        ultimaAsignacion.posicion = 1
        ultimaAsignacion.atId = idAT
        ultimaAsignacion.atTipo = tipoAT
        ultimaAsignacion.atName = numPG
        ultimaAsignacion.volProg = volProg
        ultimaAsignacion.conector = conector
        ultimaAsignacion.password = idAT
        ultimaAsignacion.fecha = fechaEntrada
        ultimaAsignacion.llenadera = llenaderaDisponible
        ultimaAsignacion.save()
        LogsServices.write('Actualizada última asignación.')
        

        # Pasar tanque a lista de servicio
        tanque_insertado_servicio = TanksInService(
            productoNombre = "L.P.G.",
            productoDescripcion = "Gas Licuado de Petroleo",
            atID = idAT,
            atTipo =  tipoAT,
            atName = numPG,
            claveCarga = idAT,
            conector = conector,
            embarque = 0,
            capacidad = volProg,
            estandar = volProg,
            commSAP = 1,
            estatus = 1,
            llenadera = llenaderaDisponible,
            horaEntrada = horaEntrada,
            fechaEntrada = fechaEntrada,
            reporte24 =  fechaEntrada,
            reporte05 =  fecha05
        )
        tanque_insertado_servicio.save()
        
        tanque_insertado_servicio = TanksInService.select().order_by(TanksInService.id.desc()).first()
        LogsServices.write(f"tanque_insertado_servicio: {tanque_insertado_servicio.atName}")
        
        #   Eliminar de la lista de espera
        LogsServices.write(f"ultimaAsignacion.atName: {ultimaAsignacion.atName}")
        tank_delete = TankWaiting.select().where(TankWaiting.atName == ultimaAsignacion.atName).first()
        if tank_delete is None:
            return tanque_insertado_servicio
            
        LogsServices.write(f'Tanque eliminado de lista de servicio: {tank_delete.atName}')
        tank_delete.delete_instance()
        
        # Cambiar el orden de posicion de los tanques
        tanques_le = TankWaiting.select().order_by(TankWaiting.posicion.asc())
        if len(tanques_le) > 0:
            print(tanques_le)
            for i in range(len(tanques_le)):
                tanques_le[i].posicion = i + 1
                tanques_le[i].save()

        return tanque_insertado_servicio
    
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )



# -> cancelar asignacion
@router.post('/asignacion/cancelar')
async def post_cancelarAsignacion():
    # 1 = Cancelar asignacion RFVER_ELIMINAASIGNA

    try:
        LogsServices.setNameFile()
        OpcServices.writeOPC(path_cancelarAsignacion, 1)
        
        return JSONResponse(
            status_code=201,
            content={
                "estado": True,
                "message": 'Se ha cancelado la asignacion de la llenadera.'
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )

# -> reasignar asignacion
@router.post('/asignacion/reasignar')
async def post_reasignarAsignacion():
    try:
        # 1 = Obtener La llenadera disponible
        LogsServices.setNameFile()
        llenaderaDisponible = OpcServices.readDataPLC(path_llenaderaDisponible)
        #llenaderaDisponible = 6
        if llenaderaDisponible is None:
            return JSONResponse(
                status_code=404,
                content={
                    "estado": False,
                    "message": "OPC servidor no disponible."
                }
            )
        # 2 Escribir el valor en la llenadera que se elija
        pathReasignar = getPathAsignarLlenadera(llenaderaDisponible)
        OpcServices.writeOPC(pathReasignar, 1)
        OpcServices.writeOPC(path_reasignarLlenadera,1)
        
        return JSONResponse(
            status_code=201,
            content={
                "estado": True,
                "message": f'Se ha reasignado la llenadera {llenaderaDisponible}.'
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )
    

# -> resetear llenadera 
@router.post('/liberar/{llenadera}')
async def post_liberar_llenadera(llenadera: int):
    try:
        LogsServices.setNameFile()
        pathLiberar = getPathAsignarLlenadera(llenadera)
        OpcServices.writeOPC(pathLiberar, 0)
        
        return JSONResponse(
            status_code=201,
            content={
                "estado": True,
                "message": f'Se ha Liberado la llenadera {llenadera}.'
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": str(e)}
        )
    



# -> salidas Llenaderas
@router.post('/asignacion/salida')
async def postGetSenalesSalidas():
    try:
        # Revisar Folio Llenadera
        LogsServices.setNameFile()
        numLlenaderas = [5,6,7,8,9,10,11,12,13,14]
        

        for llen in numLlenaderas:
            url_llenaderaLibre = getPLCLlenaderaLibre(llen)
            #LogsServices.write(f'path_llenaderaLibre: {url_llenaderaLibre}')
            llenaderaIsLibre = OpcServices.readDataPLC(url_llenaderaLibre)
            #LogsServices.write(f'llenadera IsLibre: {llenaderaIsLibre}')
            if llenaderaIsLibre == 0 :
                #LogsServices.write(f'-------- Cargando Pasamos a otra llenadera ---------')
                #LogsServices.write(f'************************************')
                continue
            else:
                #LogsServices.write(f'-----------Revisar Folio----------')
                #LogsServices.write(f'llen: {llen}')
                #LogsServices.write(f'llenadera IsLibre: {llenaderaIsLibre}')
                llenadera = Llenadera.select().where(Llenadera.numero == llen).first()
                #LogsServices.write(f'llenadera: {llenadera.numero}')
                folioDB = Folio.select().where(Folio.llenadera_id == llenadera.id).first()
                #LogsServices.write(f'folioDB: {folioDB.folio}')
                pathFolioLlenadera = getFolioLllenadera(llenadera.numero)
                #LogsServices.write(f'pathFolioLlenadera: {pathFolioLlenadera}')
                folioLlenadera = OpcServices.readDataPLC(pathFolioLlenadera)
                #LogsServices.write(f'folioLlenadera: {folioLlenadera}')
                #LogsServices.write(f'Llenadera: {llen}')
                #LogsServices.write(f'folioLlenadera: {folioLlenadera}')

                # Si folioPCL es diferente al folioDB Se registra - else se omite el registro
                if (folioLlenadera != folioDB.folio):
                    # Obtener el tanque de la lista de Servicio
                    #LogsServices.write(f'-----------Registrar Carga----------')
                    tipoAtUCL = OpcServices.readDataPLC(getPLCLlenaderaTipo(llenadera.numero))
                    #tipoAtUCL = 12100
                    #LogsServices.write(f'tipoAtUCL: {tipoAtUCL}')
                    tipoAtUCLSt = f"{tipoAtUCL}"
                    LogsServices.write(f'tipoAtUCLSt: {tipoAtUCLSt}')
                    atID = ''
                    atType = ''
                    if len(tipoAtUCLSt) < 5:
                        atID = tipoAtUCL
                        atType = 0
                    else:
                        atID = int(tipoAtUCLSt[1:5])
                        atType = int(tipoAtUCLSt[0])

                    LogsServices.write(f'atID: {atID}')
                    LogsServices.write(f'atType: {atType}')
                    tanqueToExit = TanksInService.select().where(TanksInService.atID == atID, TanksInService.atTipo == atType).order_by(TanksInService.id.desc()).first()
                    
                    registerInService = True
                    if tanqueToExit is None:

                        tanqueToExit = Tank.select().where(Tank.atId == atID, Tank.atTipo == atType).first()
                        if tanqueToExit is None:
                            continue
                        registerInService = False
                    
                    
                    LogsServices.write(f'tanqueToExit.id: {tanqueToExit.id}')
                    LogsServices.write(f'Registrado en servicio {registerInService}')
                    volumen = OpcServices.readDataPLC(getVolumenLlenadera(llenadera.numero))
                    volumenBls = volumen / 158.9873
                    volumenBlsTruncado = int(volumenBls * 1000) / 1000
                    volumen20 = OpcServices.readDataPLC(getVolumenCorrLlenadera(llenadera.numero))
                    volumen20Bls = volumen20 / 158.9873
                    volumen20BlsTruncado = int(volumen20Bls * 1000) / 1000
                    masa = OpcServices.readDataPLC(getMasaCorrLlenadera(llenadera.numero))
                    masaTons = masa / 1000
                    densidad = OpcServices.readDataPLC(getDensidadLlenadera(llenadera.numero)) / 10000
                    densidad20 = OpcServices.readDataPLC(getDensidadCorrLlenadera(llenadera.numero)) / 10000
                    porcentaje = OpcServices.readDataPLC(getPorcentajeLlenadera(llenadera.numero)) / 100
                    temperatura = OpcServices.readDataPLC(getTemperaturaLlenadera(llenadera.numero)) / 100
                    presion = OpcServices.readDataPLC(getPresionLlenadera(llenadera.numero)) / 100
                    modo = OpcServices.readDataPLC(getModoLlenadera(llenadera.numero))
                    anioInicio = OpcServices.readDataPLC(getAnioInicioLlenadera(llenadera.numero))
                    mesInicio = OpcServices.readDataPLC(getMesInicioLlenadera(llenadera.numero))
                    diaInicio = OpcServices.readDataPLC(getDiaInicioLlenadera(llenadera.numero))
                    horaInicio = OpcServices.readDataPLC(getHoraInicioLlenadera(llenadera.numero))
                    minutoInicio = OpcServices.readDataPLC(getMinutoInicioLlenadera(llenadera.numero))
                    horaFin = OpcServices.readDataPLC(getHoraFinLlenadera(llenadera.numero))
                    minutoFin = OpcServices.readDataPLC(getMinutoFinLlenadera(llenadera.numero))

                    now = datetime.now()
                    fecha =  now.strftime("%Y-%m-%d")
                    fechaFin = f"{fecha} {horaFin}:{minutoFin}:00"
                    tipoCarga = 1 if masa > 0 else 0

                    fechaEntrada = ''
                    fechaInicio = ''
                    if tipoCarga == 1 :
                        
                        if registerInService == True:
                            LogsServices.write(f'tanqueToExit.atName: {tanqueToExit.atName}')
                            LogsServices.write(f'tanqueToExit.fechaEntrada: {tanqueToExit.fechaEntrada}')
                            LogsServices.write(f'tanqueToExit.horaEntrada: {tanqueToExit.horaEntrada}')

                            fechaEntrada = f'{tanqueToExit.fechaEntrada} {tanqueToExit.horaEntrada}'
                            fechaInicio = datetime(anioInicio, mesInicio, diaInicio, horaInicio, minutoInicio, 0)
                            report24 = tanqueToExit.reporte24
                            report05 = tanqueToExit.reporte05
                            producto = tanqueToExit.productoNombre
                            productDescripcion = tanqueToExit.productoDescripcion
                            atID = tanqueToExit.atID
                            embarque = tanqueToExit.embarque
                            capacidad = tanqueToExit.capacidad
                        else:
                            fechaEntrada = now.strftime("%Y-%m-%d %H:%M:%S")
                            fechaInicio = datetime(anioInicio, mesInicio, diaInicio, horaInicio, minutoInicio, 0)
                            fechaInicioStr = fechaInicio.strftime('%Y-%m-%d %H:%M:%S')
                            report05 = obtenerFecha05Reporte(int(horaFin), fecha)
                            report24 = obtenerFecha24Reporte(int(horaFin), fecha)
                            producto = 'Propano'
                            productDescripcion = 'Gas L.P.'
                            atID = tanqueToExit.atId
                            embarque = 0
                            capacidad = tanqueToExit.capacidad90
                        
                        #LogsServices.write(f"fechaEntrada: {fechaEntrada}")
                        #LogsServices.write(f"fechaInicio: {fechaInicio}")

                        # Llenar datos de llenadera
                        salida = TankInTrucks.create(
                            productoNombre = producto,
                            productoDescripcion = productDescripcion,
                            atId = atID,
                            atTipo = tanqueToExit.atTipo,
                            atName = tanqueToExit.atName,
                            conector = tanqueToExit.conector,
                            embarque = embarque,
                            capacidad = capacidad,
                            capacidadStd = capacidad - volumen,
                            llenadera = llenadera.numero,
                            folioPLC = folioLlenadera,
                            volNatLts = volumen,
                            volNatBls = volumenBlsTruncado,
                            volCorLts = volumen20,
                            volCorBls = volumen20BlsTruncado,
                            masa = masa,
                            masaTons = masaTons,
                            densidadNat = densidad,
                            densidadCor = densidad20,
                            porcentaje = porcentaje,
                            temperaturaBase = 20,
                            temperatura = temperatura,
                            presion = presion,
                            modo = modo,
                            fechaEntrada = fechaEntrada,
                            fechaInicio = fechaInicio,
                            fechaFin = fechaFin,
                            reporte24 =  report24,
                            reporte05 =  report05,
                            tipoCarga = tipoCarga,
                            turno05 = obtenerTurno05(int(horaFin) + 1),
                            turno24 = obtenerTurno24(int(horaFin) + 1)
                        )
                        if registerInService == True:
                            tanqueToExit.delete_instance()
                        # Liberar llenadera
                        OpcServices.writeOPC(getFolioGuardadoLlenadera(llen), folioLlenadera)
                        #LogsServices.write(f'salida: {salida.atName} | {salida.atId} | {salida.atTipo} | {salida.conector} | {salida.capacidad} | {volumen} | {volumen20} | Folio: {salida.folioPLC} | llenadera: {salida.llenadera}')
                        

                        # Actualizar Folio de llenadera
                        folioLlen = Folio.select().where(Folio.llenadera == llenadera.id).first()
                        folioLlen.folio = folioLlenadera
                        folioLlen.save()

                        # Guardar registro en ultimas salidas
                        tanqueLastExit = TankExit.select().where(TankExit.id == 1).first()
                        tanqueLastExit.productoNombre = salida.productoNombre
                        #LogsServices.write(salida.productoNombre)
                        tanqueLastExit.productoDescripcion = salida.productoNombre
                        #LogsServices.write(salida.productoDescripcion)
                        tanqueLastExit.atId = salida.atId
                        #LogsServices.write(salida.atId)
                        tanqueLastExit.atTipo = salida.atTipo
                        #LogsServices.write(salida.atTipo)
                        tanqueLastExit.atName = salida.atName
                        #LogsServices.write(salida.atName)
                        tanqueLastExit.conector = salida.conector
                        #LogsServices.write(salida.conector)
                        tanqueLastExit.embarque = salida.embarque
                        #LogsServices.write(salida.embarque)
                        tanqueLastExit.capacidad = salida.capacidad
                        #LogsServices.write(salida.capacidad)
                        tanqueLastExit.capacidadStd = salida.capacidadStd
                        #LogsServices.write(salida.capacidadStd)
                        tanqueLastExit.masa = salida.masa
                        #LogsServices.write(salida.masa)
                        tanqueLastExit.fechaSalida = salida.fechaFin
                        #LogsServices.write(salida.fechaFin)
                        tanqueLastExit.save()
                        # Mandar error al grabar la ultima salida.
                        # ---------------------------------------
                        # ---------------------------------------
                        #LogsServices.write(f'tanqueLastExit: {tanqueLastExit.atName} | {tanqueLastExit.atId} | {tanqueLastExit.atTipo} | {tanqueLastExit.conector} | {tanqueLastExit.capacidad} | {tanqueLastExit.fechaSalida}')
                        #LogsServices.write(f'************************************')
                    else:
                        #LogsServices.write(f'llen: {llen}')
                        #LogsServices.write(f'Carga No Valida')
                        #LogsServices.write(f'************************************')
                        print(f'Carga No Valida')
                else:
                    #LogsServices.write(f'llen: {llen}')
                    #LogsServices.write(f'-----------NO Registrar Carga----------')
                    print(f'-----------NO Registrar Carga----------')
                    #LogsServices.write(f'Llenadera {llenadera.numero} con folio plc {folioLlenadera} - folio BD: {folioDB.folio}')
                    #LogsServices.write(f'************************************')
    except Exception as e:
        LogsServices.write(f'Error: {e}')
        return JSONResponse(
            status_code=201,
            content={"message": str(e)}
        )


def getPathAsignarLlenadera(llenadera):
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
async def get_llenadera_libre():
    try:
        tabla_llenaderas = {
            "5": getPLCLlenaderaLibre(5), 
            "6": getPLCLlenaderaLibre(6), 
            "7": getPLCLlenaderaLibre(7), 
            "8": getPLCLlenaderaLibre(8), 
            "9": getPLCLlenaderaLibre(9), 
            "10": getPLCLlenaderaLibre(10), 
            "11": getPLCLlenaderaLibre(11), 
            "12": getPLCLlenaderaLibre(12), 
            "13": getPLCLlenaderaLibre(13), 
            "14": getPLCLlenaderaLibre(14),
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
    

@router.get('/disponible')
async def get_llenadera_disponible():
    try:
        LogsServices.setNameFile()
        llenaderaDisponible = OpcServices.readDataPLC(path_llenaderaDisponible)
        if llenaderaDisponible is None:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "OPC servidor no disponible.",
                    "llenaderaDisponible": 0
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "message": f"Llenadera disponible consultada correctamente.",
                "llenaderaDisponible": llenaderaDisponible
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={
                "sucess": False,
                "message": str(e)}
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
        LogsServices.write('------------------ Desasignar Llenadera ------------------')
        LogsServices.write(f"llenadera: {llenadera}")
        # obtener si la llenadera esta libre
        strLibre = getPLCLlenaderaLibre(llenadera)
        LogsServices.write(f"rutaOPC: {strLibre}")
        if strLibre is False:
            return JSONResponse(
                status_code=401,
                content={"message": "Debe proporcionar un numero correcto de llenadera."}
            )
        libre = OpcServices.readDataPLC(strLibre)
        LogsServices.write(f"libre: {libre}")
        #libre = True
        # obtener el turno de la llenadera
        
        strTurno = getPLCLlenaderaTurno(llenadera)
        LogsServices.write(f"rutaOCP - turno : {strTurno}")
        turno = OpcServices.readDataPLC(strTurno)
        LogsServices.write(f"turno: {turno}")
        #turno = 0

        # si la llenadera esta libre y el turno es menor o igual a cero -> se debe modificar la llenadera
        if libre == 1 and turno <= 0:
            LogsServices.write('Libre true y turno cero')

            strDesasignar = getPLCLlenaderaDesasignar(llenadera)
            OpcServices.writeOPC(strDesasignar, llenadera)
            return JSONResponse(
                status_code=201,
                content={"message": f"El estatus de la llenadera {llenadera} se ha actualizado, PLC liberará llenadera."}
            )

        
        # si la llenadera esta libre y el turno es mayor a cero -> enviar mensaje que ya esta deasignada
        elif libre is True and turno > 0:
            LogsServices.write(f"La llenadera {llenadera} ya se encuentra disponible.")
            return JSONResponse(
                status_code=201,
                content={"message": f"La llenadera {llenadera} ya se encuentra disponible."}
            )
        # de lo contrario enviar que se realice de forma manual
        else:
            LogsServices.write(f"La llenadera {llenadera} no se encuentra liberada en el SCD, debe resetear la secuencia.")
            return JSONResponse(
                status_code=201,
                content={"message": f"La llenadera {llenadera} no se encuentra liberada en el SCD, debe resetear la secuencia."}
            )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": f"{str(e)} - No se pudo desasignar la llenadera."}
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


def getPLCLlenaderaTipo(llenadera):
    llenaderas = {
        5: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TIPO_AT_LLEN05",
        6: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TIPO_AT_LLEN06",
        7: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TIPO_AT_LLEN07",
        8: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TIPO_AT_LLEN08",
        9: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TIPO_AT_LLEN09",
        10: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TIPO_AT_LLEN10",
        11: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TIPO_AT_LLEN11",
        12: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TIPO_AT_LLEN12",
        13: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TIPO_AT_LLEN13",
        14: "GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TIPO_AT_LLEN14"
    }

    return llenaderas.get(llenadera, False)


def getPLCVolumenLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.VOL_LLEN5',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.VOL_LLEN6',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.VOL_LLEN7',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.VOL_LLEN8',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.VOL_LLEN9',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.VOL_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.VOL_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.VOL_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.VOL_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.VOL_LLEN14'
    }
    return tabla_llenaderas.get(llenadera, 0 )


def getPLCNipLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.NIP_LLEN5',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.NIP_LLEN6',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.NIP_LLEN7',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.NIP_LLEN8',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.NIP_LLEN9',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.NIP_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.NIP_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.NIP_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.NIP_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.NIP_LLEN14'
    }
    return tabla_llenaderas.get(llenadera, 0 )


def getPLCPGLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.PG-LLEN5',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.PG-LLEN6',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.PG-LLEN7',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.PG-LLEN8',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.PG-LLEN9',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.PG-LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.PG-LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.PG-LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.PG-LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Asignacion.PG-LLEN14'
    }
    return tabla_llenaderas.get(llenadera, 0 )


def getFolioLllenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getFolioGuardadoLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.DATOSGUARDADOS_LLEN14'
    }

    return tabla_llenaderas.get(llenadera, 0 )


def getVolumenLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_NAT_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_NAT_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_NAT_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_NAT_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_NAT_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_NAT_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_NAT_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_NAT_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_NAT_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_NAT_LLEN14'
    }

    return tabla_llenaderas.get(llenadera, 0 )


def getVolumenCorrLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_COR_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_COR_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_COR_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_COR_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_COR_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_COR_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_COR_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_COR_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_COR_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.VOL_CARGA_COR_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getMasaCorrLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.WI_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.WI_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.WI_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.WI_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.WI_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.WI_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.WI_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.WI_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.WI_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.WI_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getDensidadLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_NAT_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_NAT_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_NAT_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_NAT_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_NAT_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_NAT_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_NAT_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_NAT_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_NAT_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_NAT_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getDensidadCorrLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_COR_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_COR_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_COR_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_COR_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_COR_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_COR_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_COR_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_COR_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_COR_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DENS_COR_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getPorcentajeLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PORC_LLEN_FIN_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PORC_LLEN_FIN_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PORC_LLEN_FIN_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PORC_LLEN_FIN_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PORC_LLEN_FIN_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PORC_LLEN_FIN_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PORC_LLEN_FIN_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PORC_LLEN_FIN_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PORC_LLEN_FIN_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PORC_LLEN_FIN_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getTemperaturaLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TI_PROM_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TI_PROM_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TI_PROM_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TI_PROM_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TI_PROM_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TI_PROM_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TI_PROM_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TI_PROM_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TI_PROM_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.TI_PROM_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getPresionLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PI_PROM_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PI_PROM_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PI_PROM_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PI_PROM_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PI_PROM_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PI_PROM_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PI_PROM_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PI_PROM_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PI_PROM_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.PI_PROM_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )

def getModoLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MODO_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MODO_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MODO_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MODO_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MODO_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MODO_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MODO_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MODO_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MODO_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MODO_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getAnioInicioLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.ANO_INI_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.ANO_INI_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.ANO_INI_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.ANO_INI_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.ANO_INI_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.ANO_INI_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.ANO_INI_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.ANO_INI_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.ANO_INI_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.ANO_INI_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getMesInicioLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MES_INI_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MES_INI_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MES_INI_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MES_INI_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MES_INI_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MES_INI_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MES_INI_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MES_INI_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MES_INI_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MES_INI_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getDiaInicioLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DIA_INI_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DIA_INI_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DIA_INI_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DIA_INI_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DIA_INI_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DIA_INI_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DIA_INI_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DIA_INI_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DIA_INI_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.DIA_INI_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getHoraInicioLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_INI_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_INI_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_INI_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_INI_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_INI_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_INI_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_INI_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_INI_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_INI_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_INI_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getMinutoInicioLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_INI_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_INI_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_INI_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_INI_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_INI_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_INI_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_INI_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_INI_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_INI_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_INI_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getHoraFinLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_FIN_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_FIN_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_FIN_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_FIN_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_FIN_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_FIN_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_FIN_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_FIN_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_FIN_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.HORA_FIN_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getMinutoFinLlenadera(llenadera):
    tabla_llenaderas = {
        5: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_FIN_LLEN05',
        6: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_FIN_LLEN06',
        7: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_FIN_LLEN07',
        8: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_FIN_LLEN08',
        9: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_FIN_LLEN09',
        10: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_FIN_LLEN10',
        11: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_FIN_LLEN11',
        12: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_FIN_LLEN12',
        13: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_FIN_LLEN13',
        14: 'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.MIN_FIN_LLEN14'
    }
    
    return tabla_llenaderas.get(llenadera, 0 )


def getSufijoTanque(atTipo):
    tabla_tipos = {
        0: '',
        1: 'A',
        2: 'B',
    }
    
    return tabla_tipos.get(atTipo, 0 )



