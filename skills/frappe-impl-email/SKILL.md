---
name: frappe-impl-email
description: >-
  Use when configuring email sending or receiving in a Frappe app. Triggers on
  "email setup", "SMTP", "outgoing email", "incoming email", "IMAP",
  "frappe.sendmail", "email template", "email queue", "notification DocType",
  "email not sending". Covers outgoing/incoming accounts, frappe.sendmail(),
  Email Template, Notification DocType, and troubleshooting the queue.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
---

# Frappe Email - Outgoing and Incoming

Email is infrastructure. Get it wrong and customers don't receive invoices,
support tickets don't get created, and notifications silently fail.

## Outgoing Email Account

Setup → Email Account → New.

| Field | Notes |
| --- | --- |
| Email Address | The from address (e.g., erp@company.com) |
| Password | SMTP password or App Password (for Gmail) |
| SMTP Server | See table below |
| Port | 587 (STARTTLS) or 465 (SSL) |
| Use TLS | Yes for port 587 |
| Use SSL | Yes for port 465 |
| Enable Outgoing | Yes |
| Default Outgoing | Yes - only one account should be default |

SMTP servers:

| Provider | Server | Port | Auth |
| --- | --- | --- | --- |
| Gmail | smtp.gmail.com | 587 | App Password (2FA required) or OAuth2 |
| SendGrid | smtp.sendgrid.net | 587 | User: `apikey`, Password: API key |
| AWS SES (Mumbai) | email-smtp.ap-south-1.amazonaws.com | 587 | IAM SMTP credentials |
| Custom/cPanel | mail.yourdomain.com | 587 | Email password |

**Gmail:** must use an App Password (not your Google account password).
Enable 2FA on the Google account first, then generate an App Password at
myaccount.google.com → Security → App Passwords.

**AWS SES:** verify domain in SES console first. If the account is in sandbox
mode, only verified email addresses can receive. Request production access
before go-live.

Test the outgoing account:
```bash
bench execute frappe.core.doctype.email_account.email_account.send_test_email \
  --args '{"email_account": "erp@company.com", "to": "test@example.com"}'
```

## frappe.sendmail() API

```python
frappe.sendmail(
    recipients=["customer@example.com"],
    cc=["accounts@company.com"],
    reply_to="support@company.com",
    subject=f"Invoice {doc.name} from {doc.company}",
    message=frappe.render_template(
        "myapp/templates/emails/invoice_notification.html",
        {"doc": doc, "link": frappe.utils.get_url_to_form(doc.doctype, doc.name)}
    ),
    attachments=[{
        "fname": f"{doc.name}.pdf",
        "fcontent": frappe.get_print(doc.doctype, doc.name, print_format="Tax Invoice", as_pdf=True)
    }],
    reference_doctype=doc.doctype,
    reference_name=doc.name,  # links the email to the document timeline
    delayed=True,              # True = add to Email Queue (recommended in hooks)
)
```

**Use `delayed=True` in all document hooks.** Synchronous email (`delayed=False`)
in `validate` or `on_update` blocks the save and can cause timeouts.

## Email Template (no-code)

Setup → Email Template. Jinja subject and response body. Reference in Notification
or call from code:

```python
template = frappe.get_doc("Email Template", "Invoice Sent")
subject = frappe.render_template(template.subject, {"doc": doc})
message = frappe.render_template(template.response, {"doc": doc})
frappe.sendmail(recipients=[doc.contact_email], subject=subject, message=message,
                reference_doctype=doc.doctype, reference_name=doc.name, delayed=True)
```

## Notification DocType (no-code automation)

Setup → Notification. Fires automatically on document events.

| Field | Setting |
| --- | --- |
| Document Type | e.g., Sales Invoice |
| Event | after_insert / after_save / Days Before or After (date field) |
| Condition | Jinja, e.g. `doc.docstatus == 1 and doc.outstanding_amount > 0` |
| Recipients | From field (e.g., `doc.contact_email`) or fixed addresses |
| Email Template | Select an Email Template |

Notifications run asynchronously via the scheduler. They don't block form saves.

## Incoming Email (IMAP for Support)

Setup → Email Account → New. Enable Incoming: Yes.
Set IMAP server (e.g., imap.gmail.com, port 993, SSL).
Link to DocType: Support Issue (auto-creates a new Issue on incoming email).
Set Filters to prevent spam from auto-creating issues.

The scheduler polls the IMAP mailbox every 5 minutes. Not real-time.
For real-time email processing, use a webhook from the email provider.

## Troubleshooting the Email Queue

Setup → Email Queue (or search "Email Queue" in desk).

| Status | Meaning | Fix |
| --- | --- | --- |
| Not Sent | In queue, not yet attempted | Wait for scheduler or run `bench execute frappe.email.queue.flush` |
| Sending | Currently being sent | If stuck > 10 min, scheduler may be down - check `bench doctor` |
| Sent | Delivered to SMTP | Check spam folder if recipient didn't receive |
| Error | SMTP rejected | Open the record, read the Error Log field for the exact SMTP error |

Common SMTP errors:

| Error | Fix |
| --- | --- |
| `535 Authentication failed` | Wrong password or App Password not set for Gmail |
| `550 Relaying denied` | Your IP is not authorised to send via this SMTP; check SPF/DKIM |
| `421 Too many connections` | Rate limiting; reduce sending frequency or upgrade SMTP plan |
| `Message size exceeds limit` | Attachment too large; reduce PDF size or use a link instead |

Force retry stuck emails:
```bash
bench execute frappe.email.queue.flush
```

## Anti-patterns

| Do NOT | Do Instead |
| --- | --- |
| `delayed=False` in document hooks | `delayed=True` - synchronous email blocks saves |
| Hardcode email addresses in code | Fetch from a Settings DocType or System Settings |
| Send without `reference_doctype` / `reference_name` | Always link - email appears in document timeline |
| Use email for real-time alerts | Use `frappe.publish_realtime` for desk notifications (`frappe-core-realtime`) |

## Definition of Done
- Outgoing account configured and test email received.
- `frappe.sendmail()` used in at least one hook with `delayed=True`.
- Email visible in document timeline (reference_doctype set).
- Email Queue checked - no stuck or errored emails.
- Incoming email (IMAP) configured and tested if support module is in scope.

## Related Skills
`frappe-core-notifications`, `frappe-impl-hooks`, `frappe-core-realtime`
