import socket


HOST = "127.0.0.1"  
PORT = 5000

# Crear socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
    print(f"[INFO] Conectado al servidor en {HOST}:{PORT}")
except Exception as e:
    print(f"[ERROR] No se pudo conectar al servidor: {e}")
    exit(1)

# Bucle para enviar múltiples mensajes
while True:
    mensaje = input("Escribí un mensaje (o 'éxito' para salir): ").strip()
    if not mensaje:
        continue
    
    client_socket.sendall(mensaje.encode("utf-8"))
    
    if mensaje.lower() == "éxito":
        print("[INFO] Cerrando conexión...")
        break
    
    # Esperar respuesta del servidor
    data = client_socket.recv(1024).decode("utf-8")
    print("Servidor:", data)

client_socket.close()
