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

class UserResponseModel(BaseModel):
    id: int
    username: str

    class Config:
      orm_mode = True
      getter_dict = PeeweeGetterDict