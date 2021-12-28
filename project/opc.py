import OpenOPC
import pywintypes
import os
from os.path import join,dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

pywintypes.datetime = pywintypes.TimeType

SERVER_OPC = os.environ.get('SERVER_OPC')
HOST_OPC = os.environ.get('HOST_OPC')

#tags = sorted(opc.list('GE_ETHERNET.PLC_SCA_TULA.Asignacion.*', flat= True))

#tagsReaded = []
#for tag in tags:
#    try:
#        value = opc.read(tag)
#        tagsReaded.append(tag)
#    except OpenOPC.TimeoutError:
#        print('TimeoutError ocurred')

class OpcServices():
    server = SERVER_OPC
    host = HOST_OPC

    @classmethod
    def conectarOPC(self):
        try:
            opc = OpenOPC.client()
            opc.connect(self.server, self.host)
            return True
        except OpenOPC.TimeoutError:
            print('TimeoutError ocurred')
            return False
