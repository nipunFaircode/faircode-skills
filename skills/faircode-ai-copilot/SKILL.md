---
name: faircode-ai-copilot
description: >-
  Use when building AI-powered features inside a Frappe/ERPNext custom app
  using the Claude API (Anthropic). Triggers on "add AI to ERPNext", "Claude
  API in Frappe", "AI feature", "summarise with AI", "draft email with AI",
  "classify with AI". Covers API setup, prompt caching, cost control, async
  patterns, and data handling rules for client deployments.
---

# Faircode AI Copilot - Claude API in Frappe

This skill is for building AI features FOR clients in their ERPNext deployment.
It is not about using Claude Code internally.

Before building: confirm with the client that they accept data being sent to
Anthropic's API, and that their privacy policy covers this. Do not proceed
without explicit client sign-off.

## Setup

Add to your app's `requirements.txt`:
```
anthropic>=0.34.0
```

Install: `bench setup requirements` (or `pip install anthropic` in the bench env).

## API key storage

Never hardcode the API key. Store in a custom Settings DocType:

```python
# myapp/myapp/doctype/ai_settings/ai_settings.py
# Fields: api_key (Password fieldtype), model (Select), max_tokens (Int)

def get_api_key():
    key = frappe.db.get_single_value("AI Settings", "api_key")
    if not key:
        frappe.throw("Anthropic API key not configured in AI Settings")
    return key
```

The Password fieldtype encrypts the value at rest. Never store in site_config.json
or any version-controlled file.

## Basic API call (synchronous - for short tasks only)

```python
import anthropic
import frappe

@frappe.whitelist()
def summarise_support_issue(issue_name: str) -> str:
    issue = frappe.get_doc("Issue", issue_name)
    client = anthropic.Anthropic(api_key=get_api_key())

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system="You are a support assistant. Summarise the issue in 2-3 sentences.",
        messages=[{
            "role": "user",
            "content": f"Issue: {issue.subject}\n\n{issue.description}"
        }]
    )
    return response.content[0].text
```

Call from client script:
```javascript
frappe.call({
    method: "myapp.api.summarise_support_issue",
    args: { issue_name: frm.doc.name },
    callback(r) {
        frm.set_value("ai_summary", r.message);
    }
});
```

## Prompt caching (use for repeated system prompts)

Prompt caching reduces cost by ~90% on repeated calls with the same system prompt.
Use it whenever the system prompt is long (> 1024 tokens) and reused across calls.

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,  # your detailed instructions
            "cache_control": {"type": "ephemeral"}  # cache this block
        }
    ],
    messages=[{"role": "user", "content": user_input}]
)
```

The cache TTL is 5 minutes. Cache hits are charged at ~10% of the normal input
token rate. Always add `cache_control` to system prompts > 1024 tokens.

## Async pattern (use for long tasks and batch processing)

Never call the AI API synchronously in `validate`, `on_update`, or any
document hook - it blocks the save and can time out.

```python
# Trigger from a whitelisted method or a client-side button
@frappe.whitelist()
def enqueue_ai_classification(lead_name: str):
    frappe.enqueue(
        "myapp.ai.classify_lead",
        lead_name=lead_name,
        queue="default",
        timeout=120
    )

# The actual AI call runs in a background worker
def classify_lead(lead_name: str, **kwargs):
    lead = frappe.get_doc("Lead", lead_name)
    client = anthropic.Anthropic(api_key=get_api_key())

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # use Haiku for fast, cheap classification
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"Classify this company into one of: Manufacturing, Retail, Services, Healthcare, Other.\nCompany: {lead.company_name}\nDescription: {lead.notes}"
        }]
    )

    industry = response.content[0].text.strip()
    frappe.db.set_value("Lead", lead_name, "industry", industry)

    # Notify the user who triggered it
    frappe.publish_realtime(
        event="lead_classified",
        message={"lead": lead_name, "industry": industry},
        user=frappe.session.user
    )
```

## Cost control

```python
# Log every API call - essential for cost visibility
def log_ai_call(doctype, docname, model, input_tokens, output_tokens, task):
    frappe.get_doc({
        "doctype": "AI Usage Log",  # create this DocType
        "reference_doctype": doctype,
        "reference_name": docname,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "task": task,
        "user": frappe.session.user,
        "timestamp": frappe.utils.now()
    }).insert(ignore_permissions=True)

# After every API call:
log_ai_call(
    doc.doctype, doc.name,
    response.model,
    response.usage.input_tokens,
    response.usage.output_tokens,
    "summarise_issue"
)
```

Always set `max_tokens` - no ceiling means runaway costs on unexpected inputs.

## Model selection guide

| Task | Model | Reason |
| --- | --- | --- |
| Classification, short extraction | claude-haiku-4-5-20251001 | Fastest, cheapest |
| Drafting emails, summaries | claude-sonnet-4-6 | Best quality/cost balance |
| Complex reasoning, long documents | claude-opus-4-7 | Highest capability, highest cost |

## Data handling rules (non-negotiable)

- Never send customer PII (name, phone, email, Aadhaar, PAN) to the API without
  client consent and a confirmed privacy policy update.
- Anonymise or pseudonymise where possible (e.g., replace customer name with
  "Customer X" in the prompt).
- Log all AI calls (inputs token count, output token count, model, timestamp,
  triggered by whom) in an AI Usage Log DocType.
- Do not use AI output as a final decision without human review for: financial
  approvals, compliance classification, credit decisions.

## STOP - red flags

| Thought | Reality |
| --- | --- |
| "I'll store the API key in site_config.json" | Version-controlled or backup-exposed. Use a Settings DocType with Password fieldtype. |
| "Call the API in the validate hook" | Blocks the save; can cause timeouts and partial saves. Use frappe.enqueue. |
| "No need to log token usage" | Without logs you can't split costs per client or detect runaway usage. |
| "Send the full customer record to Claude" | Strip PII first. Only send what is necessary for the task. |

## Definition of Done
- API key stored in a custom Settings DocType (Password fieldtype).
- AI calls run via `frappe.enqueue` (not synchronously in hooks).
- `max_tokens` set on every API call.
- Prompt caching enabled on system prompts > 1024 tokens.
- AI Usage Log DocType created and every call is logged.
- Client privacy policy sign-off documented before go-live.

## Related Skills
`frappe-impl-ai-integration`, `frappe-impl-whitelisted`, `frappe-core-realtime`,
`frappe-impl-scheduler`
