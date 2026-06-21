# Frappe Methods — the Faircode way

Do it the framework's way. Never paste raw SQL or hand-rolled HTTP where a
framework method exists.

## Data access
- Read one: `frappe.get_doc(doctype, name)`. Read many: `frappe.get_all(doctype, filters=..., fields=...)`.
- Query builder for complex reads: `frappe.qb`. Raw `frappe.db.sql` only with a written reason in the PR.
- Single values: `frappe.db.get_value` / `set_value`. Never `UPDATE` by hand.

## Documents & lifecycle
- Create: `doc = frappe.new_doc(dt); doc.update({...}); doc.insert()`.
- Modify in controller hooks: `validate`, `before_save`, `on_submit`, `on_cancel` — declared in `hooks.py`, not monkey-patched.
- Never bypass permissions with `ignore_permissions=True` unless justified in the PR.

## APIs
- Expose with `@frappe.whitelist()`. Validate inputs. Return plain dicts/lists.

## Background work
- Long jobs: `frappe.enqueue`. Scheduled: `scheduler_events` in `hooks.py`.

## Anti-patterns (reject in review)
- Copy-pasted code from chat with no understanding of what it does.
- Re-implementing framework features (caching, permissions, naming series).
- Over-engineering: new abstraction layers for a one-off requirement (YAGNI).
