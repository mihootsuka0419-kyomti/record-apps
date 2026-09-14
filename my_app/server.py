from http.server import HTTPServer, BaseHTTPRequestHandler
import os


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            file_path = os.path.join(
                os.path.dirname(__file__),
                "templates",
                "index.html"
            )

            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            self.wfile.write(html.encode("utf-8"))

        elif self.path == "/static/style.css":

            file_path = os.path.join(
                os.path.dirname(__file__),
                "static",
                "style.css"
            )

            with open(file_path, "r", encoding="utf-8") as f:
                css = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/css; charset=utf-8")
            self.end_headers()

            self.wfile.write(css.encode("utf-8"))


server_address = ("", 8000)

httpd = HTTPServer(server_address, MyHandler)

print("🚀 サーバーを起動しました")
print("http://localhost:8000")

httpd.serve_forever()