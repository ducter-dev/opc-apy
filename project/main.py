from fastapi import FastAPI


app = FastAPI(
    title='SCADA-IRGE',
    description='Api para servir OPC',
    version='1.0'
)


@app.on_event('startup')
def startup():
    print('El servidor va a comenzar.')


@app.on_event('shutdown')
def shutdown():
    print('El servidor se encuentra finalizado.')


@app.get('/')
async def index():
    return 'Hola mundo desde FastApi'


@app.get('/about')
async def about():
    return 'About'