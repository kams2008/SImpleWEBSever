
import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

server.listen(5)

print("Web Server Started Successfully!")
print("Open http://127.0.0.1:8080 in your browser")

while True:

    client, address = server.accept()

    print("Client connected:", address)

    request = client.recv(1024).decode("utf-8", errors="replace")

    if not request:
        client.close()
        continue

    request_line = request.splitlines()[0]
    parts = request_line.split()

    if len(parts) < 2:
        client.close()
        continue

    method = parts[0]
    path = parts[1]

    if method == "GET" and path in ("/", "/index.html"):

        with open("index.html", "rb") as file:
            content = file.read()

        status = "200 OK"

    elif method != "GET":

        status = "405 Method Not Allowed"
        content = b"<h1>405 Method Not Allowed</h1>"

    else:

        status = "404 Not Found"
        content = b"<h1>404 Page Not Found</h1>"

    response = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8") + content

    client.sendall(response)

    client.close()
