import ssl
import socket

hostname = 'www.psu.edu'
context = ssl.create_default_context()

with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print("TLS version:", ssock.version())
        print("Cipher used:", ssock.cipher())