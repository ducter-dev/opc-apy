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


# --------- user ---------
class UserRequestModel(BaseModel):
    username: str
    password: str
    categoria: int
    departamento: str


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
        if len(departamento) < 3 or len(departamento) > 20:
            raise ValueError('El departamento debe ser entre 3 y 20 caracteres.')

        return departamento



class UserResponseModel(ResponseModel):
    id: int
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

class TankWaitingResponseModel(ResponseModel):
    id: int
    posicion: int
    atId: int
    atTipo: int
    atName: str
    embarque: int
    capacidad: int
    conector: int
    horaEntrada: str
    fechaEntrada: str

class TankInServiceRequestModel(BaseModel):
    productoNombre: str
    productoDescripcion: str
    atID: int
    atTipo: int
    atName: str
    claveCarga: int
    conector: int
    Embarque: int
    capacidad: int
    estandar: int
    commSAP: int
    estatus: int
    llenadera: int
    horaEntrada: str
    fechaEntrada: str

class TankInServiceResponseModel(ResponseModel):
    id: int
    productoNombre: str
    productoDescripcion: str
    atID: int
    atTipo: int
    atName: str
    claveCarga: int
    conector: int
    Embarque: int
    capacidad: int
    estandar: int
    commSAP: int
    estatus: int
    llenadera: int
    horaEntrada: str
    fechaEntrada: str


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
    fechaJornada: str
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
    fechaEntrada: str
    fechaInicio: str
    fechaFin: str
    fechaSalida: str
    fechaJornada: str
    tipoCarga: int


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
    fecha: str
    llenadera: int
    posicion: int