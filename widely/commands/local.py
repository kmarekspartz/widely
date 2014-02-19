"""
Serve this site locally.
"""

import sys
import SimpleHTTPServer
import SocketServer


class MyTCPServer(SocketServer.TCPServer):
    """
    Release the socket when killed.
    """
    allow_reuse_address = True


def local(arguments):
    """
    Runs the site in a local server on port 8000 or specified port.

    Usage: widely local [-p <PORT> | --port <PORT>]
    """
    host = '0.0.0.0'
    port = arguments['<PORT>']
    if port:
        try:
            port = int(port)
        except ValueError:
            print('<PORT> must be an integer.')
            sys.exit(1)
    else:
        port = 8000
        
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = MyTCPServer((host, port), Handler)
    url = 'http://' + host + ':' + str(port)
    print("serving at " + url)
    import webbrowser

    webbrowser.open_new_tab(url)
    httpd.serve_forever()
