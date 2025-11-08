from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server


class LoginService(ServiceBase):
    """
    Servicio SOAP que simula un proceso de LOGIN.
    Credenciales quemadas solo con fines académicos.
    """

    # "Base de datos" simulada de usuarios válidos
    USERS = {
        "admin": "1234",
        "user": "abcd",
        "fernando": "password"
    }

    @rpc(Unicode, Unicode, _returns=Unicode)
    def login(ctx, username, password):
        """
        Recibe usuario y contraseña.
        Regresa un mensaje indicando resultado del login.
        """
        if username in LoginService.USERS and LoginService.USERS[username] == password:
            return f"Login correcto. Bienvenido, {username}."
        else:
            return "Login incorrecto. Credenciales inválidas."


# Definimos la aplicación SOAP
soap_app = Application(
    [LoginService],
    'tns:login.soap',                # Namespace específico para el servicio de login
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Adaptador WSGI
wsgi_app = WsgiApplication(soap_app)


if __name__ == "__main__":
    # Puerto independiente para este proyecto (no usamos el de temperaturas)
    server = make_server('0.0.0.0', 8002, wsgi_app)
    print("Servicio SOAP Login corriendo en http://localhost:8002")
    print("WSDL disponible en               http://localhost:8002/?wsdl")
    server.serve_forever()
