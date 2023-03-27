from datetime import date, datetime, time
from typing import Any, List
from pydantic import validator
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
    class Config:
      orm_mode = True
      getter_dict = PeeweeGetterDict


class UserValidator():
    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 20:
            raise ValueError('La longitud debe ser entre 3 y 20 caracteres.')

        return username
    

    @validator('password')
    def password_validator(cls, password):
        if len(password) < 8 or len(password) > 16:
            raise ValueError('La longitud debe ser entre 8 y 16 caracteres.')

        return password
    

    @validator('categoria')
    def categoria_validator(cls, categoria):
        if categoria < 1:
            raise ValueError('La categoría debe ser mayor a 0.')

        return categoria


    @validator('departamento')
    def departamento_validator(cls, departamento):
        if departamento < 1:
            raise ValueError('El departamento debe ser mayor a 0.')

        return departamento



# --------- user ---------
class UserRequestModel(BaseModel, UserValidator):
    username: str
    password: str
    categoria: int
    departamento: int
    registra: int

class UserResponseModel(ResponseModel):
    id: int
    username: str
    categoria: int
    departamento: int

class UserRequestPutModel(BaseModel, UserValidator):
    username: str
    categoria: int
    departamento: str

class UserChangePasswordRequestModel(BaseModel, UserValidator):
    user_id: int
    password: str


# --------- TanksWaiting ---------
class TankWaitingRequestModel(BaseModel):
    posicion: int
    atId: int
    atTipo: int
    atName: str
    password: int
    embarque: int
    capacidad: int
    conector: int
    horaEntrada: str
    fechaEntrada: str
    reporte24: str
    reporte05: str

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
    horaEntrada: str
    fechaEntrada: str
    reporte24: str
    reporte05: str

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
    fechaEntrada: str
    
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
    fechaEntrada: date
    fechaInicio: date
    fechaFin: date
    reporte24: date
    reporte05: date
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
    usuario: str
    actividad: str
    ubicacion: str
    fecha: str
    reporte24: str
    reporte05:  str

class BitacoraResponseModel(ResponseModel):
    id: int
    usuario: str
    actividad: str
    ubicacion: str
    fecha: datetime
    reporte24: date
    reporte05: date


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
    estado: int


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
    fechaBloqueo: str

class BloqueadosResponseModel(ResponseModel):
    id: int
    user: UserResponseModel
    fechaBloqueo: datetime
    fechaDesbloqueo: datetime

class BloqueadosUserRequestModel(BaseModel):
    usuario: str