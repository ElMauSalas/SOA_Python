from zeep import Client

def main():
    # URL del servicio SOAP (conversión de temperatura)
    wsdl_url = 'https://www.w3schools.com/xml/tempconvert.asmx?WSDL'

    client = Client(wsdl=wsdl_url)

    print("Lista de Métodos - Operaciones disponibles:")
    for service in client.wsdl.services.values():
        for port in service.ports.values():
            for op in port.binding._operations.values():
                print(" -", op.name)

    fahrenheit_value = 200
    celsius_result = client.service.FahrenheitToCelsius(Fahrenheit=fahrenheit_value)
    print(f'La conversión de {fahrenheit_value}°F a Celsius es: {celsius_result}°C')

    celsius_value = 45.8
    fahrenheit_result = client.service.CelsiusToFahrenheit(Celsius=celsius_value)
    print(f'La conversión de {celsius_value}°C a Fahrenheit es: {fahrenheit_result}°F')

    client2 = Client('https://www.w3schools.com/xml/tempconvert.asmx?WSDL')
    print("Conversión rápida de 400°F a Celsius:", client2.service.FahrenheitToCelsius("400"), "°C")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error al consumir el servicio SOAP: {e}')
