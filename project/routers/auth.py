from fastapi import HTTPException
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.params import Header
from fastapi.security import HTTPBasicCredentials
from ..schemas import UserResponseModel, UserRequestModel, UserRequestPutModel, UserChangePasswordRequestModel, BloqueadosResponseModel, BloqueadosUserRequestModel, BloqueadosRequestModel

from ..tokenServices import validate_token, write_token

from ..database import User, Caducidad, Bloqueado, Bitacora
from datetime import datetime, timedelta
from ..funciones import obtenerFecha05Reporte, obtenerFecha24Reporte
router = APIRouter(prefix='/api/v1/auth')

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
    
    user_dict = {
        "id": user.id,
        "username": user.username,
        "categoria": user.categoria,
        "departamento": user.departamento
    }

    fecha05 = obtenerFecha05Reporte()
    fecha24 = obtenerFecha24Reporte()

    Bitacora.create(
        user = user.id,
        evento = 1,
        actividad = f"El usuario {user.username} ha iniciado sesión.",
        fecha = user.created_at,
        reporte24 = fecha24,
        reporte05 = fecha05
    )
    
    data_dic = {
        "user": user_dict,
        "token": write_token(user_dict)
    }
    return data_dic

@router.post('/register', response_model=UserResponseModel)
async def create_user(user_req: UserRequestModel):

    if User.select().where(User.username == user_req.username).exists():
        raise HTTPException(409, 'El usuario ya se encuentra en uso.')

    hash_password = User.create_password(user_req.password)
    user = User.create(
        username = user_req.username,
        password = hash_password,
        categoria = user_req.categoria,
        departamento = user_req.departamento
    )
    usuarioRegistra = User.select().where(User.id == user_req.registra).first()
    Caducidad.create(
        password = user.password,
        caducidad = user.created_at,
        ultimoAcceso = user.created_at,
        estado = 1,
        user = user.id
    )
    fecha05 = obtenerFecha05Reporte()
    fecha24 = obtenerFecha24Reporte()

    Bitacora.create(
        user = usuarioRegistra.id,
        evento = 3,
        actividad = f"El usuario {usuarioRegistra.username} ha registrado a {user.username}",
        fecha = user.created_at,
        reporte24 = fecha24,
        reporte05 = fecha05
    )
    return user


@router.post('/update-password', response_model=UserResponseModel)
async def change_password(request_user: UserChangePasswordRequestModel):
    try: 
        user_id_req = request_user.user_id
        pass_req = request_user.password
        
        contrasenas = Caducidad.select().where(Caducidad.user == user_id_req)
        if len(contrasenas) > 0:
            existPassword = False
            for i in range(len(contrasenas)):
                #   Revisa que la password no exista ya
                
                user_exist = User.validate_password(pass_req, contrasenas[i].password)
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
                hash_password = User.create_password(pass_req)
                userBD = User.select().where(User.id == user_id_req).first()
                userBD.password = hash_password
                userBD.save()


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
                    user = userBD.id
                )

        return JSONResponse(
            status_code=201,
            content={"message": True}
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
    