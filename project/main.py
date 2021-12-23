from fastapi import FastAPI

app = FastAPI(
    title='SCADA-IRGE',
    description='Api para servir OPC',
    version='1.0'
)

@app.get('/')
async def index():
    return 'Hola mundo desde FastApi'

@app.get('/about')
async def about():
    return 'About'