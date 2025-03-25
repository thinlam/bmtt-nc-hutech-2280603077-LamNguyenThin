import socket
import ssl
import threading
import os

# Server information
server_address = ('localhost', 12345)

# List of connected clients
clients = []
clients_lock = threading.Lock()  # Lock for thread-safe operations on clients list

def handle_client(client_socket):
    # Add client to list
    with clients_lock:
        clients.append(client_socket)
    print("Đã kết nối với:", client_socket.getpeername())

    try:
        # Receive and send data
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))
            
            # Send data to all other clients
            with clients_lock:
                for client in clients[:]:  # Create a copy of the list for iteration
                    if client != client_socket:
                        try:
                            client.send(data)
                        except:
                            clients.remove(client)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Clean up client connection
        print("Đã ngắt kết nối:", client_socket.getpeername())
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
        client_socket.close()

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

print("Server đang chờ kết nối...")

# Listen for connections
while True:
    client_socket, client_address = server_socket.accept()
    
    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    try:
        # Use absolute path or verify relative path is correct
        cert_path = os.path.join(os.path.dirname(__file__), "certificates", "server-cert.crt")
        key_path = os.path.join(os.path.dirname(__file__), "certificates", "server-key.key")
        
        context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    except FileNotFoundError as e:
        print(f"Error: SSL certificate files not found: {e}")
        client_socket.close()
        continue
    
    # Establish SSL connection
    try:
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
        client_socket.close()
        continue
    
    # Start a new thread for each client
    client_thread = threading.Thread(target=handle_client, args=(ssl_socket,))
    client_thread.start()