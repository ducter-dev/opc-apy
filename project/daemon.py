import threading
import time

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
    interval = 3

    def buscarCargasNuevas(self):
        print("Bucando cargas nuevas")