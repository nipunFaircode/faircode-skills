---
name: frappe-impl-payment
description: >-
  Use when integrating a payment gateway or setting up payment flows in a Frappe
  app. Triggers on "Razorpay", "payment gateway", "payment request", "online
  payment", "payment webhook", "UPI payment link", "Stripe", "payment
  reconciliation". Covers Payment Request, Razorpay integration, webhook
  handling, and reconciliation.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
---

# Frappe Payment Gateway Integration

Two payment scenarios:
- **Manual (B2B):** accounts team creates Payment Entry after bank transfer.
- **Online (B2C/portal):** Payment Request sent to customer → customer pays via gateway → webhook confirms.

This skill covers online payment gateway integration. For manual payment entry,
see `erpnext-selling`.

## Prerequisites
- Frappe `payments` app installed: `bench get-app payments && bench --site sitename install-app payments`.
- Payment Gateway Account record created (Setup → Payment Gateway Account).
- A clearing/gateway account in CoA to hold payments before reconciliation.

## Payment Gateway Account setup (Razorpay example)

Setup → Payment Gateway Account:
- Payment Gateway: Razorpay
- Payment Account: e.g., "Razorpay Clearing - Company" (bank/gateway clearing account)
- Currency: INR
- API Key, API Secret: from Razorpay Dashboard → Settings → API Keys

## Payment Request flow

```python
# Create a Payment Request linked to a Sales Invoice
def create_payment_request(invoice_name):
    invoice = frappe.get_doc("Sales Invoice", invoice_name)
    pr = frappe.get_doc({
        "doctype": "Payment Request",
        "payment_request_type": "Inward",
        "party_type": "Customer",
        "party": invoice.customer,
        "reference_doctype": "Sales Invoice",
        "reference_name": invoice.name,
        "grand_total": invoice.outstanding_amount,
        "currency": invoice.currency,
        "payment_gateway_account": "Razorpay",
        "email_to": invoice.contact_email,
        "subject": f"Payment Request for {invoice.name}",
    })
    pr.insert(ignore_permissions=True)
    pr.submit()
    return pr.payment_url  # share this link with the customer
```

The payment URL opens a Razorpay checkout page. On payment:
1. Razorpay calls your webhook.
2. Webhook handler verifies signature, marks Payment Request as paid,
   creates Payment Entry.

## Webhook handler

```python
# In myapp/api.py - registered in hooks.py as a whitelisted endpoint
@frappe.whitelist(allow_guest=True)
def razorpay_webhook():
    import hmac, hashlib, json

    data = frappe.request.get_json()
    if not data:
        frappe.throw("Empty payload", frappe.ValidationError)

    # ALWAYS verify signature before processing
    secret = frappe.db.get_single_value("Razorpay Settings", "webhook_secret")
    if not secret:
        frappe.throw("Webhook secret not configured")

    signature = frappe.get_request_header("X-Razorpay-Signature")
    expected = hmac.new(
        secret.encode("utf-8"),
        frappe.request.data,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature or ""):
        frappe.throw("Invalid signature", frappe.PermissionError)

    event = data.get("event")
    if event == "payment.captured":
        payment_id = data["payload"]["payment"]["entity"]["id"]
        order_id = data["payload"]["payment"]["entity"]["order_id"]

        # Idempotency check - don't process the same payment twice
        if frappe.db.exists("Payment Entry", {"reference_no": payment_id}):
            return {"status": "already processed"}

        # Find the Payment Request linked to this order
        pr_name = frappe.db.get_value(
            "Payment Request",
            {"name": order_id},  # Razorpay order ID stored as PR name
            "name"
        )
        if pr_name:
            pr = frappe.get_doc("Payment Request", pr_name)
            pr.run_method("on_payment_authorized", "Completed")

    return {"status": "ok"}
```

Register webhook in Razorpay Dashboard:
- URL: `https://yoursite.com/api/method/myapp.api.razorpay_webhook`
- Events: `payment.captured`, `payment.failed`
- Secret: set the same secret in your Razorpay Settings DocType

## Payment Reconciliation (manual)

When advance payments exist and need to be matched to invoices:
Accounts → Payment Reconciliation:
1. Select Party Type (Customer) and Party.
2. Click "Get Unreconciled Entries" - shows Payment Entries and outstanding invoices.
3. Select entries to match.
4. Click "Reconcile".

Run this after every batch of advance payments. Unreconciled advances inflate
the receivables report.

## Anti-patterns

| Do NOT | Do Instead |
| --- | --- |
| Trust webhook payload without signature verification | Always verify HMAC signature before any processing |
| Create Payment Entry without idempotency check | Check if Payment Entry for this transaction ID already exists |
| Call `frappe.db.commit()` in webhook handler | Let Frappe manage the transaction |
| Store gateway credentials in code | Store in a Settings DocType, never in code or version control |
| Process webhook synchronously for slow operations | Enqueue with `frappe.enqueue()` if processing takes > 1 second |

## Definition of Done
- Payment Gateway Account created and linked to the correct clearing account.
- Payment Request generates a working payment link.
- Webhook endpoint registered in the gateway dashboard.
- Webhook signature verification passing in staging.
- Payment Entry created and linked to the invoice after a test payment.
- Duplicate webhook delivery handled (idempotency check passes).
- Payment Reconciliation demonstrated to the client's accounts team.

## Related Skills
`frappe-impl-whitelisted`, `frappe-core-api`, `frappe-impl-website`, `erpnext-selling`
