import bcrypt
from peewee import *
from datetime import datetime

database = MySQLDatabase('scairge', 
                        user='remote_ducter', 
                        password='19Ducter2019$', 
                        host='localhost',
                        port=3306)


class User(Model):
  username = CharField(max_length=50, unique=True)
  password = CharField(max_length=50)
  categoria = IntegerField(default=3)
  departamento = CharField(max_length=50)
  created_at = DateTimeField(default=datetime.now)

  def __str__(self):
      return self.username

  class Meta:
      database = database
      table_name = 'users'

  @classmethod
  def create_password(cls, password):
      hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
      return hashed.hex()

class tanksWaiting(Model):
    posicion =  IntegerField(null=True)
    atId =  IntegerField(null=True)
    atTipo =  IntegerField(null=True)
    password =  IntegerField(null=True)
    embarque =  IntegerField(null=True)
    capacidad =  IntegerField(null=True)
    conector =  IntegerField(null=True)
    horaEntrada =  TimeField(default=datetime.now, formats='%H:%M:%S')
    fechaEntrada =  DateField(default=datetime.now, formats='%Y-%m-%d')
    created_at =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return self.atId

    class Meta:
        database = database
        table_name = 'lista_espera'

class tanksInService(Model):
    productoNombre = CharField(45, null=True)
    productoDescripcion = CharField(100, null=True)
    atID = IntegerField(null=True)
    atTipo =  IntegerField(null=True)
    atName = CharField(12, null=True)
    claveCarga = IntegerField(null=True)
    conector = IntegerField(null=True)
    Embarque = IntegerField(null=True)
    capacidad = IntegerField(null=True)
    estandar = IntegerField(null=True)
    commSAP = IntegerField(null=True)
    estatus = IntegerField(null=True)
    llenadera = IntegerField(null=True)
    horaEntrada = IntegerField(null=True)
    minEntrada = IntegerField(null=True)
    fechaEntrada = DateField(default=datetime.now, formats='%Y-%m-%d')
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = database
        table_name = 'lista_servicio'

class tanksInTrucks(Model):
    productoNombre = CharField(45, null=True)
    productoDescripcion = CharField(100, null=True)
    atID = IntegerField(null=True)
    atTipo = IntegerField(null=True)
    conector = IntegerField(null=True)
    embarque = IntegerField(null=True)
    capacidad = IntegerField(null=True)
    estandarCapacidad = IntegerField(null=True)
    commSAP = IntegerField(null=True)
    respuestaMsgA = CharField(10, null=True)
    respuestaMsgB = CharField(10, null=True)
    respuestaMsgI = CharField(10, null=True)
    atEstatus = IntegerField(null=True)
    llenadera = IntegerField(null=True)
    folioPLC = IntegerField(null=True)
    volNatLts = IntegerField(null=True)
    volNatBls = DoubleField(null=True)
    volCorLts = IntegerField(null=True)
    volCorBls = DoubleField(null=True)
    masa = IntegerField(null=True)
    masaTons = DoubleField(null=True)
    densidadNat = DoubleField(null=True)
    densidadCor = DoubleField(null=True)
    porcentaje = DoubleField(null=True)
    temperaturaBase = DoubleField(null=True)
    temperatura = DoubleField(null=True)
    presion = DoubleField(null=True)
    modo = CharField(45, null=True)
    fechaEntrada = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    fechaInicio = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    fechaFin = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    fechaSalida = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    fechaJornada = DateField(default=datetime.now, formats='%Y-%m-%d')
    tipoCarga = IntegerField(null=True)
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = database
        table_name = 'lista_cargas'

class lastAssign(Model):
    atNum = IntegerField(null=True)
    atTipo = IntegerField(null=True)
    volProg = IntegerField(null=True)
    conector = IntegerField(null=True)
    embarque = IntegerField(null=True)
    password = IntegerField(null=True)
    fecha = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    llenadera = IntegerField(null=True)
    posicion = IntegerField(null=True)

    class Meta:
        database = database
        table_name = 'ultima_asignacion'