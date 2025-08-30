import socket       
import sqlite3       
from datetime import datetime  
import sys           


HOST = "127.0.0.1"  
PORT = 5000        
DB_PATH = "mensajes.db"  
BUFFER_SIZE = 1024       # Tamaño máximo de mensaje a recibir

def crear_base_de_datos(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"[ERROR DB] No se pudo crear/acceder a la base: {e}")
        sys.exit(1)
    finally:
        conn.close()

def inicializar_servidor(host, port):#Creamos un socket TCP/IP y lo preparamos para escuchar conexiones.

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        server_socket.bind((host, port))  # Asociar IP y puerto
        server_socket.listen(5)           # Máx. 5 conexiones en cola
        print(f"[INFO] Servidor escuchando en {host}:{port}")
        return server_socket
    except OSError as e:
        print(f"[ERROR SOCKET] No se pudo iniciar el servidor: {e}")
        sys.exit(1)

def guardar_mensaje(db_path, contenido, ip_cliente): #Inserta un mensaje en la base con la fecha actual y la IP del cliente.

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        fecha_envio = datetime.now().isoformat(timespec='seconds')  # Timestamp
        cur.execute("""
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        """, (contenido, fecha_envio, ip_cliente))
        conn.commit()
        return fecha_envio
    except sqlite3.Error as e:
        print(f"[ERROR DB] No se pudo guardar el mensaje: {e}")
        return None
    finally:
        conn.close()


def manejar_cliente(conn, addr, db_path):

    print(f"[INFO] Cliente conectado desde {addr}")
    
    while True:
        try:
            # Recibir mensaje 
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break  
            
            mensaje = data.decode("utf-8").strip()
            
            if mensaje.lower() == "éxito":
                print(f"[INFO] Cliente {addr} finalizó la conexión")
                break
            
            # Guardar mensaje en la base de datos
            fecha_envio = guardar_mensaje(db_path, mensaje, addr[0])
            
            if fecha_envio:
                respuesta = f"Mensaje recibido: {fecha_envio}"
                conn.sendall(respuesta.encode("utf-8"))
                print(f"[INFO] Mensaje guardado y respondido: {mensaje}")
            else:
                conn.sendall("Error al guardar el mensaje".encode("utf-8"))
            
        except Exception as e:
            print(f"[ERROR] Ocurrió un error con el cliente {addr}: {e}")
            break
    
    conn.close()

def aceptar_conexiones(server_socket, db_path):

    while True:
        try:
            conn, addr = server_socket.accept()  # Espera un cliente
            manejar_cliente(conn, addr, db_path)
        except KeyboardInterrupt:
            print("\n[INFO] Servidor detenido manualmente")
            server_socket.close()
            break
        except Exception as e:
            print(f"[ERROR] Ocurrió un error al aceptar conexiones: {e}")

if __name__ == "__main__":
    crear_base_de_datos(DB_PATH)
    server_socket = inicializar_servidor(HOST, PORT)
    aceptar_conexiones(server_socket, DB_PATH)