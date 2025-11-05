#openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -nodes -subj "/CN=localhost"
#!/usr/bin/env python3
import http.server
import socketserver
import ssl
import sys
from pathlib import Path

HOST = "0.0.0.0"
PORT = 8443

# Accept cert/key paths via CLI, else default to server.crt/server.key in CWD
cert_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("server.crt")
key_path  = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("server.key")

class QuietLoggingHandler(http.server.SimpleHTTPRequestHandler):
    # Serve files from the current directory; override logging if you want less noise
    def log_message(self, fmt, *args):
        print("%s - - [%s] %s" % (self.client_address[0],
                                  self.log_date_time_string(),
                                  fmt % args))

if __name__ == "__main__":
    # Serve files from the working directory
    handler = QuietLoggingHandler

    with socketserver.ThreadingTCPServer((HOST, PORT), handler) as httpd:
        httpd.daemon_threads = True  # handle each request in its own thread

        # Create a modern TLS context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # Disable old/broken protocols & ciphers by default settings (Python does this reasonably)
        # Load your cert & private key
        context.load_cert_chain(certfile=str(cert_path), keyfile=str(key_path))

        # Wrap the server socket with TLS
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

        print(f"Serving HTTPS on https://{HOST}:{PORT} (ctrl+c to quit)")
        print(f"Using cert: {cert_path.resolve()}")
        print(f"Using key : {key_path.resolve()}")
        httpd.serve_forever()
