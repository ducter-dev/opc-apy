from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.params import Header
from fastapi.security import HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from ..schemas import UserResponseModel, UserRequestModel, UserRequestPutModel, UserChangePasswordRequestModel, BloqueadosResponseModel, BloqueadosUserRequestModel, BloqueadosRequestModel

from ..tokenServices import validate_token, write_token

from ..database import User, Caducidad, Bloqueado, Bitacora
from datetime import datetime, timedelta
from ..funciones import obtenerFecha05Reporte, obtenerFecha24Reporte, generar_cadena_aleatoria
from ..emails import EmailServices
from ..logs import LogsServices
router = APIRouter(prefix='/api/v1/auth')

templates = Jinja2Templates(directory="templates")

@router.post('/login')
async def login(credentials: HTTPBasicCredentials):

    user = User.select().where(User.username == credentials.username).first()
    if user is None:
        return JSONResponse(
            status_code=419,
            content={"message": "Las credenciales no coinciden con nuestros registros."}
        )
    
    user_valid = User.validate_password(credentials.password, user.password)
    if user_valid is False:
        return JSONResponse(
            status_code=419,
            content={"message": "Las credenciales no coinciden con nuestros registros."}
        )
    
    if user.verificado is None:
        return JSONResponse(
            status_code=419,
            content={"message": "El usuario no se ha verificado, debe verificar su cuenta primero."}
        )
    
    user_dict = {
        "id": user.id,
        "username": user.username,
        "categoria": user.categoria,
        "departamento": user.departamento,
        "verificado": user.verificado.strftime("%Y-%m-%d %H:%M:%S")
    }

    fecha05 = obtenerFecha05Reporte()
    fecha24 = obtenerFecha24Reporte()
    now = datetime.now()
    ahora = now.strftime("%Y-%m-%d %H:%M:%S")

    Bitacora.create(
        user = user.id,
        evento = 1,
        actividad = f"El usuario {user.username} ha iniciado sesión.",
        fecha = ahora,
        reporte24 = fecha24,
        reporte05 = fecha05
    )
    
    data_dic = {
        "user": user_dict,
        "token": write_token(user_dict)
    }
    return data_dic

#@router.post('/register', response_model=UserResponseModel)
@router.post('/register', response_model=UserResponseModel)
async def create_user(user_req: UserRequestModel):
    try:
        LogsServices.setNameFile()
        if User.select().where(User.username == user_req.username).exists():
            return JSONResponse(
                status_code=501,
                content={"message": 'El usuario ya se encuentra en uso.'}
            )
        
        password_random = generar_cadena_aleatoria(10)

        hash_password = User.create_password(password_random)

        user = User.create(
            username = user_req.username,
            password = hash_password,
            email = user_req.email,
            categoria = user_req.categoria,
            departamento = user_req.departamento
        )

        Caducidad.create(
            password = user.password,
            caducidad = user.created_at,
            ultimoAcceso = user.created_at,
            estado = 1,
            user = user.id
        )
        
        
        enviar_email = EmailServices.enviar_correo_activacion(user, password_random)
        LogsServices.write(f'enviar_email: {enviar_email}')

        fecha05 = obtenerFecha05Reporte()
        fecha24 = obtenerFecha24Reporte()

        Bitacora.create(
            user = 1,
            evento = 3,
            actividad = f"El usuario {user.username} ha sido registrado.",
            fecha = user.created_at,
            reporte24 = fecha24,
            reporte05 = fecha05
        )
        return user
    
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )

@router.get('/activar-cuenta/{token}', response_class=HTMLResponse)
async def activar_cuenta(token: str, request: Request):
    try:
        LogsServices.setNameFile()
        id_cuenta_desencriptado, token_desencriptado, success = EmailServices.desencriptar_enlace(token)
        LogsServices.write(f'success: {success}')
        LogsServices.write(f'id_cuenta_desencriptado: {id_cuenta_desencriptado}')
        LogsServices.write(f'token_desencriptado: {token_desencriptado}')

        user = User.select().where(User.id == id_cuenta_desencriptado).first()
        now = datetime.now()
        ahora = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        user.verificado = ahora
        user.save()
        
        return templates.TemplateResponse('count_activated.html', {"request": request})
    except Exception as e:
        print(e)
        return False


@router.post('/update-password', response_model=UserResponseModel)
async def change_password(request_user: UserChangePasswordRequestModel):
    try: 
        req_email = request_user.email
        req_pass = request_user.password
        user = User.select().where(User.email == req_email).first()

        if user is None:
            return JSONResponse(
                status_code=422,
                content={"message": "El correo no se encuentra registrado, verifique su información."}
            )
        contrasenas = Caducidad.select().where(Caducidad.user == user.id)
        if len(contrasenas) > 0:
            existPassword = False
            for i in range(len(contrasenas)):
                #   Revisa que la password no exista ya
                user_exist = User.validate_password(req_pass, contrasenas[i].password)
                #   Si existe retornamos error y mensaje ·
                
                if user_exist:
                    existPassword = True
            
            if existPassword:
                return JSONResponse(
                    status_code=422,
                    content={"message": "La contraseña ya fue registrada antes, intente con otra."}
                )
            else:
                #   Actualizar password de usuario
                hash_password = User.create_password(req_pass)
                user.password = hash_password
                user.save()


                for i in range(len(contrasenas)):
                    contrasenas[i].estado = 2
                    contrasenas[i].save()

                #   Actualizar estados de password en caducidad
                now = datetime.now()
                ahora = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
                fechaCaducidad = now + timedelta(days=60)
                fechaCaducidadStr = fechaCaducidad.strftime('%Y-%m-%d %H:%M:%S')
                
                #   Insertar registro en caducidad
                Caducidad.create(
                    password = hash_password,
                    caducidad = fechaCaducidadStr,
                    ultimoAcceso = ahora,
                    estado = 1,
                    user = user.id
                )

                #   Enviar correo con las nuevas credenciales

        enviar_email = EmailServices.enviar_correo_nueva_password(user, req_pass)
        return JSONResponse(
            status_code=200,
            content={"message": 'Credenciales actualizadas'}
        )
    except Exception as e:
        return JSONResponse(
            status_code=501,
            content={"message": e}
        )


@router.post('/verify/token')
async def verify_token(Authorization: str = Header(None)):
    token = Authorization.split(' ')[1]
    return validate_token(token, output=True)


@router.post('/bloqueados', response_model=BloqueadosResponseModel)
async def insert_bloqueados(request: BloqueadosRequestModel):
    userBlock = User.select().where(User.username == request.user).first()
    if userBlock is None:
        return JSONResponse(
            status_code=200,
            content={"message": 'Usuario no encontrado.'}
        )

    fechaDesbloqueo = datetime.strptime(request.fechaBloqueo, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=15)
    bloqueado = Bloqueado.create(
        user = userBlock.id,
        fechaBloqueo = request.fechaBloqueo,
        fechaDesbloqueo = fechaDesbloqueo,
    )
    return bloqueado


@router.post('/bloqueados/user')
async def status_bloqueados(request: BloqueadosUserRequestModel):
    try:
        """ Se recibe el usuario en el request, primero se revisa si existe en la BD, si existe continuamos, 
        si no retornamos que no existe con un status code 400.
        """

        now = datetime.now()
        user_bd = User.select().where(User.username == request.usuario).first()

        if user_bd is None:
            return JSONResponse(
                status_code=400,
                content={"message": "Error revise sus credenciales ó contacte al administrador del sistema."}
            )
        """ Revisamos que el usuario se encuentre en la tabla de bloqueos, si no existe retornamos bloqueado false, 
            y si existe comprobamos que la fecha de desbloqueo ya haya pasado.
        """
        bloqueado = Bloqueado.select().where(Bloqueado.user == user_bd.id).order_by(Bloqueado.id.desc()).first()

        if bloqueado is None:
            return JSONResponse(
                    status_code=200,
                    content={"bloqueado": False}
                )
        else:
            # ahora > fecha de desbloqueo
            if now > bloqueado.fechaDesbloqueo:
                return JSONResponse(
                    status_code=200,
                    content={"bloqueado": False}
                )
            else:
                return JSONResponse(
                    status_code=200,
                    content={"bloqueado": True}
                )
    except Exception as e:
        return JSONResponse(
        status_code=501,
        content={"message": e}
    )