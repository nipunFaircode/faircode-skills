---
name: frappe-core-realtime
description: >-
  Use when publishing real-time events from the server or listening for them on
  the client. Triggers on "real-time", "socket.io", "publish_realtime", "live
  update", "background job progress", "realtime notification", "push update to
  browser". Covers server publish, client listeners, room scoping, progress
  bars, and cleanup.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
---

# Frappe Real-time Events

Frappe uses Socket.io (via Node) for real-time events. Python publishes;
JavaScript listens. Always scope events to a user or room - unscoped events
go to all connected users.

## Server → Client (Python)

```python
# Send to a specific user only
frappe.publish_realtime(
    event="invoice_approved",
    message={"invoice": doc.name, "status": "Approved"},
    user=frappe.session.user
)

# Send to all users currently viewing a specific document
frappe.publish_realtime(
    event="doc_status_change",
    message={"status": doc.status},
    doctype=doc.doctype,
    docname=doc.name
)

# Send to all users on a DocType's list view
frappe.publish_realtime(
    event="list_update",
    message={"doctype": doc.doctype},
    room=f"list:{doc.doctype}"
)

# Background job progress bar (shows in Frappe desk automatically)
frappe.publish_progress(
    percent=round((i / total) * 100),
    title="Processing Invoices",
    description=f"{i} of {total} done"
)
```

## Room scoping reference

| `user=` | `doctype=` + `docname=` | `room=` | Who receives |
| --- | --- | --- | --- |
| Set | - | - | Only that one user |
| Not set | Both set | - | All users viewing that document |
| Not set | - | `"list:Doctype"` | All users on that list view |
| Not set | - | Not set | **All** connected users - avoid this |

## Client → listener (JavaScript)

```javascript
// Listen for a custom event
frappe.realtime.on("invoice_approved", (data) => {
    frappe.show_alert({
        message: `Invoice ${data.invoice} has been ${data.status}`,
        indicator: "green"
    });
});

// Remove listener (always do this on cleanup)
frappe.realtime.off("invoice_approved");
```

## In a form script (with auto-cleanup)

```javascript
frappe.ui.form.on("Sales Invoice", {
    onload(frm) {
        // Listen for updates to this specific document
        frappe.realtime.on("invoice_approved", (data) => {
            if (data.invoice === frm.doc.name) {
                frm.reload_doc();
                frappe.show_alert({ message: "Invoice approved!", indicator: "green" });
            }
        });
    },

    before_unload(frm) {
        // Remove listener when form is closed
        frappe.realtime.off("invoice_approved");
    }
});
```

## Background job with progress

```python
# In a whitelisted method that triggers a long-running job
@frappe.whitelist()
def process_bulk_invoices(invoices):
    frappe.enqueue(
        "myapp.api._process_bulk_invoices",
        invoices=invoices,
        queue="long",
        timeout=600
    )

def _process_bulk_invoices(invoices, **kwargs):
    invoice_list = frappe.parse_json(invoices)
    total = len(invoice_list)
    for i, name in enumerate(invoice_list, 1):
        # ... process the invoice ...
        frappe.publish_progress(
            percent=round((i / total) * 100),
            title="Processing Invoices",
            description=f"Invoice {name} - {i} of {total}"
        )
    frappe.publish_realtime(
        event="bulk_processing_done",
        message={"total": total},
        user=frappe.session.user
    )
```

## Built-in Frappe events you can listen to

| Event | When it fires |
| --- | --- |
| `"msgprint"` | Server calls `frappe.msgprint()` |
| `"progress"` | `frappe.publish_progress()` called |
| `"list_update"` | A document in a list changed (after save) |
| `"doc_update"` | A specific document changed |
| `"logout"` | User session ended |

## Anti-patterns

| Do NOT | Do Instead |
| --- | --- |
| Publish without `user=` or `room=` | Always scope - unscoped goes to all connected users |
| Send full document data in payload | Send only the `name` or key; let client call `frm.reload_doc()` |
| `frappe.realtime.on()` without a matching `off()` | Remove listeners in `before_unload` or teardown |
| Call `frappe.publish_realtime()` in `validate` | Call in `on_update` - validate may run without committing |
| Poll with `setInterval` for updates | Use `frappe.realtime.on()` instead - no polling needed |

## Definition of Done
- Server publishes event scoped to correct user or room.
- Client listener registered and fires on receipt.
- Listener removed in teardown (`before_unload` or equivalent).
- Tested in two simultaneous browser sessions to confirm correct scoping
  (only the intended user sees the event).

## Related Skills
`frappe-impl-ui-components`, `frappe-impl-scheduler`, `frappe-core-notifications`
