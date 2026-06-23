---
name: frappe-impl-ai-integration
description: >-
  Use when wiring AI features into ERPNext workflows at the framework level.
  Triggers on "where to add AI in Frappe", "AI in controller", "AI button on
  form", "AI scheduler job", "AI webhook trigger", "AI audit log". Covers the
  four integration patterns and how to choose between them.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
---

# Frappe AI Integration Patterns

This skill covers WHERE and HOW to wire AI into Frappe's architecture.
For the API call itself (model selection, prompt caching, cost control),
see `faircode-ai-copilot`.

There is no built-in AI layer in vanilla ERPNext - everything is custom code.

## Pattern selection

```
Who triggers the AI call?
│
├── User explicitly requests it (button click)
│   └── Pattern 1: On-demand via custom button
│
├── Document save/submit automatically triggers it
│   └── Pattern 2: Controller hook → enqueue
│
├── Batch of documents needs processing overnight
│   └── Pattern 3: Scheduled batch job
│
└── Incoming external event (new email, webhook)
    └── Pattern 4: Webhook-triggered
```

## Pattern 1: On-demand via custom button

Best for: user-initiated tasks where the result is shown immediately (draft reply,
summarise document, classify a field value).

**Client Script:**
```javascript
frappe.ui.form.on("Issue", {
    refresh(frm) {
        frm.add_custom_button("Draft Reply with AI", () => {
            frappe.show_alert({ message: "Drafting...", indicator: "blue" });
            frappe.call({
                method: "myapp.ai.draft_reply",
                args: { issue_name: frm.doc.name },
                callback(r) {
                    if (r.message) {
                        frm.set_value("ai_draft_reply", r.message);
                        frappe.show_alert({ message: "Draft ready", indicator: "green" });
                    }
                }
            });
        }, "AI");
    }
});
```

**Whitelisted method:**
```python
@frappe.whitelist()
def draft_reply(issue_name: str) -> str:
    # For short tasks (< 10 seconds): call synchronously
    issue = frappe.get_doc("Issue", issue_name)
    # ... call Claude API ...
    return draft_text
```

For tasks that may take > 5 seconds: enqueue instead and use
`frappe.publish_realtime` to notify the user when done (see Pattern 2).

## Pattern 2: Controller hook → enqueue

Best for: automatic enrichment on save/submit (classify a lead on creation,
extract line items from an uploaded file after insert).

**Rule: never call the AI API synchronously in a hook.** Always enqueue.

```python
# In the controller
class Lead(Document):
    def after_insert(self):
        # Enqueue - do not call AI API directly here
        frappe.enqueue(
            "myapp.ai.classify_lead_industry",
            lead_name=self.name,
            queue="default",
            timeout=120,
            enqueue_after_commit=True  # ensures the doc is committed before the job runs
        )

# In myapp/ai.py
def classify_lead_industry(lead_name: str, **kwargs):
    lead = frappe.get_doc("Lead", lead_name)
    # ... call Claude API ...
    industry = response.content[0].text.strip()
    frappe.db.set_value("Lead", lead_name, "industry", industry)
    frappe.publish_realtime(
        event="lead_enriched",
        message={"lead": lead_name},
        user=lead.lead_owner or "Administrator"
    )
```

Use `enqueue_after_commit=True` for `after_insert` - without it, the job may
run before the document is committed and find nothing.

## Pattern 3: Scheduled batch job

Best for: overnight enrichment of a backlog, periodic re-classification,
generating weekly AI reports.

```python
# In hooks.py
scheduler_events = {
    "daily": [
        "myapp.ai.nightly_lead_enrichment"
    ]
}

# In myapp/ai.py
def nightly_lead_enrichment():
    # Get leads that need enrichment (no industry set, created in last 7 days)
    leads = frappe.get_all(
        "Lead",
        filters={
            "industry": ["is", "not set"],
            "creation": [">", frappe.utils.add_days(frappe.utils.today(), -7)]
        },
        pluck="name",
        limit=100  # process max 100 per run to control API costs
    )

    total = len(leads)
    for i, lead_name in enumerate(leads, 1):
        try:
            classify_lead_industry(lead_name)
            frappe.publish_progress(
                percent=round((i / total) * 100),
                title="AI Lead Enrichment",
                description=f"{i} of {total}"
            )
        except Exception:
            frappe.log_error(frappe.get_traceback(), f"AI enrichment failed: {lead_name}")
            continue  # don't abort the whole batch for one failure

    frappe.db.commit()
```

## Pattern 4: Webhook-triggered

Best for: incoming email → auto-classify and route, incoming form submission →
AI-generated acknowledgement.

```python
# Registered as a whitelisted endpoint in hooks.py
# hooks.py: override_whitelisted_methods = {"myapp.api.incoming_email_webhook": "myapp.api.incoming_email_webhook"}

@frappe.whitelist(allow_guest=True)
def incoming_email_webhook():
    # Verify the webhook signature first (see frappe-impl-payment for pattern)
    data = frappe.request.get_json()
    subject = data.get("subject", "")
    body = data.get("body", "")

    # Enqueue AI classification - don't do it in the webhook handler itself
    frappe.enqueue(
        "myapp.ai.classify_and_route_email",
        subject=subject,
        body=body,
        queue="short",
        timeout=60
    )
    return {"status": "queued"}

def classify_and_route_email(subject: str, body: str, **kwargs):
    # Call Claude to classify
    category = call_claude_classification(subject, body)
    # Create an Issue and assign based on category
    issue = frappe.get_doc({
        "doctype": "Issue",
        "subject": subject,
        "description": body,
        "issue_type": category,
    })
    issue.insert(ignore_permissions=True)
```

## AI Audit Log DocType

Create this DocType to log every AI call across all patterns:

Fields: reference_doctype (Link to DocType), reference_name (Dynamic Link),
model (Data), task (Data), input_tokens (Int), output_tokens (Int),
triggered_by (Link to User), timestamp (Datetime), status (Select: Success/Error),
error_message (Small Text).

```python
def log_ai_call(doctype, docname, model, task, input_tokens, output_tokens, error=None):
    frappe.get_doc({
        "doctype": "AI Audit Log",
        "reference_doctype": doctype,
        "reference_name": docname,
        "model": model,
        "task": task,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "triggered_by": frappe.session.user,
        "timestamp": frappe.utils.now_datetime(),
        "status": "Error" if error else "Success",
        "error_message": str(error) if error else None,
    }).insert(ignore_permissions=True)
```

Call this at the end of every AI function regardless of pattern.

## Anti-patterns

| Do NOT | Do Instead |
| --- | --- |
| Call AI API in `validate` or `on_update` directly | Always use `frappe.enqueue` - hooks are synchronous |
| Show raw AI output to the user without review | Show in a field or dialog; let the user confirm before saving |
| Run batch jobs without a per-item try/except | One failure should not abort the whole batch |
| Skip the Audit Log because "it's just internal" | Log everything - you will need this for cost attribution and debugging |

## Definition of Done
- Pattern chosen based on trigger type (user/hook/schedule/webhook).
- AI calls are always enqueued, never synchronous in hooks.
- `frappe.publish_realtime` notifies user on completion.
- AI Audit Log DocType created and every call is logged.
- Error handling: individual failures log and continue; don't abort batch.
- `max_tokens` set on all API calls; prompt caching on repeated system prompts.

## Related Skills
`faircode-ai-copilot`, `frappe-impl-scheduler`, `frappe-impl-whitelisted`,
`frappe-core-realtime`, `frappe-impl-hooks`
