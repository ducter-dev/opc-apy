from datetime import datetime, timedelta, date
import random
import string
from .logs import LogsServices
from .opc import OpcServices 

def obtenerFecha05Reporte(hora, fecha):
    """ LogsServices.write('------obtenerFecha05Reporte-------')
    LogsServices.write(f'hora: {hora}')
    LogsServices.write(f'fecha: {fecha}') """
    if hora <= 5: 
        fechaAnt = obtenerDiaAnterior(fecha)
        #LogsServices.write(f'fechaAnt: {fechaAnt}')
        #LogsServices.write('-------------')
        return fechaAnt
    else:
        #LogsServices.write(f'fecha: {fecha}')
        #LogsServices.write('-------------')
        return fecha

def obtenerFecha24Reporte(hora, fecha):
    #LogsServices.write('------obtenerFecha05Reporte-------')
    if hora == 0: 
        fechaAnt = obtenerDiaAnterior(fecha)
        #LogsServices.write(f'fechaAnt: {fechaAnt}')
        #LogsServices.write('-------------')
        return fechaAnt
    else:
        #LogsServices.write(f'fecha: {fecha}')
        #LogsServices.write('-------------')
        return fecha

def obtenerTurno05(hora):
    turno = 0
    if hora >= 6 and hora <= 13: 
        turno = 1
    elif hora >= 14 and hora <= 21:
        turno = 2
    elif hora >= 22:
        turno = 3
    elif hora <= 5:
        turno = 3
    
    return turno


def obtenerTurno24(hora):
    turno = 0
    if hora >= 1 and hora <= 8: 
        turno = 1
    elif hora >= 9 and hora <= 16:
        turno = 2
    elif hora >= 17:
        turno = 3
    elif hora == 0:
        turno = 3
    
    return turno

def obtenerDiaAnterior(fecha):
    fechaDT = datetime.strptime(fecha, '%Y-%m-%d')
    fechaResult = (fechaDT - timedelta(days=1)).strftime('%Y-%m-%d')
    return fechaResult

def obtenerDiaPosterior(fecha):
    fechaDT = datetime.strptime(fecha, '%Y-%m-%d')
    fechaResult = (fechaDT + timedelta(days=1)).strftime('%Y-%m-%d')
    return fechaResult


def obtenerUltimoDiaMes(any_day):
    last_day = date(any_day.year, any_day.month + 1, 1) - timedelta(days=1)
    last_day_dt = datetime.combine(last_day, datetime.min.time())
    return last_day_dt.strftime("%Y-%m-%d")


def obtenerUltimoDiaMesOrAhora(any_day):
    last_day = date(any_day.year, any_day.month + 1, 1) - timedelta(days=1)
    last_day_dt = datetime.combine(last_day, datetime.min.time())
    now = datetime.now()
    last_day_str = ''
    if now < last_day_dt:
        last_day_str = now.strftime("%Y-%m-%d")
    else:
        last_day_str = last_day_dt.strftime("%Y-%m-%d")

    return last_day_str

def generar_cadena_aleatoria(longitud):
    caracteres = string.ascii_letters + string.digits
    cadena_aleatoria = ''.join(random.choice(caracteres) for _ in range(longitud))
    return cadena_aleatoria


def obtenerFechaCaducidad(fecha):
    try:
        fechaDT = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        fechaResult = (fechaDT + timedelta(days=60)).strftime('%Y-%m-%d %H:%M:%S')
        return fechaResult
    except Exception as e:
        LogsServices.write(f'error: {e}')


async def get_clock():
    try:
        year = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Year')
        monthOPC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Month')
        dayOPC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Day')
        hourOPC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Hours')
        minuteOPC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Mins')
        secondOPC = OpcServices.readDataPLC('GE_ETHERNET.PLC_SCA_TULA.Applications.Radiofrecuencia.EntryExit.uDCS_Secs')

        month = convertTimeIntToString(monthOPC)
        day = convertTimeIntToString(dayOPC)
        hour = convertTimeIntToString(hourOPC)
        minute = convertTimeIntToString(minuteOPC)
        second = convertTimeIntToString(secondOPC)


        fecha_hora = f'{year}-{month}-{day} {hour}:{minute}:{second}'
        return {
            'fechaHora': fecha_hora
        }
    except Exception as e:
        LogsServices.write(f'error: {e}')

def convertTimeIntToString(number):
    numbersStr = ''
    if number < 10:
        numbersStr = f'0{number}'
    else:
        numbersStr = f'{number}'
    
    return numbersStr