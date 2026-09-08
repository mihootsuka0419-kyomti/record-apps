from http.server import HTTPServer, BaseHTTPRequestHandler


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            with open("templates/index.html", "r", encoding="utf-8") as f:
                html = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            self.wfile.write(html.encode("utf-8"))

        elif self.path == "/static/style.css":
            with open("static/style.css", "r", encoding="utf-8") as f:
                css = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/css; charset=utf-8")
            self.end_headers()

            self.wfile.write(css.encode("utf-8"))


server = HTTPServer(("", 8000), MyHandler)

print("サーバー起動！")

server.serve_forever()