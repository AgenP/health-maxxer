"""Serve the prototype and a live photo-extraction endpoint.

Usage: ../../health-maxxer-image-evals/.venv/bin/python app/server.py  (from the repo root), then open http://localhost:8780
Reuses the image-capture eval's prompt, schema and request (evals/image-capture/run_eval.py) unchanged.
"""
import base64, json, pathlib, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

APP = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(APP.parent / "evals" / "image-capture"))
sys.path.insert(0, str(APP))

import anthropic
import run_eval
from estimate import map_extraction

run_eval.load_env()
CLIENT = anthropic.Anthropic()


def extract(data_url, text):
    header, b64 = data_url.split(",", 1)
    media = header.split(";")[0].split(":")[1]
    req = run_eval.build_request("claude-opus-5-5", "medium", media, b64)
    if text:
        req["messages"][0]["content"][1]["text"] += f' The person also typed: "{text}".'
    resp = CLIENT.beta.messages.create(**req)
    return json.loads(next(b.text for b in resp.content if b.type == "text"))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(APP), **kw)

    def do_POST(self):
        if self.path != "/api/extract":
            self.send_error(404)
            return
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        try:
            out = map_extraction(extract(body["image"], body.get("text", "")))
            code = 200
        except Exception as e:
            out, code = {"error": str(e)}, 502
        raw = json.dumps(out).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


if __name__ == "__main__":
    print("http://localhost:8780")
    ThreadingHTTPServer(("127.0.0.1", 8780), Handler).serve_forever()
