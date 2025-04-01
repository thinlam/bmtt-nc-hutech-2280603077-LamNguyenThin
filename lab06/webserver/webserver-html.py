import socket
import os

def handle_request(client_socket, request_data):
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if "GET /admin" in request_data:
            file_path = os.path.join(script_dir, "admin.html")
        else:
            file_path = os.path.join(script_dir, "index.html")
        
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n\r\n"
                    + file.read()
                )
        else:
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n\r\n"
                "<h1>404 Not Found</h1>"
                f"<p>File not found: {os.path.basename(file_path)}</p>"
            )
        
        client_socket.sendall(response.encode('utf-8'))
    
    except Exception as e:
        print(f"Error: {e}")
        error_response = (
            "HTTP/1.1 500 Internal Server Error\r\n"
            "Content-Type: text/html\r\n\r\n"
            "<h1>500 Server Error</h1>"
        )
        client_socket.sendall(error_response.encode('utf-8'))
    
    finally:
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    print("Server running on http://127.0.0.1:8080")
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            request_data = client_socket.recv(1024).decode('utf-8')
            print(f"Request from {addr}: {request_data.splitlines()[0]}")
            handle_request(client_socket, request_data)
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()