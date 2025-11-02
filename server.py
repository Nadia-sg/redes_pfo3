# server.py
import socket
import json
import threading

HOST = 'localhost'
PORT = 5000


def procesar_tarea(task):
    """
    Procesa la tarea según su tipo.
    """
    tipo = task.get("type")
    data = task.get("data")

    if tipo == "invertir_texto":
        return data[::-1]

    elif tipo == "promedio":
        if not isinstance(data, list) or len(data) == 0:
            return "Error: lista vacía o no válida"
        promedio = sum(data) / len(data)
        return f"El promedio es {promedio:.2f}"

    elif tipo == "contar_caracteres":
        return f"El texto tiene {len(data)} caracteres"

    else:
        return "Tipo de tarea desconocido"


def manejar_cliente(conn, addr):
    """
    Función que maneja la conexión con un cliente.
    Se ejecuta en un hilo separado.
    """
    print(f"[WORKER-{threading.current_thread().name}] Conectado con {addr}")

    try:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            return

        task = json.loads(data)
        print(f"[WORKER-{threading.current_thread().name}] Tarea recibida: {task['type']}")

        resultado = procesar_tarea(task)
        respuesta = f"Procesado por {threading.current_thread().name}: {resultado}"

        conn.send(respuesta.encode('utf-8'))
        print(f"[WORKER-{threading.current_thread().name}] Respuesta enviada\n")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()


def iniciar_servidor():
    """
    Inicia el servidor principal y crea un hilo por cliente.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}...\n")

    try:
        while True:
            conn, addr = server_socket.accept()
            # crear un thread para atender al cliente
            worker = threading.Thread(target=manejar_cliente, args=(conn, addr))
            worker.start()
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Apagando servidor...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    iniciar_servidor()
