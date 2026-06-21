import json
import pytest
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


def make_client(pages):
    calls = []

    def opener(req, timeout=60):
        calls.append(req.full_url)
        return FakeResp(pages.pop(0))

    c = ERPNextClient(base_url="https://erp.test", token="k:s")
    c._opener = opener
    c._calls = calls
    return c


def test_requires_token(monkeypatch):
    monkeypatch.delenv("FAIRCODE_ERP_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        ERPNextClient(base_url="https://erp.test")


def test_get_list_paginates():
    page1 = {"message": [{"name": f"T{i}"} for i in range(500)]}
    page2 = {"message": [{"name": "T500"}]}
    c = make_client([page1, page2])
    rows = c.get_list("Task", ["name"])
    assert len(rows) == 501
    assert len(c._calls) == 2
    assert "Authorization" not in c._calls[0]  # token is a header, not in URL
