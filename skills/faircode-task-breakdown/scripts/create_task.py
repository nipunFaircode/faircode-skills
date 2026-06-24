#!/usr/bin/env python3
"""Create a Task in erp.faircode.co and print its name.

Usage (non-interactive, after user confirms payload in Claude):
  python3 create_task.py \
    --project "PROJ-001" \
    --subject "Add credit-limit check on Sales Order" \
    --description "Context line..." \
    --ac "- Given SO is saved\n- When credit limit is exceeded\n- Then a validation error is raised" \
    --custom-app "my_app" \
    --estimate 2.0 \
    --yes

Omit --yes for interactive terminal use (prompts before writing).

Token: FAIRCODE_ERP_TOKEN env var (format api_key:api_secret).
URL:   FAIRCODE_ERP_URL env var (default https://erp.faircode.co).
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta


BASE_URL = (os.environ.get("FAIRCODE_ERP_URL") or "https://erp.faircode.co").rstrip("/")
TOKEN = os.environ.get("FAIRCODE_ERP_TOKEN")


def _ping():
    """Return the HTTP status code from a lightweight auth check."""
    url = f"{BASE_URL}/api/method/frappe.auth.get_logged_user"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        print(f"Network error during token check: {e.reason}", file=sys.stderr)
        return 0


def _post(doctype, doc):
    url = f"{BASE_URL}/api/resource/{urllib.parse.quote(doctype)}"
    data = json.dumps(doc).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())["data"]
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            payload = json.loads(body)
            msgs = json.loads(payload.get("_server_messages", "[]"))
            for m in msgs:
                try:
                    print("ERP ERROR:", json.loads(m).get("message", m), file=sys.stderr)
                except Exception:
                    print("ERP ERROR:", m, file=sys.stderr)
            if not msgs:
                print(f"HTTP {e.code}: {body[:500]}", file=sys.stderr)
        except Exception:
            print(f"HTTP {e.code}: {body[:500]}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    if not TOKEN:
        print("ERROR: FAIRCODE_ERP_TOKEN is not set.", file=sys.stderr)
        print("  Set it with:  export FAIRCODE_ERP_TOKEN=<api_key>:<api_secret>", file=sys.stderr)
        sys.exit(1)

    today = date.today().isoformat()
    default_end = (date.today() + timedelta(days=7)).isoformat()

    parser = argparse.ArgumentParser(description="Create a Task in ERPNext")
    parser.add_argument("--project", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--ac", required=True, help="Acceptance criteria (one item per line, prefixed with -)")
    parser.add_argument("--custom-app", required=True, dest="custom_app")
    parser.add_argument("--estimate", type=float, default=1.0, help="Estimated hours")
    parser.add_argument("--type", default="Task", help="Task type (default: Task)")
    parser.add_argument("--start-date", default=today, dest="start_date", help="exp_start_date (YYYY-MM-DD, default: today)")
    parser.add_argument("--end-date", default=default_end, dest="end_date", help="exp_end_date (YYYY-MM-DD, default: today+7)")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip interactive confirmation (use after reviewing payload in Claude)")
    parser.add_argument("--dry-run", action="store_true", help="Print the JSON payload without calling the API")
    args = parser.parse_args()

    if not args.dry_run:
        status = _ping()
        if status != 200:
            print(f"ERROR: Token rejected by ERP (HTTP {status}). Regenerate FAIRCODE_ERP_TOKEN before continuing.", file=sys.stderr)
            sys.exit(1)

    description = (
        f"{args.description}\n\n"
        f"## Acceptance Criteria\n{args.ac}\n\n"
        f"## Dev Environment\nCustom App: `{args.custom_app}`"
    )

    if not args.yes:
        summary = (
            f"\n--- Task to be created ---\n"
            f"Project    : {args.project}\n"
            f"Subject    : {args.subject}\n"
            f"Start/End  : {args.start_date} to {args.end_date} ({args.estimate}h)\n"
            f"Description: {description}\n"
            f"--------------------------\n"
            f"Create this task in erp.faircode.co? [y/N] "
        )
        answer = input(summary).strip().lower()
        if answer != "y":
            print("Aborted - nothing written.")
            sys.exit(0)

    doc = {
        "project": args.project,
        "subject": args.subject,
        "description": description,
        "expected_time": args.estimate,
        "exp_start_date": args.start_date,
        "exp_end_date": args.end_date,
        "type": args.type,
    }

    if args.dry_run:
        print(json.dumps(doc, indent=2))
        sys.exit(0)

    result = _post("Task", doc)
    print(f"Created: {result['name']}")


if __name__ == "__main__":
    main()
