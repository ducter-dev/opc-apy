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


# ---------- usuarios ---------- #
class User(Model):
    nombre = CharField()
    username = CharField(max_length=50, unique=True)
    password = CharField(unique=True)
    email = CharField()
    categoria = IntegerField(default=3)
    departamento = IntegerField(default=3)
    verificado = DateTimeField(null=True)
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


# ---------- bloqueados ---------- #
class Bloqueado(Model):
    user = ForeignKeyField(User, backref='usuarios')
    fechaBloqueo = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    fechaDesbloqueo = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    created_at =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return self.id

    class Meta:
        database = database
        table_name = 'bloqueados'


# ---------- contraseñas caducidad ---------- #
class Caducidad(Model):
    password = CharField()
    caducidad = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    ultimoAcceso = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    estado = IntegerField(default=1)
    user = ForeignKeyField(User, backref='usuarios')
    created_at =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return self.id

    class Meta:
        database = database
        table_name = 'caducidades'


# ---------- tanques ---------- #
class Tank(Model):
    atId =  IntegerField(null=True)
    atTipo =  IntegerField(null=True)
    atName = CharField(12, null=True)
    conector = IntegerField(null=True)
    capacidad90 =  IntegerField(null=True)
    transportadora = IntegerField(null=True)
    created_at =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return self.atId

    class Meta:
        database = database
        table_name = 'autotanques'

# ---------- tanques en lista de espera ---------- #
class TankWaiting(Model):
    posicion =  IntegerField(null=True)
    atId =  IntegerField(null=True)
    atTipo =  IntegerField(null=True)
    atName = CharField(12, null=True)
    password =  IntegerField(null=True)
    embarque =  IntegerField(null=True)
    capacidad =  IntegerField(null=True)
    conector = IntegerField(null=True)
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


# ---------- tanques en entrada ---------- #

class TanksEntry(Model):
    posicion =  IntegerField(null=True)
    atId =  IntegerField(null=True)
    atTipo =  IntegerField(null=True)
    atName = CharField(12, null=True)
    capacidad =  IntegerField(null=True)
    conector = IntegerField(null=True)
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


# ---------- ultima Entrada ---------- #

class TankEntry(Model):
    posicion =  IntegerField(null=True)
    atId =  IntegerField(null=True)
    atTipo =  IntegerField(null=True)
    atName = CharField(12, null=True)
    capacidad =  IntegerField(null=True)
    conector = IntegerField(null=True)
    tipoEntrada = IntegerField(null=True)
    estatusSol = IntegerField(null=True)
    fechaEntrada = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = database
        table_name = 'ultima_entrada'


# ---------- tanques en servicio ---------- #

class TanksInService(Model):
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


# ---------- tanques en lista de salida ---------- #

class TankInTrucks(Model):
    productoNombre = CharField(45, null=True)
    productoDescripcion = CharField(100, null=True)
    atId = IntegerField(null=True)
    atTipo = IntegerField(null=True)
    atName = CharField(12, null=True)
    conector = IntegerField(null=True)
    embarque = IntegerField(null=True)
    capacidad = IntegerField(null=True)
    capacidadStd = IntegerField(null=True)
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
    turno05 = IntegerField(null=True)
    turno24 = IntegerField(null=True)
    tipoCarga = IntegerField(null=True)
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = database
        table_name = 'lista_salida'


# ---------- tanque ultima salida ---------- #
class TankExit(Model):
    productoNombre = CharField(45, null=True)
    productoDescripcion = CharField(100, null=True)
    atId = IntegerField(null=True)
    atTipo = IntegerField(null=True)
    atName = CharField(12, null=True)
    conector = IntegerField(null=True)
    embarque = IntegerField(null=True)
    capacidad = IntegerField(null=True)
    capacidadStd = IntegerField(null=True)
    masa = IntegerField(null=True)
    fechaSalida = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = database
        table_name = 'ultima_salida'

        
# ---------- tanque ultima asignacion ---------- #
class TankAssign(Model):
    atId = IntegerField(null=True)
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


# ----- Eventos -----
class Evento(Model):
    descripcion = CharField()

    class Meta:
        database = database
        table_name = 'eventos'


# ----- Bitacora -----
class Bitacora(Model):
    actividad = CharField()
    user = ForeignKeyField(User, backref='usuarios')
    evento = ForeignKeyField(Evento, backref='eventos')
    ubicacion = CharField()
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



# ----- Esfera -----
class Esfera(Model):
    hora = CharField()
    presion = DoubleField(null=True)
    temperatura = DoubleField(null=True)
    densidad = DoubleField(null=True)
    densidadCor = DoubleField(null=True)
    volumenBlsNat = DoubleField(null=True)
    volumenBlsCor = DoubleField(null=True)
    volumenTon = DoubleField(null=True)
    porcentaje = DoubleField(null=True)
    nivel = FloatField(null=True)
    volumenNatDisp = DoubleField(null=True)
    volumenCorDisp = DoubleField(null=True)
    volumenTonDisp = DoubleField(null=True)
    esfera = IntegerField(null=True)
    fecha =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    reporte05 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    turno05 = IntegerField(null=True)
    reporte24 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    turno24 = IntegerField(null=True)
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        database = database
        table_name = 'esferas'


class Patin(Model):
    descripcion = CharField()
    
    class Meta:
        database = database
        table_name = 'patines'

class PatinData(Model):
    hora = CharField()
    presion = DoubleField(null=True)
    flujoVolumen = DoubleField(null=True)
    flujoMasico = DoubleField(null=True)
    temperatura = DoubleField(null=True)
    densidadNat = DoubleField(null=True)
    densidadCor = DoubleField(null=True)
    volUnc = DoubleField(null=True)
    blsNat = DoubleField(null=True)
    blsCor = DoubleField(null=True)
    ton = DoubleField(null=True)
    patin = ForeignKeyField(Patin, backref='patines')
    totalizadorBlsNat = DoubleField(null=True)
    totalizadorBlsCor = DoubleField(null=True)
    totalizadorMassTon = DoubleField(null=True)
    fecha =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    reporte05 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    turno05 = IntegerField(null=True)
    reporte24 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    turno24 = IntegerField(null=True)
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    class Meta:
        database = database
        table_name = 'patin_data'


class Cromatografo(Model):
    hora = CharField()
    cromatografo = CharField()
    corriente: IntegerField(null=True)
    c6 = DoubleField(null=True)
    propano = DoubleField(null=True)
    propileno = DoubleField(null=True)
    iButano = DoubleField(null=True)
    nButano = DoubleField(null=True)
    c4 = DoubleField(null=True)
    iPentano = DoubleField(null=True)
    nPentano = DoubleField(null=True)
    metano = DoubleField(null=True)
    etileno = DoubleField(null=True)
    etano = DoubleField(null=True)
    olefinas = DoubleField(null=True)
    densidad = DoubleField(null=True)
    pentano = DoubleField(null=True)
    corriente = IntegerField(null=True)
    fecha =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    reporte05 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    turno05 = IntegerField(null=True)
    reporte24 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    turno24 = IntegerField(null=True)
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = database
        table_name = 'cromatografo'


class Bomba(Model):
    hora = CharField()
    bomba = CharField()
    estatus = CharField()
    totalHorasOper = IntegerField(null=True)
    totalMinsOper = IntegerField(null=True)
    totalTiempoOper = CharField()
    horasOper = IntegerField(null=True)
    minsOper = IntegerField(null=True)
    enOper = IntegerField(null=True)
    horasMantto = IntegerField(null=True)
    minsMantto = IntegerField(null=True)
    enMantto = CharField()
    horasDisp = IntegerField(null=True)
    minsDisp = IntegerField(null=True)
    enDisp = CharField()
    horasNoDisp = IntegerField(null=True)
    minsNoDisp = IntegerField(null=True)
    enNoDisp = CharField()
    fecha =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    reporte05 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    turno05 = IntegerField(null=True)
    reporte24 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    turno24 = IntegerField(null=True)
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = database
        table_name = 'bombas'


class BombaReporte(Model):
    hora = CharField()
    oper_ba301a = CharField()
    mantto_ba301a = CharField()
    stat_ba301a = CharField()
    oper_ba301b = CharField()
    mantto_ba301b = CharField()
    stat_ba301b = CharField()
    oper_ba301c = CharField()
    mantto_ba301c = CharField()
    stat_ba301c = CharField()

    class Meta:
        database = database
        table_name = 'bombas_reporte'


class TipoTanque(Model):
    tipo = IntegerField(null=True)
    descripcion = CharField()
    
    class Meta:
        database = database
        table_name = 'tipos_tanques'



class ConectorTanque(Model):
    descripcion = CharField()
    abreviatura = CharField()
    
    class Meta:
        database = database
        table_name = 'conectores_tanques'


class BalanceDiario(Model):
    turno = CharField()
    inicial_nat = DoubleField(null=True)
    inicial_cor = DoubleField(null=True)
    inicial_tons = DoubleField(null=True)
    recibo_nat = DoubleField(null=True)
    recibo_cor = DoubleField(null=True)
    recibo_tons = DoubleField(null=True)
    ventas_nat = DoubleField(null=True)
    ventas_cor = DoubleField(null=True)
    ventas_tons = DoubleField(null=True)
    ventas_pgs = IntegerField(null=True)
    final_nat = DoubleField(null=True)
    final_cor = DoubleField(null=True)
    final_tons = DoubleField(null=True)
    dif_nat = DoubleField(null=True)
    dif_cor = DoubleField(null=True)
    dif_tons = DoubleField(null=True)

    class Meta:
        database = database
        table_name = 'balance_diario'


class BalanceMensual(Model):
    dia = CharField()
    inicial_nat = DoubleField(null=True)
    inicial_cor = DoubleField(null=True)
    inicial_tons = DoubleField(null=True)
    recibo_nat = DoubleField(null=True)
    recibo_cor = DoubleField(null=True)
    recibo_tons = DoubleField(null=True)
    ventas_nat = DoubleField(null=True)
    ventas_cor = DoubleField(null=True)
    ventas_tons = DoubleField(null=True)
    ventas_pgs = IntegerField(null=True)
    final_nat = DoubleField(null=True)
    final_cor = DoubleField(null=True)
    final_tons = DoubleField(null=True)
    dif_nat = DoubleField(null=True)
    dif_cor = DoubleField(null=True)
    dif_tons = DoubleField(null=True)

    class Meta:
        database = database
        table_name = 'balance_mensual'



class ReportePatin(Model):
    medidor = CharField()
    toneladas = DoubleField(null=True)
    blsNat = DoubleField(null=True)
    blsCor = DoubleField(null=True)

    class Meta:
        database = database
        table_name = 'recibo_patin'

# Densidaddes
class Densidad(Model):
    hora = CharField()
    fecha =  DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    presSupEsf1 = DoubleField(null=True)
    presInfEsf1 = DoubleField(null=True)
    presSupEsf2 = DoubleField(null=True)
    presInfEsf2 = DoubleField(null=True)
    densNatEsf1 = DoubleField(null=True)
    densNatEsf2 = DoubleField(null=True)
    densitometro = DoubleField(null=True)
    cromatografo = DoubleField(null=True)
    analisisCrom = DoubleField(null=True)
    reporte05 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    reporte24 =  DateField(default=datetime.now, formats='%Y-%m-%d')
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = database
        table_name = 'densidades'


class Horas(Model):
    hora = IntegerField()
    referencia = CharField()

    class Meta:
        database = database
        table_name = 'hours_data'


class ReporteEsferas(Model):
    esfera = CharField()
    inicialBls = DoubleField(null=True)
    inicialBls20 = DoubleField(null=True)
    inicialTons = DoubleField(null=True)
    actualBls = DoubleField(null=True)
    actualBls20 = DoubleField(null=True)
    actualTons = DoubleField(null=True)
    diferenciaBls = DoubleField(null=True)
    diferenciaBls20 = DoubleField(null=True)
    diferenciaTons = DoubleField(null=True)

    class Meta:
        database = database
        table_name = 'reporte_esferas'