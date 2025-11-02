# client.py
import socket
import json

HOST = 'localhost'  
PORT = 5000         

def main():
    print("=" * 50)
    print(" CLIENTE - Sistema Distribuido ")
    print("=" * 50)

    while True:
        print("\nSelecciona una tarea:")
        print("1. Invertir texto")
        print("2. Calcular promedio de números")
        print("3. Contar caracteres en un texto")
        print("4. Salir")

        opcion = input("\nTu elección: ")

        if opcion == '1':
            texto = input("Ingresa un texto: ")
            task = {"type": "invertir_texto", "data": texto}

        elif opcion == '2':
            numeros = input("Ingresa números separados por comas (ej: 10, 20, 30): ")
            lista = [float(x.strip()) for x in numeros.split(',')]
            task = {"type": "promedio", "data": lista}

        elif opcion == '3':
            texto = input("Ingresa un texto: ")
            task = {"type": "contar_caracteres", "data": texto}

        elif opcion == '4':
            print("Cerrando cliente...")
            break

        else:
            print("Opción no válida. Intenta otra vez.")
            continue

        # Enviar la tarea al servidor
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))

            client_socket.send(json.dumps(task).encode('utf-8'))

            # Recibir la respuesta del servidor
            respuesta = client_socket.recv(1024).decode('utf-8')
            print(f"\n Respuesta del servidor: {respuesta}")

            client_socket.close()

        except Exception as e:
            print(f"\n Error de conexión: {e}")

if __name__ == "__main__":
    main()
