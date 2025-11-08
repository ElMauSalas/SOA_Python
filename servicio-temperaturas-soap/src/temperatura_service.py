from spyne import Application, rpc, ServiceBase, Double
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server


class TemperaturaService(ServiceBase):
    """
    Servicio SOAP para conversiones de temperatura.
    Incluye:
    - Celsius a Fahrenheit
    - Fahrenheit a Celsius
    - Celsius a Kelvin
    """

    @rpc(Double, _returns=Double)
    def celsius_a_fahrenheit(ctx, celsius):
        """
        Convierte de grados Celsius a Fahrenheit.
        Fórmula: F = C * 9/5 + 32
        """
        return (celsius * 9.0 / 5.0) + 32.0

    @rpc(Double, _returns=Double)
    def fahrenheit_a_celsius(ctx, fahrenheit):
        """
        Convierte de grados Fahrenheit a Celsius.
        Fórmula: C = (F - 32) * 5/9
        """
        return (fahrenheit - 32.0) * 5.0 / 9.0

    @rpc(Double, _returns=Double)
    def celsius_a_kelvin(ctx, celsius):
        """
        Convierte de grados Celsius a Kelvin.
        Fórmula: K = C + 273.15
        """
        return celsius + 273.15


# Definimos la aplicación SOAP
soap_app = Application(
    [TemperaturaService],                   # Servicios expuestos
    'tns:temperaturas.soap',               # Namespace del servicio
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Adaptador WSGI
wsgi_app = WsgiApplication(soap_app)


if __name__ == "__main__":
    # Levantar el servidor en localhost:8000
    server = make_server('0.0.0.0', 8000, wsgi_app)
    print("Servicio SOAP Temperaturas corriendo en http://localhost:8000")
    print("WSDL disponible en                         http://localhost:8000/?wsdl")
    server.serve_forever()
