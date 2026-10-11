import base64
import json
import types

import run_eval


class FakeMessages:
    def __init__(self):
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        text = types.SimpleNamespace(type="text", text=json.dumps({"subject_type": "not_food"}))
        usage = types.SimpleNamespace(input_tokens=1, output_tokens=1)
        return types.SimpleNamespace(model="m", stop_reason="end_turn", usage=usage, content=[text])


def fake_client():
    m = FakeMessages()
    return types.SimpleNamespace(beta=types.SimpleNamespace(messages=m)), m


def test_predict_sends_pinned_request():
    client, m = fake_client()
    row = {"id": "off-0001", "set": "off-packaging", "file": "images/off/off-0001.jpg"}
    run_eval.predict(client, "claude-opus-5-5", "medium", row)
    data = base64.standard_b64encode((run_eval.ROOT / row["file"]).read_bytes()).decode()
    assert m.kwargs == {
        "model": "claude-opus-5-5",
        "max_tokens": 4000,
        "system": run_eval.SYSTEM,
        "output_config": {"effort": "medium", "format": {"type": "json_schema", "schema": run_eval.SCHEMA}},
        "betas": ["server-side-fallback-2026-07-01"],
        "extra_body": {"fallbacks": "default"},
        "messages": [{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}},
            {"type": "text", "text": "Extract the facts from this photo."},
        ]}],
    }


def test_request_config_redacts_image_but_matches_request():
    cfg = run_eval.request_config("claude-opus-5-5", "medium")
    client, m = fake_client()
    run_eval.predict(client, "claude-opus-5-5", "medium", {"id": "x", "set": "s", "file": "images/off/off-0001.jpg"})
    sent = json.loads(json.dumps(m.kwargs))
    sent["messages"][0]["content"][0]["source"]["data"] = "<base64 image bytes>"
    assert cfg == sent
