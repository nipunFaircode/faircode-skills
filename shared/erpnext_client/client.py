"""Read + safe-write ERPNext client for Faircode skills.

Token from FAIRCODE_ERP_TOKEN env var (format "<api-key>:<api-secret>").
Base URL from FAIRCODE_ERP_URL (default https://erp.faircode.co).
Stdlib only.
"""
import json
import os
import urllib.parse
import urllib.request

DEFAULT_URL = "https://erp.faircode.co"


class ERPNextClient:
    def __init__(self, base_url=None, token=None):
        self.base_url = (base_url or os.environ.get("FAIRCODE_ERP_URL") or DEFAULT_URL).rstrip("/")
        self.token = token or os.environ.get("FAIRCODE_ERP_TOKEN")
        if not self.token:
            raise RuntimeError("FAIRCODE_ERP_TOKEN not set")
        self._opener = lambda req, timeout=60: urllib.request.urlopen(req, timeout=timeout)

    def _request(self, method, path, params=None, body=None):
        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"token {self.token}")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        with self._opener(req, timeout=60) as r:
            return json.loads(r.read().decode())

    def get_list(self, doctype, fields, filters=None, order_by=None):
        out, start = [], 0
        while True:
            params = {
                "doctype": doctype,
                "fields": json.dumps(fields),
                "limit_start": start,
                "limit_page_length": 500,
            }
            if filters:
                params["filters"] = json.dumps(filters)
            if order_by:
                params["order_by"] = order_by
            batch = self._request("GET", "/api/method/frappe.client.get_list", params=params)["message"]
            out.extend(batch)
            if len(batch) < 500:
                break
            start += 500
        return out

    def _confirm(self, summary):
        print(summary)
        return input("Proceed with this write to ERPNext? [y/N] ").strip().lower() == "y"

    def _safe_post(self, doctype, doc, summary):
        if not self._confirm(summary):
            print("Aborted — nothing written.")
            return None
        return self._request("POST", f"/api/resource/{urllib.parse.quote(doctype)}", body=doc)["data"]

    def create_task(self, project, subject, description, acceptance_criteria):
        full_desc = f"{description}\n\n## Acceptance Criteria\n{acceptance_criteria}"
        doc = {"project": project, "subject": subject, "description": full_desc}
        summary = f"CREATE Task in {project}: {subject!r}\n{full_desc}"
        return self._safe_post("Task", doc, summary)

    def add_comment(self, doctype, name, text):
        doc = {"reference_doctype": doctype, "reference_name": name,
               "content": text, "comment_type": "Comment"}
        summary = f"COMMENT on {doctype} {name}: {text!r}"
        return self._safe_post("Comment", doc, summary)

    def file_bug(self, project, subject, body):
        doc = {"project": project, "subject": subject, "description": body}
        summary = f"CREATE Issue in {project}: {subject!r}\n{body}"
        return self._safe_post("Issue", doc, summary)
