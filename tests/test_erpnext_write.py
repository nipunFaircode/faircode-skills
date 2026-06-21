import json
from shared.erpnext_client.client import ERPNextClient


class FakeResp:
    def __init__(self, payload):
        self._p = json.dumps(payload).encode()

    def read(self):
        return self._p

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def client(confirm_value):
    posted = []

    def opener(req, timeout=60):
        posted.append((req.method, req.full_url, req.data))
        return FakeResp({"data": {"name": "TASK-0001"}})

    c = ERPNextClient(base_url="https://erp.test", token="k:s")
    c._opener = opener
    c._confirm = lambda summary: confirm_value
    c._posted = posted
    return c


def test_create_task_declined_does_not_post():
    c = client(confirm_value=False)
    result = c.create_task("PROJ-1", "Add field", "desc", "AC: field saves")
    assert result is None
    assert c._posted == []


def test_create_task_confirmed_posts():
    c = client(confirm_value=True)
    result = c.create_task("PROJ-1", "Add field", "desc", "AC: field saves")
    assert result["name"] == "TASK-0001"
    assert len(c._posted) == 1
    method, url, body = c._posted[0]
    assert method == "POST"
    assert "/api/resource/Task" in url
    sent = json.loads(body.decode())
    assert sent["project"] == "PROJ-1"
    assert "AC: field saves" in sent["description"]


def test_log_action_item_posts_todo():
    c = client(confirm_value=True)
    result = c.log_action_item("Send revised quote", "akhila@faircode.co",
                               reference_type="Task", reference_name="TASK-9")
    assert result["name"] == "TASK-0001"
    method, url, body = c._posted[0]
    assert method == "POST"
    assert "/api/resource/ToDo" in url
    sent = json.loads(body.decode())
    assert sent["allocated_to"] == "akhila@faircode.co"
    assert sent["reference_name"] == "TASK-9"


def test_confirmation_receives_payload():
    # the gate must surface the full payload to the user before they decide
    seen = {}

    c = client(confirm_value=True)

    def capture(summary):
        seen["summary"] = summary
        return True

    c._confirm = capture
    c.create_task("PROJ-1", "Add field", "desc", "AC: field saves")
    assert "PROJ-1" in seen["summary"]
    assert "AC: field saves" in seen["summary"]
