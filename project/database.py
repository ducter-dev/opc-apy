import base64
import bcrypt
from peewee import *
from datetime import datetime
import os
from os.path import join,dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE_DB = os.environ.get('DATABASE_DB')
USER_DB = os.environ.get('USER_DB')
PASSWORD_DB = os.environ.get('PASSWORD_DB')
HOST_DB = os.environ.get('HOST_DB')
PORT_DB = os.environ.get('PORT_DB')

database = MySQLDatabase(DATABASE_DB, 
                        user=USER_DB, 
                        password=PASSWORD_DB, 
                        host=HOST_DB,
                        port=int(PORT_DB))


class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField()
    categoria = IntegerField(default=3)
    departamento = IntegerField(default=3)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username

    class Meta:
        database = database
        table_name = 'users'

    @classmethod
    def create_password(cls, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed

    @classmethod
    def validate_password(cls, password, hashed):
        result = bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        return result

class Tank(Model):
    atId =  IntegerField(null=True)
    atTipo =  IntegerField(null=True)
    atName = CharField(12, null=True)
    conector =  IntegerField(null=True)
    capacidad90 =  IntegerField(null=True)
    transportadora = IntegerField(null=True)
    created_at =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return self.atId

    class Meta:
        database = database
        table_name = 'autotanques'


class TankWaiting(Model):
    posicion =  IntegerField(null=True)
    atId =  IntegerField(null=True)
    atTipo =  IntegerField(null=True)
    atName = CharField(12, null=True)
    password =  IntegerField(null=True)
    embarque =  IntegerField(null=True)
    capacidad =  IntegerField(null=True)
    conector =  IntegerField(null=True)
    horaEntrada =  TimeField(default=datetime.now, formats='%H:%M:%S')
    fechaEntrada =  DateField(default=datetime.now, formats='%Y-%m-%d')
    reporte24 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    reporte05 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    created_at =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return self.atId

    class Meta:
        database = database
        table_name = 'lista_espera'

class TankEntry(Model):
    posicion =  IntegerField(null=True)
    atId =  IntegerField(null=True)
    atTipo =  IntegerField(null=True)
    atName = CharField(12, null=True)
    capacidad =  IntegerField(null=True)
    conector =  IntegerField(null=True)
    horaEntrada =  TimeField(default=datetime.now, formats='%H:%M:%S')
    fechaEntrada =  DateField(default=datetime.now, formats='%Y-%m-%d')
    reporte24 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    reporte05 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    created_at =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return self.atId

    class Meta:
        database = database
        table_name = 'lista_entrada'

class TankInService(Model):
    productoNombre = CharField(45, null=True)
    productoDescripcion = CharField(100, null=True)
    atID = IntegerField(null=True)
    atTipo =  IntegerField(null=True)
    atName = CharField(12, null=True)
    claveCarga = IntegerField(null=True)
    conector = IntegerField(null=True)
    embarque = IntegerField(null=True)
    capacidad = IntegerField(null=True)
    estandar = IntegerField(null=True)
    commSAP = IntegerField(null=True)
    estatus = IntegerField(null=True)
    llenadera = IntegerField(null=True)
    horaEntrada = TimeField(default=datetime.now, formats='%H:%M:%S')
    fechaEntrada = DateField(default=datetime.now, formats='%Y-%m-%d')
    reporte24 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    reporte05 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = database
        table_name = 'lista_servicio'

class TankInTrucks(Model):
    productoNombre = CharField(45, null=True)
    productoDescripcion = CharField(100, null=True)
    atID = IntegerField(null=True)
    atTipo = IntegerField(null=True)
    atName = CharField(12, null=True)
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
    reporte24 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    reporte05 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    tipoCarga = IntegerField(null=True)
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = database
        table_name = 'lista_salida'

class TankAssign(Model):
    atNum = IntegerField(null=True)
    atTipo = IntegerField(null=True)
    atName = CharField(12, null=True)
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

# ----- Llenaderas -----
class Llenadera(Model):
    numero = IntegerField(null=True)
    conector = IntegerField(null=True)
    tipo = IntegerField(null=True)

    class Meta:
        database = database
        table_name = 'llenaderas'


# ----- Bitacora -----
class Bitacora(Model):
    usuario = CharField(50)
    actividad = CharField()
    ubicacion = CharField(50)
    fecha = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    reporte24 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    reporte05 =  DateField(default=datetime.now, formats='%Y-%m-%d')

    class Meta:
        database = database
        table_name = 'bitacora'


# ----- Reloj -----
class RelojPLC(Model):
    year = IntegerField(null=True)
    month = IntegerField(null=True)
    day = IntegerField(null=True)
    hours = IntegerField(null=True)
    mins = IntegerField(null=True)
    secs = IntegerField(null=True)

    class Meta:
        database = database
        table_name = "relojPLC"


# ----- Folios -----
class Folio(Model):
    llenadera = ForeignKeyField(Llenadera)
    folio = IntegerField()
    
    class Meta:
        database = database
        table_name = "folios"

