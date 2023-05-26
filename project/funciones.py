from datetime import datetime, timedelta, date

def obtenerFecha05Reporte():
    now = datetime.now()
    fecha_base = datetime(now.year, now.month, now.day, 5, 0, 0)
    fecha05 = (now - timedelta(days=1)).strftime("%Y-%m-%d") if fecha_base > now else now.strftime("%Y-%m-%d")
    return fecha05


def obtenerFecha24Reporte():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

def obtenerTurno05(hora):
    turno = 0
    if hora >= 6 and hora <= 13: 
        turno = 1
    elif hora >= 14 and hora <= 21:
        turno = 2
    elif hora >= 21 and hora <= 5:
        turno = 3
    
    return turno


def obtenerTurno24(hora):
    turno = 0
    if hora >= 1 and hora <= 8: 
        turno = 1
    elif hora >= 9 and hora <= 16:
        turno = 2
    elif hora >= 17 and hora == 0:
        turno = 3
    
    return turno

def obtenerDiaAnterior(fecha):
    fechaDT = datetime.strptime(fecha, '%Y-%m-%d')
    fechaResult = (fechaDT - timedelta(days=1)).strftime('%Y-%m-%d')
    return fechaResult

def obtenerUltimoDiaMes(any_day):
    last_day = date(any_day.year, any_day.month + 1, 1) - timedelta(days=1)
    return last_day