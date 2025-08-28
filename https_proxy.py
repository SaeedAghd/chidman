#!/usr/bin/env python
"""
Simple HTTPS Proxy Server for Django
"""
import ssl
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.parse

class HTTPSProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Forward request to Django server
            url = f"http://127.0.0.1:8000{self.path}"
            req = urllib.request.Request(url)
            
            # Copy headers
            for header, value in self.headers.items():
                req.add_header(header, value)
            
            # Make request to Django
            with urllib.request.urlopen(req) as response:
                # Send response headers
                self.send_response(response.status)
                for header, value in response.getheaders():
                    self.send_header(header, value)
                self.end_headers()
                
                # Send response body
                self.wfile.write(response.read())
                
        except Exception as e:
            self.send_error(500, f"Proxy Error: {str(e)}")
    
    def do_POST(self):
        try:
            # Get request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Forward request to Django server
            url = f"http://127.0.0.1:8000{self.path}"
            req = urllib.request.Request(url, data=post_data, method='POST')
            
            # Copy headers
            for header, value in self.headers.items():
                if header.lower() != 'content-length':
                    req.add_header(header, value)
            
            # Make request to Django
            with urllib.request.urlopen(req) as response:
                # Send response headers
                self.send_response(response.status)
                for header, value in response.getheaders():
                    self.send_header(header, value)
                self.end_headers()
                
                # Send response body
                self.wfile.write(response.read())
                
        except Exception as e:
            self.send_error(500, f"Proxy Error: {str(e)}")
    
    def log_message(self, format, *args):
        # Disable logging for cleaner output
        pass

def run_https_proxy():
    """Run HTTPS proxy server"""
    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    
    # Create server
    server = HTTPServer(('127.0.0.1', 8443), HTTPSProxyHandler)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    
    print("🔒 HTTPS Proxy Server running on https://127.0.0.1:8443")
    print("📡 Forwarding requests to http://127.0.0.1:8000")
    print("🌐 Access your Django app at: https://127.0.0.1:8443")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()

if __name__ == "__main__":
    run_https_proxy()
