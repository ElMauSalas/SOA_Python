from zeep import Client

def main():
    # URL del WSDL del servicio de calculadora (SOAP)
    wsdl = 'http://www.dneonline.com/calculator.asmx?WSDL'

    # Crear el cliente SOAP
    client = Client(wsdl=wsdl)

    # --- Operaciones de ejemplo ---

    result1 = client.service.Add(intA=5, intB=10)
    print(f'La suma de 5 y 10 es: {result1}')

    result2 = client.service.Divide(intA=4, intB=10)
    print(f'La división de 4 entre 10 es: {result2}')

    result3 = client.service.Multiply(intA=5, intB=10)
    print(f'La multiplicación de 5 y 10 es: {result3}')

    result4 = client.service.Subtract(intA=20, intB=8)
    print(f'La resta de 20 menos 8 es: {result4}')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:

        print(f'Error al consumir el servicio SOAP: {e}')
