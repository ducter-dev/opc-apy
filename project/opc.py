import OpenOPC
import pywintypes
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

pywintypes.datetime = pywintypes.TimeType

SERVER_OPC = os.environ.get('SERVER_OPC')
HOST_OPC = os.environ.get('HOST_OPC')

class OpcServices():
    server = SERVER_OPC
    host = HOST_OPC
    opc = OpenOPC.client()
    @classmethod
    def conectarOPC(self):
        try:
            self.opc.connect(self.server, self.host)
            return True
        except OpenOPC.TimeoutError:
            print('TimeoutError ocurred')
            return False

    @classmethod
    def readDataPLC(self, tag):
        value = self.opc.read(tag)
        return value[0]
    
    @classmethod
    def writeOPC(self, tag, value):
        self.opc.write((tag, value))
        return value