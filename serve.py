# Local preview of the built site (dist/), visible only on this computer.
# Sends no-cache headers so the browser always shows the latest build.
#   python3 serve.py        → http://127.0.0.1:8765/
import functools, http.server, os

PORT = 8765
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()


handler = functools.partial(NoCache, directory=ROOT)
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler).serve_forever()
