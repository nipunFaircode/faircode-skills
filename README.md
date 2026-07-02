# Faircode Frappe

Claude plugin: a delivery-lifecycle skill suite for Faircode's ERPNext/Frappe
implementation & customisation team.

## Install (team)

```bash
/plugin marketplace add https://github.com/nipunFaircode/faircode-frappe
/plugin install faircode
```

Once installed, start with `/faircode-help` or `/faircode-delivery` to route
to the right skill for your current project phase.

## Configure ERPNext access

```bash
export FAIRCODE_ERP_URL="https://erp.faircode.co"
export FAIRCODE_ERP_TOKEN="<api-key>:<api-secret>"   # never commit this
```

## Layout

- `skills/faircode-*/SKILL.md` — the skills
- `shared/erpnext_client/` — read + safe-write ERPNext helper
- `shared/references/` — shared rules cited by skills

See `docs/superpowers/specs/` for the design and `docs/superpowers/plans/` for the build plan.

## Security note

The legacy `tracker/fetch.py` had a hardcoded ERPNext API token. That token must
be **rotated** in ERPNext (deactivate the old key/secret, issue a new one) and
supplied only via `FAIRCODE_ERP_TOKEN`. Treat the old token as compromised.
