import smtplib
import os
import secrets
import hashlib
import base64
from os.path import join, dirname
from dotenv import load_dotenv
from .database import User
from .logs import LogsServices
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MAIL_HOST = os.environ.get('MAIL_HOST')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_ENCRYPTION = os.environ.get('MAIL_ENCRYPTION')
MAIL_FROM_ADDRESS = os.environ.get('MAIL_FROM_ADDRESS')
MAIL_FROM_NAME = os.environ.get('MAIL_FROM_NAME')
KEY_APP = os.environ.get('KEY_APP')

class EmailServices():
    servidor = MAIL_HOST
    puerto_smtp = MAIL_PORT
    usuario = MAIL_USERNAME
    clave = MAIL_PASSWORD
    key = KEY_APP


    @classmethod
    def enviar_correo_activacion(self, user: User, password_plain: str):
        try:
            # Crear el objeto SMTP
            conexion_smtp = smtplib.SMTP_SSL(self.servidor, self.puerto_smtp)
            #conexion_smtp.starttls()

            # Autenticarse en el servidor de correo
            conexion_smtp.login(self.usuario, self.clave)

            asunto = 'Registro a SCA v2'
            enlace_activacion = self.generar_enlace_activacion(user.id)

            sender = 'soporte.sistemas@ducter.con.mx'
            ccp = 'michel.morales@ducter.com.mx'

            # Crear el objeto MIMEMultipart
            mensaje = MIMEMultipart("alternative")
            mensaje["Subject"] = asunto
            mensaje["From"] = sender
            mensaje["To"] = user.email

            contenido_html = self.contenido_email_registed(enlace_activacion, user, password_plain)
            
            # Crear un objeto MIMEText para el contenido HTML
            parte_html = MIMEText(contenido_html, 'html')

            # Adjuntar la parte HTML al mensaje
            mensaje.attach(parte_html)


            # Enviar el correo
            conexion_smtp.sendmail(sender, [user.email, ccp], mensaje.as_string())

            # Cerrar la conexión con el servidor
            conexion_smtp.quit()

            return {
                "send" : True,
                "mensaje": "Correo enviado"
            }
        except Exception as e:
            return {
                "send": False,
                "mensaje": f'Error: {e}'
            }

    @classmethod
    def enviar_correo_nueva_password(self, user: User, password_plain: str):
        try:
            # Crear el objeto SMTP
            conexion_smtp = smtplib.SMTP(self.servidor, self.puerto_smtp)
            conexion_smtp.starttls()

            # Autenticarse en el servidor de correo
            conexion_smtp.login(self.usuario, self.clave)

            asunto = 'Contraseña actualizada'
            
            sender = 'info@scav2.com'
            # Crear el objeto MIMEMultipart
            mensaje = MIMEMultipart("alternative")
            mensaje["Subject"] = asunto
            mensaje["From"] = sender
            mensaje["To"] = user.email

            contenido_html = self.contenido_email_actualizado(user, password_plain)
            
            # Crear un objeto MIMEText para el contenido HTML
            parte_html = MIMEText(contenido_html, 'html')

            # Adjuntar la parte HTML al mensaje
            mensaje.attach(parte_html)


            # Enviar el correo
            conexion_smtp.sendmail(sender, user.email, mensaje.as_string())

            # Cerrar la conexión con el servidor
            conexion_smtp.quit()
            return {
                "send" : True,
                "mensaje": "Correo enviado"
            }
        except Exception as e:
            return {
                "send": False,
                "mensaje": f'Error: {e}'
            }
        
    @classmethod
    def enviar_correo_recovery_password(self, user: User, password_plain: str):
        try:
            # Crear el objeto SMTP
            conexion_smtp = smtplib.SMTP(self.servidor, self.puerto_smtp)
            conexion_smtp.starttls()

            # Autenticarse en el servidor de correo
            conexion_smtp.login(self.usuario, self.clave)

            asunto = 'Recuperar password'
            
            sender = 'info@scav2.com'
            # Crear el objeto MIMEMultipart
            mensaje = MIMEMultipart("alternative")
            mensaje["Subject"] = asunto
            mensaje["From"] = sender
            mensaje["To"] = user.email

            contenido_html = self.contenido_email_recovery_password(user, password_plain)
            
            # Crear un objeto MIMEText para el contenido HTML
            parte_html = MIMEText(contenido_html, 'html')

            # Adjuntar la parte HTML al mensaje
            mensaje.attach(parte_html)

            # Enviar el correo
            conexion_smtp.sendmail(sender, user.email, mensaje.as_string())

            # Cerrar la conexión con el servidor
            conexion_smtp.quit()
            return {
                "send" : True,
                "mensaje": "Correo enviado"
            }
        except Exception as e:
            return {
                "send": False,
                "mensaje": f'Error: {e}'
            }

    @classmethod
    def generarClaveCifrado(self):
        key = Fernet.generate_key()
        LogsServices.write(f'key: {key}')


    @classmethod
    def generar_enlace_activacion(self, usuario_id: int):

        # Generar un token aleatorio para el enlace
        token = secrets.token_urlsafe(32)

        # Concatenar el identificador y el token
        mensaje = f'{token}:{usuario_id}'
        LogsServices.write(f'mensaje: {mensaje}')
        LogsServices.write(f'key: {self.key}')
        mensaje_encriptado = self.encrypt(mensaje.encode(), self.key)
        LogsServices.write(f'mensaje_encriptado: {mensaje_encriptado}')
        cadena_encriptada = base64.urlsafe_b64encode(mensaje_encriptado).decode()
        LogsServices.write(f'cadena_encriptada: {cadena_encriptada}')

        # Link original
        enlace_activacion = f"http://10.122.50.90/sca/api/v1/auth/activar-cuenta/{cadena_encriptada}"
        LogsServices.write(f'enlace_activacion: {enlace_activacion}')
        
        return enlace_activacion


    @classmethod
    def contenido_email_registed(self, link_verification: str, user: User, password_plain: str):
        html1 = """
            <!doctype html>
            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

            <head>
            <title>
            </title>
            <!--[if !mso]><!-- -->
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <!--<![endif]-->
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style type="text/css">
                #outlook a {
                padding: 0;
                }

                .ReadMsgBody {
                width: 100%;
                }

                .ExternalClass {
                width: 100%;
                }

                .ExternalClass * {
                line-height: 100%;
                }

                body {
                margin: 0;
                padding: 0;
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
                }

                table,
                td {
                border-collapse: collapse;
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                }

                img {
                border: 0;
                height: auto;
                line-height: 100%;
                outline: none;
                text-decoration: none;
                -ms-interpolation-mode: bicubic;
                }

                p {
                display: block;
                margin: 13px 0;
                }
            </style>
            <!--[if !mso]><!-->
            <style type="text/css">
                @media only screen and (max-width:480px) {
                @-ms-viewport {
                    width: 320px;
                }

                @viewport {
                    width: 320px;
                }
                }
            </style>
            <!--<![endif]-->
            <!--[if mso]>
                    <xml>
                    <o:OfficeDocumentSettings>
                    <o:AllowPNG/>
                    <o:PixelsPerInch>96</o:PixelsPerInch>
                    </o:OfficeDocumentSettings>
                    </xml>
                    <![endif]-->
            <!--[if lte mso 11]>
                    <style type="text/css">
                    .outlook-group-fix { width:100% !important; }
                    </style>
                    <![endif]-->
            <!--[if !mso]><!-->
            <link href="https://fonts.googleapis.com/css?family=Open Sans" rel="stylesheet" type="text/css">
            <style type="text/css">
                @import url(https://fonts.googleapis.com/css?family=Open Sans);
            </style>
            <!--<![endif]-->
            <style type="text/css">
                @media only screen and (min-width:480px) {
                .mj-column-per-100 {
                    width: 100% !important;
                    max-width: 100%;
                }
                }
            </style>
            <style type="text/css">
                [owa] .mj-column-per-100 {
                width: 100% !important;
                max-width: 100%;
                }
            </style>
            <style type="text/css">
                @media only screen and (max-width:480px) {
                table.full-width-mobile {
                    width: 100% !important;
                }

                td.full-width-mobile {
                    width: auto !important;
                }
                }
            </style>
            </head>

            <body style="background-color:#f8f8f8;">
            <div style="background-color:#f8f8f8;">
                <!--[if mso | IE]>
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0px 20px 0px;padding-bottom:0px;padding-top:0px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="background:#ffffff;background-color:#ffffff;Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-left:0px;padding-right:0px;padding-top:0px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td style="font-size:0px;padding:10px 25px;padding-top:0px;padding-right:0px;padding-bottom:40px;padding-left:0px;word-break:break-word;">
                                <p style="border-top:solid 7px #DEDEDE;font-size:1;margin:0px auto;width:100%;">
                                </p>
                                <!--[if mso | IE]>
                    <table
                    align="center" border="0" cellpadding="0" cellspacing="0" style="border-top:solid 7px #DEDEDE;font-size:1;margin:0px auto;width:600px;" role="presentation" width="600px"
                    >
                    <tr>
                        <td style="height:0;line-height:0;">
                        &nbsp;
                        </td>
                    </tr>
                    </table>
                <![endif]-->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="font-size:0px;padding:10px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word;">
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                    <tbody>
                                    <tr>
                                        <td style="width:110px;">
                                        <img alt="" height="auto" src="/saas-templates-creator/static/img/mjml.png" style="border:none;display:block;outline:none;text-decoration:none;height:auto;width:100%;" title="" width="110" />
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="background:#ffffff;background-color:#ffffff;Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-top:0px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td align="center" style="font-size:0px;padding:10px 25px;padding-top:40px;padding-right:50px;padding-bottom:0px;padding-left:50px;word-break:break-word;">
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                    <tbody>
                                    <tr>
                                        <td style="width:300px;">
                                        <img alt="" height="auto" src="https://www.mailjet.com/wp-content/uploads/2019/07/Welcome-02.png" style="border:none;display:block;outline:none;text-decoration:none;height:auto;width:100%;" title="" width="300" />
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="background:#ffffff;background-color:#ffffff;Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0px 20px 0px;padding-bottom:70px;padding-top:30px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td align="left" style="font-size:0px;padding:0px 25px 0px 25px;padding-top:0px;padding-right:50px;padding-bottom:0px;padding-left:50px;word-break:break-word;">
                                <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:13px;line-height:22px;text-align:left;color:#797e82;">
                                    <h1 style="text-align:center; color: #000000; line-height:32px">Ya casi estás aquí!</h1>
                                </div>
                                </td>
                            </tr>
                            <tr>
                                <td align="left" style="font-size:0px;padding:0px 25px 0px 25px;padding-top:0px;padding-right:50px;padding-bottom:0px;padding-left:50px;word-break:break-word;">
                                <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:13px;line-height:22px;text-align:left;color:#797e82;">
        """
        html2 = f'<p style="margin: 10px 0; text-align: center;">Hola {user.username}, Gracias por registrarte a SCA v2.&nbsp;</p>'
        html3 = '<p style="margin: 10px 0; text-align: center;">Sus credenciales son las siguientes, pero deberá confirmar su cuenta primero.&nbsp;</p>'
        html4 = f'<p style="margin: 10px 0; text-align: center;">Usuario: {user.username}&nbsp;</p>'
        html5 = f'<p style="margin: 10px 0; text-align: center;">Password: { password_plain }&nbsp;</p>'
        html6 = """
                <p style="margin: 10px 0; text-align: center;">Para confirmar tu cuenta, simplemente da clic en el botón de abajo:</p>
                    </div>
                    </td>
                </tr>
                <tr>
                    <td align="center" vertical-align="middle" style="font-size:0px;padding:10px 25px;padding-top:20px;padding-bottom:20px;word-break:break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
                            <tr>
                            <td align="center" bgcolor="#DEDEDE" role="presentation" style="border:none;border-radius:100px;cursor:auto;padding:15px 25px 15px 25px;background:#DEDEDE;" valign="middle">
            """
        html7 = f'<a href="{link_verification}" style="background:#DEDEDE;color:#222222;font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:13px;font-weight:normal;line-height:120%;Margin:0;text-decoration:none;text-transform:none;" target="_blank">'
        html8 = """
            <b style="font-weight:700"><b style="font-weight:700">Activar My Cuenta</b></b>
                                        </a>
                                    </td>
                                    </tr>
                                </table>
                                </td>
                            </tr>
                            <tr>
                                <td align="left" style="font-size:0px;padding:0px 25px 0px 25px;padding-top:0px;padding-right:50px;padding-bottom:0px;padding-left:50px;word-break:break-word;">
                                <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:13px;line-height:22px;text-align:left;color:#797e82;">
        """
        html9 = f'<p style="margin: 10px 0; text-align: center;">Si éste link no funciona, cópialo en el navegador: <a target="_blank" rel="noopener noreferrer" href="{link_verification}" style="color:#DEDEDE">{link_verification}</a></p>'
        html10 = """

                                    <p style="margin: 10px 0; text-align: center;"><i style="font-style:normal"><b style="font-weight:700">Bienvenido!</b></i></p>
                                </div>
                                </td>
                            </tr>
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0px 20px 0px;padding-bottom:0px;padding-top:20px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td align="center" style="font-size:0px;padding:10px 25px;padding-bottom:0px;word-break:break-word;">
                                <!--[if mso | IE]>
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                >
                    <tr>
                
                        <td>
                        <![endif]-->
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                    <tr>
                                    <td style="padding:4px;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#DEDEDE;border-radius:6px;width:30;">
                                        <tr>
                                            <td style="font-size:0;height:30;vertical-align:middle;width:30;">
                                            <a href="[[SHORT_PERMALINK]]" target="_blank">
                                                <img height="30" src="http://saas-templates-creator.mailjet.com/saas-templates-creator/static/img/facebook_black.png" style="border-radius:6px;" width="30" />
                                            </a>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </table>
                                <!--[if mso | IE]>
                        </td>
                        
                        <td>
                        <![endif]-->
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                    <tr>
                                    <td style="padding:4px;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#DEDEDE;border-radius:6px;width:30;">
                                        <tr>
                                            <td style="font-size:0;height:30;vertical-align:middle;width:30;">
                                            <a href="[[SHORT_PERMALINK]]" target="_blank">
                                                <img height="30" src="http://saas-templates-creator.mailjet.com/saas-templates-creator/static/img/twitter_black.png" style="border-radius:6px;" width="30" />
                                            </a>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </table>
                                <!--[if mso | IE]>
                        </td>
                        
                        <td>
                        <![endif]-->
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                    <tr>
                                    <td style="padding:4px;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#DEDEDE;border-radius:6px;width:30;">
                                        <tr>
                                            <td style="font-size:0;height:30;vertical-align:middle;width:30;">
                                            <a href="[[SHORT_PERMALINK]]" target="_blank">
                                                <img height="30" src="http://saas-templates-creator.mailjet.com/saas-templates-creator/static/img/linkedin_black.png" style="border-radius:6px;" width="30" />
                                            </a>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </table>
                                <!--[if mso | IE]>
                        </td>
                        
                    </tr>
                    </table>
                <![endif]-->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="font-size:0px;padding:0px 20px 0px 20px;padding-top:0px;padding-bottom:0px;word-break:break-word;">
                                <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:11px;line-height:22px;text-align:center;color:#797e82;">
                                    <p style="margin: 10px 0;">C<a target="_blank" rel="noopener noreferrer" style="color:inherit; text-decoration:none" href="[[UNSUB_LINK_EN]]">lick <span style="color:#DEDEDE"><u>here</u></span> to unsubscribe</a>.<br /><span style="font-size:10px">Created by&nbsp;</span><a target="_blank" rel="noopener noreferrer" style="font-size:10px; color:inherit; text-decoration: none" href="https://www.mailjet.com/?utm_source=saas_email_templates&amp;utm_medium=logo_footer_email&amp;utm_campaign=account_activation"><span style="color:#DEDEDE"><u>Mailjet</u></span></a></p>
                                </div>
                                </td>
                            </tr>
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                <![endif]-->
            </div>
            </body>

            </html>
            """
        mensaje = "" + html1 + html2 + html3 + html4 + html5 + html6 + html7 + html8  + html9 + html10
        return mensaje
        

    @classmethod
    def contenido_email_actualizado(self, user: User, password_plain: str):
        html1 = """
            <!doctype html>
            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

            <head>
            <title>
            </title>
            <!--[if !mso]><!-- -->
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <!--<![endif]-->
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style type="text/css">
                #outlook a {
                padding: 0;
                }

                .ReadMsgBody {
                width: 100%;
                }

                .ExternalClass {
                width: 100%;
                }

                .ExternalClass * {
                line-height: 100%;
                }

                body {
                margin: 0;
                padding: 0;
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
                }

                table,
                td {
                border-collapse: collapse;
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                }

                img {
                border: 0;
                height: auto;
                line-height: 100%;
                outline: none;
                text-decoration: none;
                -ms-interpolation-mode: bicubic;
                }

                p {
                display: block;
                margin: 13px 0;
                }
            </style>
            <!--[if !mso]><!-->
            <style type="text/css">
                @media only screen and (max-width:480px) {
                @-ms-viewport {
                    width: 320px;
                }

                @viewport {
                    width: 320px;
                }
                }
            </style>
            <!--<![endif]-->
            <!--[if mso]>
                    <xml>
                    <o:OfficeDocumentSettings>
                    <o:AllowPNG/>
                    <o:PixelsPerInch>96</o:PixelsPerInch>
                    </o:OfficeDocumentSettings>
                    </xml>
                    <![endif]-->
            <!--[if lte mso 11]>
                    <style type="text/css">
                    .outlook-group-fix { width:100% !important; }
                    </style>
                    <![endif]-->
            <!--[if !mso]><!-->
            <link href="https://fonts.googleapis.com/css?family=Open Sans" rel="stylesheet" type="text/css">
            <style type="text/css">
                @import url(https://fonts.googleapis.com/css?family=Open Sans);
            </style>
            <!--<![endif]-->
            <style type="text/css">
                @media only screen and (min-width:480px) {
                .mj-column-per-100 {
                    width: 100% !important;
                    max-width: 100%;
                }
                }
            </style>
            <style type="text/css">
                [owa] .mj-column-per-100 {
                width: 100% !important;
                max-width: 100%;
                }
            </style>
            <style type="text/css">
                @media only screen and (max-width:480px) {
                table.full-width-mobile {
                    width: 100% !important;
                }

                td.full-width-mobile {
                    width: auto !important;
                }
                }
            </style>
            </head>

            <body style="background-color:#f8f8f8;">
            <div style="background-color:#f8f8f8;">
                <!--[if mso | IE]>
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0px 20px 0px;padding-bottom:0px;padding-top:0px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="background:#ffffff;background-color:#ffffff;Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-left:0px;padding-right:0px;padding-top:0px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td style="font-size:0px;padding:10px 25px;padding-top:0px;padding-right:0px;padding-bottom:40px;padding-left:0px;word-break:break-word;">
                                <p style="border-top:solid 7px #DEDEDE;font-size:1;margin:0px auto;width:100%;">
                                </p>
                                <!--[if mso | IE]>
                    <table
                    align="center" border="0" cellpadding="0" cellspacing="0" style="border-top:solid 7px #DEDEDE;font-size:1;margin:0px auto;width:600px;" role="presentation" width="600px"
                    >
                    <tr>
                        <td style="height:0;line-height:0;">
                        &nbsp;
                        </td>
                    </tr>
                    </table>
                <![endif]-->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="font-size:0px;padding:10px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word;">
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                    <tbody>
                                    <tr>
                                        <td style="width:110px;">
                                        <img alt="" height="auto" src="/saas-templates-creator/static/img/mjml.png" style="border:none;display:block;outline:none;text-decoration:none;height:auto;width:100%;" title="" width="110" />
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="background:#ffffff;background-color:#ffffff;Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-top:0px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td align="center" style="font-size:0px;padding:10px 25px;padding-top:40px;padding-right:50px;padding-bottom:0px;padding-left:50px;word-break:break-word;">
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                    <tbody>
                                    <tr>
                                        <td style="width:300px;">
                                        <img alt="" height="auto" src="https://www.mailjet.com/wp-content/uploads/2019/07/Welcome-02.png" style="border:none;display:block;outline:none;text-decoration:none;height:auto;width:100%;" title="" width="300" />
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="background:#ffffff;background-color:#ffffff;Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0px 20px 0px;padding-bottom:70px;padding-top:30px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td align="left" style="font-size:0px;padding:0px 25px 0px 25px;padding-top:0px;padding-right:50px;padding-bottom:0px;padding-left:50px;word-break:break-word;">
                                <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:13px;line-height:22px;text-align:left;color:#797e82;">
        """
        html2 = f'<p style="margin: 10px 0; text-align: center;">Hola {user.username}, tus credenciales se han actualizado.&nbsp;</p>'
        html3 = '<p style="margin: 10px 0; text-align: center;">Sus credenciales son las siguientes:&nbsp;</p>'
        html4 = f'<p style="margin: 10px 0; text-align: center;">Usuario: {user.username}&nbsp;</p>'
        html5 = f'<p style="margin: 10px 0; text-align: center;">Password: { password_plain }&nbsp;</p>'
        html6 = """
                    </div>
                    </td>
                </tr>
            """
        html8 = """
                            </tr>
        """
        html10 = """
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0px 20px 0px;padding-bottom:0px;padding-top:20px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td align="center" style="font-size:0px;padding:10px 25px;padding-bottom:0px;word-break:break-word;">
                                <!--[if mso | IE]>
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                >
                    <tr>
                
                        <td>
                        <![endif]-->
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                    <tr>
                                    <td style="padding:4px;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#DEDEDE;border-radius:6px;width:30;">
                                        <tr>
                                            <td style="font-size:0;height:30;vertical-align:middle;width:30;">
                                            <a href="[[SHORT_PERMALINK]]" target="_blank">
                                                <img height="30" src="http://saas-templates-creator.mailjet.com/saas-templates-creator/static/img/facebook_black.png" style="border-radius:6px;" width="30" />
                                            </a>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </table>
                                <!--[if mso | IE]>
                        </td>
                        
                        <td>
                        <![endif]-->
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                    <tr>
                                    <td style="padding:4px;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#DEDEDE;border-radius:6px;width:30;">
                                        <tr>
                                            <td style="font-size:0;height:30;vertical-align:middle;width:30;">
                                            <a href="[[SHORT_PERMALINK]]" target="_blank">
                                                <img height="30" src="http://saas-templates-creator.mailjet.com/saas-templates-creator/static/img/twitter_black.png" style="border-radius:6px;" width="30" />
                                            </a>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </table>
                                <!--[if mso | IE]>
                        </td>
                        
                        <td>
                        <![endif]-->
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                    <tr>
                                    <td style="padding:4px;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#DEDEDE;border-radius:6px;width:30;">
                                        <tr>
                                            <td style="font-size:0;height:30;vertical-align:middle;width:30;">
                                            <a href="[[SHORT_PERMALINK]]" target="_blank">
                                                <img height="30" src="http://saas-templates-creator.mailjet.com/saas-templates-creator/static/img/linkedin_black.png" style="border-radius:6px;" width="30" />
                                            </a>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </table>
                                <!--[if mso | IE]>
                        </td>
                        
                    </tr>
                    </table>
                <![endif]-->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="font-size:0px;padding:0px 20px 0px 20px;padding-top:0px;padding-bottom:0px;word-break:break-word;">
                                <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:11px;line-height:22px;text-align:center;color:#797e82;">
                                    <p style="margin: 10px 0;">C<a target="_blank" rel="noopener noreferrer" style="color:inherit; text-decoration:none" href="[[UNSUB_LINK_EN]]">lick <span style="color:#DEDEDE"><u>here</u></span> to unsubscribe</a>.<br /><span style="font-size:10px">Created by&nbsp;</span><a target="_blank" rel="noopener noreferrer" style="font-size:10px; color:inherit; text-decoration: none" href="https://www.mailjet.com/?utm_source=saas_email_templates&amp;utm_medium=logo_footer_email&amp;utm_campaign=account_activation"><span style="color:#DEDEDE"><u>Mailjet</u></span></a></p>
                                </div>
                                </td>
                            </tr>
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                <![endif]-->
            </div>
            </body>

            </html>
            """
        mensaje = "" + html1 + html2 + html3 + html4 + html5 + html6 +  html8  +  html10
        return mensaje

    @classmethod
    def contenido_email_recovery_password(self, user: User, password_plain: str):
        html1 = """
            <!doctype html>
            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

            <head>
            <title>
            </title>
            <!--[if !mso]><!-- -->
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <!--<![endif]-->
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style type="text/css">
                #outlook a {
                padding: 0;
                }

                .ReadMsgBody {
                width: 100%;
                }

                .ExternalClass {
                width: 100%;
                }

                .ExternalClass * {
                line-height: 100%;
                }

                body {
                margin: 0;
                padding: 0;
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
                }

                table,
                td {
                border-collapse: collapse;
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                }

                img {
                border: 0;
                height: auto;
                line-height: 100%;
                outline: none;
                text-decoration: none;
                -ms-interpolation-mode: bicubic;
                }

                p {
                display: block;
                margin: 13px 0;
                }
            </style>
            <!--[if !mso]><!-->
            <style type="text/css">
                @media only screen and (max-width:480px) {
                @-ms-viewport {
                    width: 320px;
                }

                @viewport {
                    width: 320px;
                }
                }
            </style>
            <!--<![endif]-->
            <!--[if mso]>
                    <xml>
                    <o:OfficeDocumentSettings>
                    <o:AllowPNG/>
                    <o:PixelsPerInch>96</o:PixelsPerInch>
                    </o:OfficeDocumentSettings>
                    </xml>
                    <![endif]-->
            <!--[if lte mso 11]>
                    <style type="text/css">
                    .outlook-group-fix { width:100% !important; }
                    </style>
                    <![endif]-->
            <!--[if !mso]><!-->
            <link href="https://fonts.googleapis.com/css?family=Open Sans" rel="stylesheet" type="text/css">
            <style type="text/css">
                @import url(https://fonts.googleapis.com/css?family=Open Sans);
            </style>
            <!--<![endif]-->
            <style type="text/css">
                @media only screen and (min-width:480px) {
                .mj-column-per-100 {
                    width: 100% !important;
                    max-width: 100%;
                }
                }
            </style>
            <style type="text/css">
                [owa] .mj-column-per-100 {
                width: 100% !important;
                max-width: 100%;
                }
            </style>
            <style type="text/css">
                @media only screen and (max-width:480px) {
                table.full-width-mobile {
                    width: 100% !important;
                }

                td.full-width-mobile {
                    width: auto !important;
                }
                }
            </style>
            </head>

            <body style="background-color:#f8f8f8;">
            <div style="background-color:#f8f8f8;">
                <!--[if mso | IE]>
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0px 20px 0px;padding-bottom:0px;padding-top:0px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="background:#ffffff;background-color:#ffffff;Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-left:0px;padding-right:0px;padding-top:0px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td style="font-size:0px;padding:10px 25px;padding-top:0px;padding-right:0px;padding-bottom:40px;padding-left:0px;word-break:break-word;">
                                <p style="border-top:solid 7px #DEDEDE;font-size:1;margin:0px auto;width:100%;">
                                </p>
                                <!--[if mso | IE]>
                    <table
                    align="center" border="0" cellpadding="0" cellspacing="0" style="border-top:solid 7px #DEDEDE;font-size:1;margin:0px auto;width:600px;" role="presentation" width="600px"
                    >
                    <tr>
                        <td style="height:0;line-height:0;">
                        &nbsp;
                        </td>
                    </tr>
                    </table>
                <![endif]-->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="font-size:0px;padding:10px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word;">
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                    <tbody>
                                    <tr>
                                        <td style="width:110px;">
                                        <img alt="" height="auto" src="/saas-templates-creator/static/img/mjml.png" style="border:none;display:block;outline:none;text-decoration:none;height:auto;width:100%;" title="" width="110" />
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="background:#ffffff;background-color:#ffffff;Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-top:0px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td align="center" style="font-size:0px;padding:10px 25px;padding-top:40px;padding-right:50px;padding-bottom:0px;padding-left:50px;word-break:break-word;">
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                    <tbody>
                                    <tr>
                                        <td style="width:300px;">
                                        <img alt="" height="auto" src="https://www.mailjet.com/wp-content/uploads/2019/07/Welcome-02.png" style="border:none;display:block;outline:none;text-decoration:none;height:auto;width:100%;" title="" width="300" />
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="background:#ffffff;background-color:#ffffff;Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0px 20px 0px;padding-bottom:70px;padding-top:30px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td align="left" style="font-size:0px;padding:0px 25px 0px 25px;padding-top:0px;padding-right:50px;padding-bottom:0px;padding-left:50px;word-break:break-word;">
                                <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:13px;line-height:22px;text-align:left;color:#797e82;">
        """
        html2 = f'<p style="margin: 10px 0; text-align: center;">Hola {user.username}, tus credenciales son las siguientes:.&nbsp;</p>'
        html4 = f'<p style="margin: 10px 0; text-align: center;">Usuario: {user.username}&nbsp;</p>'
        html5 = f'<p style="margin: 10px 0; text-align: center;">Password: { password_plain }&nbsp;</p>'
        html6 = """
                    </div>
                    </td>
                </tr>
            """
        html8 = """
                            </tr>
        """
        html10 = """
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
                >
                    <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                <![endif]-->
                <div style="Margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0px 20px 0px;padding-bottom:0px;padding-top:20px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            
                    <tr>
                
                        <td
                        class="" style="vertical-align:top;width:600px;"
                        >
                    <![endif]-->
                        <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                                <td align="center" style="font-size:0px;padding:10px 25px;padding-bottom:0px;word-break:break-word;">
                                <!--[if mso | IE]>
                <table
                    align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                >
                    <tr>
                
                        <td>
                        <![endif]-->
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                    <tr>
                                    <td style="padding:4px;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#DEDEDE;border-radius:6px;width:30;">
                                        <tr>
                                            <td style="font-size:0;height:30;vertical-align:middle;width:30;">
                                            <a href="[[SHORT_PERMALINK]]" target="_blank">
                                                <img height="30" src="http://saas-templates-creator.mailjet.com/saas-templates-creator/static/img/facebook_black.png" style="border-radius:6px;" width="30" />
                                            </a>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </table>
                                <!--[if mso | IE]>
                        </td>
                        
                        <td>
                        <![endif]-->
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                    <tr>
                                    <td style="padding:4px;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#DEDEDE;border-radius:6px;width:30;">
                                        <tr>
                                            <td style="font-size:0;height:30;vertical-align:middle;width:30;">
                                            <a href="[[SHORT_PERMALINK]]" target="_blank">
                                                <img height="30" src="http://saas-templates-creator.mailjet.com/saas-templates-creator/static/img/twitter_black.png" style="border-radius:6px;" width="30" />
                                            </a>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </table>
                                <!--[if mso | IE]>
                        </td>
                        
                        <td>
                        <![endif]-->
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                    <tr>
                                    <td style="padding:4px;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#DEDEDE;border-radius:6px;width:30;">
                                        <tr>
                                            <td style="font-size:0;height:30;vertical-align:middle;width:30;">
                                            <a href="[[SHORT_PERMALINK]]" target="_blank">
                                                <img height="30" src="http://saas-templates-creator.mailjet.com/saas-templates-creator/static/img/linkedin_black.png" style="border-radius:6px;" width="30" />
                                            </a>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    </tr>
                                </table>
                                <!--[if mso | IE]>
                        </td>
                        
                    </tr>
                    </table>
                <![endif]-->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="font-size:0px;padding:0px 20px 0px 20px;padding-top:0px;padding-bottom:0px;word-break:break-word;">
                                <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:11px;line-height:22px;text-align:center;color:#797e82;">
                                    <p style="margin: 10px 0;">C<a target="_blank" rel="noopener noreferrer" style="color:inherit; text-decoration:none" href="[[UNSUB_LINK_EN]]">lick <span style="color:#DEDEDE"><u>here</u></span> to unsubscribe</a>.<br /><span style="font-size:10px">Created by&nbsp;</span><a target="_blank" rel="noopener noreferrer" style="font-size:10px; color:inherit; text-decoration: none" href="https://www.mailjet.com/?utm_source=saas_email_templates&amp;utm_medium=logo_footer_email&amp;utm_campaign=account_activation"><span style="color:#DEDEDE"><u>Mailjet</u></span></a></p>
                                </div>
                                </td>
                            </tr>
                            </table>
                        </div>
                        <!--[if mso | IE]>
                        </td>
                    
                    </tr>
                
                            </table>
                            <![endif]-->
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <!--[if mso | IE]>
                    </td>
                    </tr>
                </table>
                <![endif]-->
            </div>
            </body>

            </html>
            """
        mensaje = "" + html1 + html2 + html4 + html5 + html6 +  html8  +  html10
        return mensaje

    
    @classmethod
    def desencriptar_enlace(self, enlace_encriptado: str):
        try:
            # Desencriptar el enlace
            cadena_activacion_encriptada = base64.urlsafe_b64decode(enlace_encriptado).decode()
            LogsServices.write(cadena_activacion_encriptada)
            cadena_activacion_desencriptada_bytes = self.decrypt(cadena_activacion_encriptada, self.key)
            LogsServices.write(f'cadena_activacion_desencriptada_bytes: {cadena_activacion_desencriptada_bytes}')
            cadena_activacion_desencriptada = cadena_activacion_desencriptada_bytes.decode()
            LogsServices.write(f'cadena_activacion_desencriptada: {cadena_activacion_desencriptada}')
            token, id_cuenta = cadena_activacion_desencriptada.split(':')
            LogsServices.write(f'token: {token}')
            LogsServices.write(f'id_cuenta: {id_cuenta}')
            return id_cuenta, token, True
        
        except Exception as e:
            return e, None, False
        
    @classmethod
    def encrypt(self, message: bytes, key: bytes) -> bytes:
        LogsServices.write(f'key: {key}')
        return Fernet(key).encrypt(message)


    @classmethod
    def decrypt(self, token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)