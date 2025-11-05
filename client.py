import ssl
import socket

hostname = '127.0.0.1'
port = 8443

# Create a default context, but disable verification for local/self-signed testing
context = ssl._create_unverified_context()

with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print("TLS version:", ssock.version())
        print("Cipher used:", ssock.cipher())
        print("Peer cert subject:", ssock.getpeercert().get('subject', '(no cert)'))