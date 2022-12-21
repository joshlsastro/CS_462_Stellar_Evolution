from wsgiref.simple_server import make_server

PORT = 8888

doctypes = {
    "gz": "application/gzip",
    "html": "text/html",
    "ico": "image/x-icon",
    "css": "text/css",
    "js": "text/javascript",
    "png": "image/png",
    "data": "application/octet-stream",
    "wasm": "application/wasm"
}

def application(environ, start_response):
    """Main application."""
    path = environ["PATH_INFO"]
    if path == "/":
        filename = "index.html"
    else:
        filename = path[1:]
    response_headers = []
    try:
        with open(filename, "rb") as f:
            output = f.read()
        extension = filename.split(".")[-1]
        if extension == "gz":
            response_headers.append(("Content-Encoding", "gzip"))
            mime = doctypes[filename.split(".")[-2]]
        else:
            mime = doctypes[extension]
        status = "200 OK"
        response_headers.append(("Content-type", mime))
    except IOError:
        # File not found
        status = "404 Not Found"
        response_headers = [("Content-type", "text/plain")]
        output = "File not found.".encode()
    # Final part
    start_response(status, response_headers)
    return [output]

httpd = make_server('', PORT, application)
print("Serving HTTP on port %s..." % PORT)
print("Go to http://127.0.0.1:%s" % PORT)
httpd.serve_forever()
