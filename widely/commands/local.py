import sys
import SimpleHTTPServer
import SocketServer


def local(arguments):
    """
    Runs the site in a local server on port 8000 or specified port.

    Usage: widely local [-p <PORT> | --port <PORT>]
    """
    ## killing this does not always free the port correctly
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
    httpd = SocketServer.TCPServer(("", port), Handler)
    url = 'http://0.0.0.0:' + str(port)
    print("serving at " + url)
    import webbrowser

    webbrowser.open_new_tab(url)
    httpd.serve_forever()
