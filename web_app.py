"""A small localhost-only upload interface for MarkItDown."""

from __future__ import annotations

import html
import io
import re
import threading
import webbrowser
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from markitdown import MarkItDown


HOST = "127.0.0.1"
PORT = 8765
MAX_UPLOAD_BYTES = 100 * 1024 * 1024
DESKTOP = Path.home() / "Desktop"
CONVERTER = MarkItDown()


PAGE = """<!doctype html>
<html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MarkItDown</title>
<style>
 body{font:16px system-ui,sans-serif;max-width:680px;margin:10vh auto;padding:0 22px;color:#172033;background:#f5f7fb}
 main{background:white;padding:32px;border-radius:16px;box-shadow:0 8px 32px #14224414}h1{margin-top:0}
 input,button{font:inherit}input[type=file]{display:block;margin:24px 0}button{border:0;border-radius:8px;background:#255be8;color:white;padding:12px 20px;cursor:pointer}
 .note{color:#596579;font-size:14px}.result{background:#eef8f0;padding:16px;border-radius:8px;margin-top:20px;overflow-wrap:anywhere}
</style><main><h1>Dosyayı Markdown’a dönüştür</h1>
<p>Bir dosya seç. Oluşan <code>.md</code> dosyası doğrudan Masaüstüne kaydedilecek.</p>
<form method="post" enctype="multipart/form-data"><input type="file" name="file" required>
<button type="submit">Dönüştür ve Masaüstüne kaydet</button></form>
<p class="note">Bu arayüz yalnızca bu bilgisayarda açılır. En fazla 100 MB dosya yükleyebilirsin.</p>{message}</main></html>"""


def page(message: str = "") -> bytes:
    return PAGE.replace("{message}", message).encode("utf-8")


def safe_stem(filename: str) -> str:
    stem = Path(filename.replace("\\", "/")).name.rsplit(".", 1)[0]
    stem = re.sub(r"[^\w.-]+", "_", stem, flags=re.UNICODE).strip("._")
    return stem or "donusturuldu"


def output_path(stem: str) -> Path:
    candidate = DESKTOP / f"{stem}.md"
    number = 1
    while candidate.exists():
        candidate = DESKTOP / f"{stem}_{number}.md"
        number += 1
    return candidate


class Handler(BaseHTTPRequestHandler):
    def send_page(self, body: bytes, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        self.send_page(page())

    def do_POST(self) -> None:
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > MAX_UPLOAD_BYTES:
                raise ValueError("Dosya boş veya 100 MB sınırını aşıyor.")
            content_type = self.headers.get("Content-Type", "")
            if not content_type.lower().startswith("multipart/form-data"):
                raise ValueError("Dosya yükleme formu bekleniyordu.")
            message = BytesParser(policy=policy.default).parsebytes(
                f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("ascii")
                + self.rfile.read(size)
            )
            uploaded = next(
                (
                    part
                    for part in message.iter_parts()
                    if part.get_param("name", header="content-disposition") == "file"
                ),
                None,
            )
            filename = uploaded.get_filename() if uploaded else None
            if uploaded is None or not filename:
                raise ValueError("Lütfen bir dosya seç.")
            source = uploaded.get_payload(decode=True) or b""
            if len(source) > MAX_UPLOAD_BYTES:
                raise ValueError("Dosya 100 MB sınırını aşıyor.")
            result = CONVERTER.convert_stream(
                io.BytesIO(source),
                file_extension=Path(filename).suffix,
            )
            DESKTOP.mkdir(parents=True, exist_ok=True)
            destination = output_path(safe_stem(filename))
            destination.write_text(result.markdown, encoding="utf-8")
            msg = f'<div class="result"><strong>Tamamlandı.</strong><br>{html.escape(str(destination))}</div>'
            self.send_page(page(msg))
        except Exception as exc:
            msg = f'<div class="result">Dönüştürme başarısız: {html.escape(str(exc))}</div>'
            self.send_page(page(msg), 400)

    def log_message(self, format: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {format % args}")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}"
    print(f"MarkItDown arayüzü hazır: {url}")
    print("Durdurmak için Terminal’de Ctrl+C tuşlarına basın.")
    threading.Timer(1, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArayüz kapatılıyor.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
