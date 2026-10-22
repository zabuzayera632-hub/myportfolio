# Local preview of the built site (dist/), visible only on this computer.
# Sends no-cache headers so the browser always shows the latest build.
#   python3 serve.py        → http://127.0.0.1:8765/
import errno, functools, http.server, os

PORT = 8765
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
URL = f"http://127.0.0.1:{PORT}/"


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()


handler = functools.partial(NoCache, directory=ROOT)
try:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
except OSError as e:
    if e.errno == errno.EADDRINUSE:
        print(f"Сайт уже запущен — откройте {URL}")
        raise SystemExit(0)
    raise
print(f"Сайт работает: {URL}  (остановить — Ctrl+C)")
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nСервер остановлен.")
