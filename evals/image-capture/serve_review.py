"""Local review app for image-capture eval runs.

Usage: .venv/bin/python evals/image-capture/serve_review.py [--run claude-opus-5-5__medium] [--port 8765]
Then open http://localhost:8765/review.html
Labels auto-save to evals/image-capture/review/labels-<run>.json
"""
import argparse, json, pathlib, random
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = pathlib.Path(__file__).resolve().parent


def load_traces(run, seed):
    gold = {}
    for f in sorted(ROOT.glob("labels-*.jsonl")):
        for line in f.read_text().splitlines():
            if line.strip():
                g = json.loads(line)
                gold[g["id"]] = g
    preds = [json.loads(l) for l in (ROOT / "preds" / f"{run}.jsonl").read_text().splitlines() if l.strip()]
    traces = [{"id": p["id"], "gold": gold.get(p["id"], {}), "pred": p} for p in preds]
    random.Random(seed).shuffle(traces)
    return traces


def make_handler(run, seed):
    labels_path = ROOT / "review" / f"labels-{run}.json"
    labels_path.parent.mkdir(exist_ok=True)

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(ROOT), **kw)

        def _json(self, obj, code=200):
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/api/traces":
                cfg_path = ROOT / "preds" / f"{run}.config.json"
                cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else None
                return self._json({"run": run, "config": cfg, "traces": load_traces(run, seed)})
            if self.path == "/api/labels":
                return self._json(json.loads(labels_path.read_text()) if labels_path.exists() else {})
            return super().do_GET()

        def do_POST(self):
            if self.path != "/api/labels":
                return self._json({"error": "not found"}, 404)
            data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            tmp = labels_path.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, indent=2))
            tmp.replace(labels_path)
            return self._json({"ok": True, "saved": len(data)})

        def log_message(self, *a):
            pass

    return Handler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="claude-opus-5-5__medium")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    print(f"http://localhost:{a.port}/review.html  (run={a.run})")
    ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(a.run, a.seed)).serve_forever()


if __name__ == "__main__":
    main()
