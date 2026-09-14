from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")


# 保存されている旅行記を読み込む
def load_records():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# 旅行記を保存する
def save_records(records):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


class MyHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        # トップページ
        if self.path == "/":
            file_path = os.path.join(
                BASE_DIR,
                "templates",
                "index.html"
            )

            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()

            records = load_records()

            # 旅行記をHTMLにする
            record_html = ""

            for record in records:
                record_html += f"""
                <div class="record">
                    <h3>{record["place"]}</h3>
                    <p class="date">{record["date"]}</p>
                    <p>{record["memory"]}</p>
                </div>
                """

            # {{RECORDS}} を旅行記一覧に置き換える
            html = html.replace("{{RECORDS}}", record_html)

            self.send_response(200)
            self.send_header(
                "Content-type",
                "text/html; charset=utf-8"
            )
            self.end_headers()

            self.wfile.write(html.encode("utf-8"))

        # CSS
        elif self.path == "/static/style.css":

            file_path = os.path.join(
                BASE_DIR,
                "static",
                "style.css"
            )

            with open(file_path, "r", encoding="utf-8") as f:
                css = f.read()

            self.send_response(200)
            self.send_header(
                "Content-type",
                "text/css; charset=utf-8"
            )
            self.end_headers()

            self.wfile.write(css.encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    # POST
    def do_POST(self):

        if self.path == "/save":

            # 送られてきたデータの大きさ
            content_length = int(
                self.headers["Content-Length"]
            )

            # データを受け取る
            body = self.rfile.read(content_length).decode("utf-8")

            # データを整理する
            data = parse_qs(body)

            place = data.get("place", [""])[0]
            date = data.get("date", [""])[0]
            memory = data.get("memory", [""])[0]

            # 新しい旅行記
            new_record = {
                "place": place,
                "date": date,
                "memory": memory
            }

            # 今までの旅行記を取得
            records = load_records()

            # 新しい旅行記を追加
            records.append(new_record)

            # 保存
            save_records(records)

            # トップページへ戻る
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()


server_address = ("", 8000)

httpd = HTTPServer(server_address, MyHandler)

print(" 旅行記録アプリを起動しました")
print("http://localhost:8000")

httpd.serve_forever()