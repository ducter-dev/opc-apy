from datetime import datetime
from os.path import exists
from os import getcwd

current_working_directory = getcwd()

class LogsServices():
    archivo = None


    @classmethod
    def write(self, texto):
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f = open(self.archivo, 'a')
            f.write(f"{now}: {texto}\n")
            return True
        except FileNotFoundError as e:
            print(f'Error: {e}')
            return False
        

    @classmethod
    def setNameFile(self):
        try:
            hoy = datetime.now().strftime("%Y-%m-%d")
            self.archivo = f"{current_working_directory}/logs/log_{hoy}.log"
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False
    