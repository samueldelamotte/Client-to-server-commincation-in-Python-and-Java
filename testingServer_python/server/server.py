#!/usr/bin/env python3
"""
- CGIHTTPRequestHandler used for do_GET, do_PUT... aka. the request handler.
- HTTPServer used for the server class
- cgitb used for error traceback, presented in the html page.
- ssl used to wrap the socket on which the server is running
"""
from http.server import CGIHTTPRequestHandler, HTTPServer
import ssl
import cgitb
cgitb.enable()


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: RUNS A HTTP SERVER USING THE CGI HTTP REQUEST HANDLER AND WRAPS IT WITH SSL
# RETURNS: NOTHING
def run(server_class=HTTPServer, handler=CGIHTTPRequestHandler):
    server_address = ("", 443)                                     # connect via "https://localhost:443"
    httpd = server_class(server_address, handler)                   # creates httpd object
    handler.have_fork = False
    httpd.socket = ssl.wrap_socket(httpd.socket,                    # wraps server socket
                                   certfile='../data/cert.pem',     # ssl self signed certificate
                                   keyfile='../data/key.pem',       # ssl keyfile
                                   server_side=True)
    httpd.serve_forever()                                           # keep server running


# ---------------------------------------------------------------------------------------------------------------------
run()  # RUN THE SERVER
