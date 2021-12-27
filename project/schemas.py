from pydantic import BaseModel

class UserBaseModel(BaseModel):
    username: str
    password: str
    categoria: int
    departamento: str