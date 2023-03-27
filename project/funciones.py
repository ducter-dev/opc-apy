from datetime import datetime, timedelta

def obtenerFecha05Reporte():
    now = datetime.now()
    fecha_base = datetime(now.year, now.month, now.day, 5, 0, 0)
    fecha05 = (now - timedelta(days=1)).strftime("%Y-%m-%d") if fecha_base > now else now.strftime("%Y-%m-%d")
    return fecha05


def obtenerFecha24Reporte():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")