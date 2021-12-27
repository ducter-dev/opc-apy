from fastapi import FastAPI
from .database import database as connection

app = FastAPI(
    title='SCADA-IRGE',
    description='Api para servir OPC',
    version='1.0'
)


@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
        print('connecting...')


@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('close')


@app.get('/')
async def index():
    return 'Hola mundo desde FastApi'


@app.get('/about')
async def about():
    return 'About'