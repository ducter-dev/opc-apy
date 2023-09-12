from datetime import date, datetime, time
from typing import Any, List, Generic
from pydantic import field_validator
from pydantic import BaseModel
from pydantic.utils import GetterDict
from peewee import ModelSelect


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):

        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return List

        return res

class ResponseModel(BaseModel):
    class ConfigDict:
        from_attributes = True
        getter_dict = PeeweeGetterDict


""" class UserValidator():
    @field_validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 20:
            raise ValueError('La longitud debe ser entre 3 y 20 caracteres.')

        return username
    

    @field_validator('password')
    def password_validator(cls, password):
        if len(password) < 8 or len(password) > 16:
            raise ValueError('La longitud debe ser entre 8 y 16 caracteres.')

        return password
    

    @field_validator('categoria')
    def categoria_validator(cls, categoria):
        if categoria < 1:
            raise ValueError('La categoría debe ser mayor a 0.')

        return categoria


    @field_validator('departamento')
    def departamento_validator(cls, departamento):
        if departamento < 1:
            raise ValueError('El departamento debe ser mayor a 0.')

        return departamento
"""


# --------- user ---------
class UserRequestModel(BaseModel):
    nombre: str
    username: str
    email: str
    categoria: int
    departamento: int

class UserResponseModel(ResponseModel):
    id: int
    nombre: str
    username: str
    email: str
    categoria: int
    departamento: int


class UserRequestPutModel(BaseModel):
    nombre: str
    username: str
    email: str
    categoria: int
    departamento: int

class UserChangePasswordRequestModel(BaseModel):
    id: int
    password: str

class UserRecuperePasswordRequestModel(BaseModel):
    email: str


# --------- TanksWaiting ---------
class TankWaitingRequestModel(BaseModel):
    posicion: int
    atId: int
    atTipo: int
    atName: str
    embarque: int
    capacidad: int
    conector: int

class TankWaitingResponseModel(ResponseModel):
    id: int
    posicion: int
    atId: int
    atTipo: int
    atName: str
    embarque: int
    capacidad: int
    conector: int
    horaEntrada: time
    fechaEntrada: date
    reporte24: date
    reporte05: date

class TankWaitingRequestPutModel(BaseModel):
    posicion: int
    atId: int
    atTipo: int
    atName: str
    password: int
    embarque: int
    capacidad: int
    conector: int

class TankWaitingRequestMovModel(BaseModel):
    inicial: int
    destino: int

class TankWaitingRequestPosicionPutModel(BaseModel):
    tanque: str

# --------- TanksEntry ---------
class TanksEntryRequestModel(BaseModel):
    posicion: int
    atId: int
    atTipo: int
    atName: str
    capacidad: int
    conector: int
    
class TanksEntryResponseModel(ResponseModel):
    id: int
    posicion: int
    atId: int
    atTipo: int
    atName: str
    capacidad: int
    conector: int
    horaEntrada: time
    fechaEntrada: date
    reporte24: date
    reporte05: date

class TanksLastEntryResponseModel(ResponseModel):
    id: int
    posicion: int
    atId: int
    atTipo: int
    atName: str
    capacidad: int
    conector: int
    fechaEntrada: datetime

# --------- TanksService ---------
class TanksInServiceRequestModel(BaseModel):
    productoNombre: str
    productoDescripcion: str
    atID: int
    atTipo: int
    atName: str
    claveCarga: int
    conector: int
    embarque: int
    capacidad: int
    estandar: int
    commSAP: int
    estatus: int
    llenadera: int
    horaEntrada: str
    fechaEntrada: str
    reporte24: str
    reporte05: str

class TanksInServiceResponseModel(ResponseModel):
    id: int
    productoNombre: str
    productoDescripcion: str
    atID: int
    atTipo: int
    atName: str
    claveCarga: int
    conector: int
    embarque: int
    capacidad: int
    estandar: int
    commSAP: int
    estatus: int
    llenadera: int
    horaEntrada: time
    fechaEntrada: date
    reporte24: date
    reporte05: date

class TanksLastAssignResponseModel(ResponseModel):
    id: int
    posicion: int
    atId: int
    atTipo: int
    atName: str
    volProg: int
    conector: int
    embarque: int
    password: int
    fecha: datetime
    llenadera: int

# --------- TanksCargados ---------
class TankInTrucksRequestModel(BaseModel):
    productoNombre: str
    productoDescripcion: str
    atId: int
    atTipo: int
    atName: str
    conector: int
    embarque: int
    capacidad: int
    estandarCapacidad: int
    commSAP: int
    respuestaMsgA: str
    respuestaMsgB: str
    respuestaMsgI: str
    atEstatus: int
    llenadera: int
    folioPLC: int
    volNatLts: int
    volNatBls: float
    volCorLts: int
    volCorBls: float
    masa: int
    masaTons: float
    densidadNat: float
    densidadCor: float
    porcentaje: float
    temperaturaBase: float
    temperatura: float
    presion: float
    modo: str
    fechaEntrada: str
    fechaInicio: str
    fechaFin: str
    reporte24: str
    reporte05: str
    tipoCarga: int

class TankInTrucksResponseModel(ResponseModel):
    id: int
    productoNombre: str
    productoDescripcion: str
    atId: int
    atTipo: int
    atName: str
    conector: int
    embarque: int
    capacidad: int
    capacidadStd: int
    llenadera: int
    folioPLC: int
    volNatLts: int
    volNatBls: float
    volCorLts: int
    volCorBls: float
    masa: int
    masaTons: float
    densidadNat: float
    densidadCor: float
    porcentaje: float
    temperaturaBase: float
    temperatura: float
    presion: float
    modo: str
    fechaEntrada: datetime
    fechaInicio: datetime
    fechaFin: datetime
    tipoCarga: int

class TanksLastExitResponseModel(ResponseModel):
    id: int
    atId: int
    atTipo: int
    atName: str
    capacidad: int
    capacidadStd: int
    conector: int
    fechaSalida: datetime

# --------- TankAsignado ---------
class TankAssignRequestModel(BaseModel):
    atNum: int
    atTipo: int
    atName: str
    volProg: int
    conector: int
    embarque: int
    password: int
    fecha: str
    llenadera: int
    posicion: int

class TankAssignResponseModel(ResponseModel):
    id: int
    atNum: int
    atTipo: int
    atName: str
    volProg: int
    conector: int
    embarque: int
    password: int
    fecha: datetime
    llenadera: int
    posicion: int

# --------- Tank ---------
class TankRequestModel(BaseModel):
    atId: int
    atTipo: int
    atName: str
    conector: int
    capacidad90: int
    transportadora: int

class TankResponseModel(ResponseModel):
    id: int
    atId: int
    atTipo: int
    atName: str
    conector: int
    capacidad90: int
    transportadora: int


class TankSingleRequestModel(ResponseModel):
    tanque: str
    

# --------- Llenadera ---------
class LlenaderaRequestModel(BaseModel):
    numero: int
    conector: int
    tipo: int

class LlenaderaResponseModel(ResponseModel):
    id: int
    numero: int
    conector: int
    tipo: int

class LlenaderaWithEstadoResponseModel(ResponseModel):
    id: int
    numero: int
    conector: int
    tipo: int
    estado: int

class LlenaderaAsignarRequestModel(BaseModel):
    tanque: str


# --------- Bitacora ---------
class BitacoraRequestModel(BaseModel):
    user: int
    actividad: str
    evento: int

# --------- Eventos ---------
class EventoResponseModel(ResponseModel):
    id: int
    descripcion: str


# --------- Bitácora ---------
class BitacoraResponseModel(ResponseModel):
    id: int
    user: UserResponseModel
    actividad: str
    evento: EventoResponseModel
    fecha: datetime
    ubicacion: str
    reporte05: date
    reporte24: date


# --------- RelojPLC ---------
class RelojPLCRequestModel(BaseModel):
    year: int
    month: int
    day: int
    hours: int
    mins: int
    secs: int

class RelojPLCResponseModel(ResponseModel):
    id: int
    year: int
    month: int
    day: int
    hours: int
    mins: int
    secs: int

# --------- Barrera ---------
class BarreraRequesteModel(BaseModel):
    estado: bool


# --------- Estado Llenadera ---------
class EstadoLlenaderaRequesteModel(BaseModel):
    estado: int


# --------- Numero Llenadera ---------
class NumeroLlenaderaRequesteModel(BaseModel):
    llenadera: int


# --------- folios ---------
class FoliosRequestModel(BaseModel):
    llenadera_id: int
    folio: int


class FoliosResponseModel(ResponseModel):
    id: int
    folio: int
    llenadera: LlenaderaResponseModel

class BloqueadosRequestModel(BaseModel):
    user: str

class BloqueadosResponseModel(ResponseModel):
    id: int
    user: UserResponseModel
    fechaBloqueo: datetime
    fechaDesbloqueo: datetime

class BloqueadosUserRequestModel(BaseModel):
    usuario: str


class FechaReportesRequestModel(BaseModel):
    fecha: str


# --------- esferas ---------
class EsferaRequestModel(BaseModel):
    hora: int
    presion: float
    temperatura: float
    densidad: float
    densidadCor: float
    volumenBlsNat: float
    volumenBlsCor: float
    volumenTon: float
    porcentaje: float
    nivel: float
    volumenNatDisp: float
    volumenCorDisp: float
    volumenTonDisp: float
    esfera: int
    fecha: str
    reporte05: str
    turno05: int
    reporte24: str
    turno24: int

class EsferaResponseModel(ResponseModel):
    id: int
    hora: str
    presion: float
    temperatura: float
    densidad: float
    densidadCor: float
    volumenBlsNat: float
    volumenBlsCor: float
    volumenTon: float
    porcentaje: float
    nivel: float
    volumenNatDisp: float
    volumenCorDisp: float
    volumenTonDisp: float
    esfera: int
    fecha: datetime
    reporte05: date
    turno05: int
    reporte24: date
    turno24: int



# --------- patines ---------
class PatinRequestModel(BaseModel):
    hora: int
    presion: float
    flujoVolumen: float
    flujoMasico: float
    temperatura: float
    densidadNat: float
    densidadCor: float
    volUnc: float
    blsNat: float
    blsCor: float
    ton: float
    patin: int
    totalizadorBlsNat: float
    totalizadorBlsCor: float
    totalizadorMassTon: float
    fecha: str
    reporte05: str
    turno05: int
    reporte24: str
    turno24: int

class PatinResponseModel(ResponseModel):
    id: int
    hora: str
    presion: float
    flujoVolumen: float
    flujoMasico: float
    temperatura: float
    densidadNat: float
    densidadCor: float
    volUnc: float
    blsNat: float
    blsCor: float
    ton: float
    patin_id: int
    totalizadorBlsNat: float
    totalizadorBlsCor: float
    totalizadorMassTon: float
    fecha: datetime
    reporte05: date
    turno05: int
    reporte24: date
    turno24: int

class CromatografoResponseModel(ResponseModel):
    id: int
    hora: str
    cromatrografo: str
    corriente: int
    c6: float
    propano: float
    propileno: float
    iButano: float
    nButano: float
    c4: float
    iPentano: float
    nPentano: float
    metano: float
    etileno: float
    etano: float
    olefinas: float
    corriente: int
    fecha: datetime
    reporte05: date
    turno05: int
    reporte24: date
    turno24: int

class BombaResponseModel(ResponseModel):
    id: int
    hora: str
    bomba: str
    estatus: str
    totalHorasOper: int
    totalMinsOper: int
    totalTiempoOper: str
    horasOper: int
    minsOper: int
    enOper: int
    horasMantto: int
    minsMantto: int
    enMantto: str
    horasDisp: int
    minsDisp: int
    enDisp: str
    horasNoDisp: int
    minsNoDisp: int
    enNoDisp: str
    fecha: datetime
    reporte05: date
    turno05: int
    reporte24: date
    turno24: int


# ---- Densidades ----
class DensidadResponseModel(ResponseModel):
    id: int
    hora: str
    fecha: datetime
    presSupEsf1: float
    presInfEsf1: float
    presSupEsf2: float
    presInfEsf2: float
    densNatEsf1: float
    densNatEsf2: float
    densitometro: float
    cromatografo: float
    analisisCrom: float
    reporte05: date
    reporte24: date