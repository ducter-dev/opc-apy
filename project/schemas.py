from datetime import date, datetime, time
from typing import Any
from pydantic import validator
from pydantic import BaseModel
from pydantic.utils import GetterDict
from peewee import ModelSelect

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
      
      res = getattr(self._obj, key, default)
      if isinstance(res, ModelSelect):
        return list

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

class UserResponseModel(ResponseModel):
    id: int
    username: str
    categoria: int
    departamento: int

class UserRequestPutModel(BaseModel, UserValidator):
    username: str
    categoria: int
    departamento: str

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

# --------- TanksEntry ---------
class TankEntryRequestModel(BaseModel):
    posicion: int
    atId: int
    atTipo: int
    atName: str
    capacidad: int
    conector: int
    horaEntrada: str
    fechaEntrada: str
    reporte24: str
    reporte05: str

class TankEntryResponseModel(ResponseModel):
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

# --------- TanksService ---------
class TankInServiceRequestModel(BaseModel):
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


class TankInServiceResponseModel(ResponseModel):
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

# --------- TanksCargados ---------
class TankInTrucksRequestModel(BaseModel):
    productoNombre: str
    productoDescripcion: str
    atID: int
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
    fechaSalida: str
    reporte24: str
    reporte05: str
    tipoCarga: int

class TankInTrucksResponseModel(ResponseModel):
    id: int
    productoNombre: str
    productoDescripcion: str
    atID: int
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
    fechaEntrada: datetime
    fechaInicio: datetime
    fechaFin: datetime
    fechaSalida: datetime = None
    reporte24: date
    reporte05: date
    tipoCarga: int

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
    