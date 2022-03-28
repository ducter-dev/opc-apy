import threading
import time
from .database import TanksInService, TankInTrucks, Folio
from .opc import OpcServices

class Daemon(threading.Thread):

    def __init__(self):
        self._timer_runs = threading.Event()
        self._timer_runs.set()
        super().__init__()

    def run(self):
        while self._timer_runs.is_set():
            self.buscarCargasNuevas()
            time.sleep(self.__class__.interval)
    
    def stop(self):
        self._timer_runs.clear()


class OpcDaemon(Daemon):
    interval = 10

    def buscarCargasNuevas(self):
        folios = Folio.select().order_by('llenadera')
        for f in folios:
            print(f"Llenadera {f.llenadera.numero} - folio: {f.folio}")
            numLlen = f.llenadera.numero if f.llenadera.numero < 10 else f'0{f.llenadera.numero}'
            folioPlc = OpcServices.readDataPLC(f'GE_ETHERNET.PLC_SCA_TULA.Applications.Reportes.Llenaderas.FIN_LLEN{numLlen}')
            print(folioPlc)
            if (f.folio == folioPlc):
                print('Mismo Folio')
            else:
                print('Diferente Folio')
