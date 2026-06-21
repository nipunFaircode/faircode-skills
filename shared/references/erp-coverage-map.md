# ERP Coverage Map

The discovery agenda. `faircode-requirements-discovery` walks the consultant (or
customer) through every in-scope item below, one question at a time, and marks
each `answered`, `N/A — reason`, or `open`. No solution is proposed while any
in-scope item is `open`.

## Core modules
- **Selling** — quotations, sales orders, pricing rules, discounts, customer
  groups, territories, sales taxes, delivery terms.
- **Buying** — supplier groups, RFQ, purchase orders, supplier quotations,
  purchase taxes, payment terms.
- **Stock / Inventory** — items, item groups, UOMs, warehouses, valuation
  method, batch/serial, stock reconciliation, reorder levels.
- **Manufacturing** — BOMs, work orders, routing, workstations, job cards,
  subcontracting, capacity planning.
- **Accounts / Finance** — chart of accounts, cost centers, fiscal year,
  journal entries, payment entries, bank reconciliation, taxes & charges,
  multi-currency.
- **HR & Payroll** — employees, departments, designations, attendance, leaves,
  salary structures, payroll cycle, statutory deductions.
- **Projects** — project types, tasks, timesheets, billing, profitability.
- **CRM** — leads, opportunities, sales pipeline, communication tracking.
- **Assets** — asset categories, depreciation, maintenance, disposal.
- **Quality** — quality inspections, procedures, goals, non-conformance.
- **Support / Helpdesk** — issues, SLAs, service contracts.
- **Website / Portal** — customer/supplier portal, web forms, e-commerce.

## Cross-cutting aspects (always ask)
- **Company & org structure** — number of companies, branches, consolidation.
- **Chart of accounts** — existing CoA to import vs standard template.
- **Taxes** — tax regime, tax templates, withholding, e-invoicing.
- **Naming series** — document numbering conventions per doctype.
- **Roles & permissions** — who can see/do what; approval hierarchy.
- **Workflows & approvals** — which documents need multi-step approval.
- **Print formats** — branded invoices, POs, letterheads, language.
- **Integrations** — payment gateways, banks, shipping, existing systems, APIs.
- **Data migration sources** — what master/transaction data to import, from
  where (Excel, legacy ERP, Tally, etc.), and in what cutover state.
- **Reporting & KPIs** — the reports and dashboards the business runs on.
- **Multi-currency / multi-company** — consolidation and inter-company flows.
- **Languages & localisation** — UI language, regional compliance.
