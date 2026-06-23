---
name: frappe-impl-print-format
description: >-
  Use when creating or customising a Print Format in Frappe. Triggers on "print
  format", "invoice design", "PDF layout", "letterhead", "custom print",
  "print template", "wkhtmltopdf", "PDF generation". Covers Jinja print formats,
  Letter Head, PDF generation API, multi-language, and PDF rendering pitfalls.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
---

# Frappe Print Formats

Two types exist. Use Jinja for all new formats - JS-based is legacy.

| Type | When to use |
| --- | --- |
| Jinja (HTML + Jinja2) | All new formats. Full control over layout and logic. |
| JS-based | Avoid. Only if editing an existing legacy format. |

## Step 1: Letter Head (do this first)

Setup → Letter Head. Fields:
- Letter Head Name, Is Default (Yes for one).
- Header: HTML with company logo (`<img src="/files/logo.png">`) and address.
- Footer: HTML with bank details, terms, page number.

```html
<!-- Header example -->
<div style="display:flex; justify-content:space-between; align-items:center;">
  <img src="/files/company-logo.png" style="height:60px;">
  <div style="text-align:right; font-size:10pt;">
    <strong>Faircode Next Pvt. Ltd.</strong><br>
    Bangalore - 560001<br>
    GSTIN: 29XXXXX1234Z1
  </div>
</div>
```

## Step 2: Create the Print Format

Setup → Print Format → New.
- Name, DocType (e.g., Sales Invoice), Format Type: Jinja.
- Paste HTML in the content area.
- Set Letter Head: Yes, Default Print Format: Yes (optional).

## Jinja print format skeleton

```html
<style>
  .print-section { font-family: Arial, sans-serif; font-size: 10pt; color: #333; }
  table { width: 100%; border-collapse: collapse; margin: 8px 0; }
  th { background: #f0f0f0; font-weight: bold; text-align: left; padding: 6px 8px; border: 1px solid #ccc; }
  td { padding: 5px 8px; border: 1px solid #ccc; vertical-align: top; }
  .text-right { text-align: right; }
  .total-row { font-weight: bold; background: #f9f9f9; }
</style>

<div class="print-section">

  {# Party info section #}
  <table style="border:none;">
    <tr>
      <td style="border:none; width:50%;">
        <strong>Bill To:</strong><br>
        {{ doc.customer_name }}<br>
        {{ doc.address_display | replace('\n', '<br>') }}
        {% if doc.tax_id %}<br>GSTIN: {{ doc.tax_id }}{% endif %}
      </td>
      <td style="border:none; text-align:right;">
        <strong>Invoice No:</strong> {{ doc.name }}<br>
        <strong>Date:</strong> {{ frappe.format(doc.posting_date, {'fieldtype': 'Date'}) }}<br>
        {% if doc.po_no %}
        <strong>PO Ref:</strong> {{ doc.po_no }}<br>
        {% endif %}
        <strong>Due Date:</strong> {{ frappe.format(doc.due_date, {'fieldtype': 'Date'}) }}
      </td>
    </tr>
  </table>

  {# Items table #}
  <table>
    <thead>
      <tr>
        <th>#</th>
        <th>Item</th>
        <th>HSN/SAC</th>
        <th class="text-right">Qty</th>
        <th class="text-right">Rate</th>
        <th class="text-right">Amount</th>
      </tr>
    </thead>
    <tbody>
      {% for item in doc.items %}
      <tr>
        <td>{{ item.idx }}</td>
        <td>{{ item.item_name }}{% if item.description %}<br><small>{{ item.description }}</small>{% endif %}</td>
        <td>{{ item.gst_hsn_code or '' }}</td>
        <td class="text-right">{{ item.qty }} {{ item.uom }}</td>
        <td class="text-right">{{ frappe.format(item.rate, {'fieldtype': 'Currency', 'currency': doc.currency}) }}</td>
        <td class="text-right">{{ frappe.format(item.amount, {'fieldtype': 'Currency', 'currency': doc.currency}) }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  {# Taxes and totals #}
  <table style="width:40%; margin-left:60%;">
    <tr><td>Subtotal</td><td class="text-right">{{ frappe.format(doc.net_total, {'fieldtype': 'Currency', 'currency': doc.currency}) }}</td></tr>
    {% for tax in doc.taxes %}
    <tr><td>{{ tax.description }}</td><td class="text-right">{{ frappe.format(tax.tax_amount, {'fieldtype': 'Currency', 'currency': doc.currency}) }}</td></tr>
    {% endfor %}
    <tr class="total-row"><td>Total</td><td class="text-right">{{ frappe.format(doc.grand_total, {'fieldtype': 'Currency', 'currency': doc.currency}) }}</td></tr>
    {% if doc.outstanding_amount %}
    <tr><td>Amount Due</td><td class="text-right"><strong>{{ frappe.format(doc.outstanding_amount, {'fieldtype': 'Currency', 'currency': doc.currency}) }}</strong></td></tr>
    {% endif %}
  </table>

  {# Terms #}
  {% if doc.terms %}
  <div style="margin-top:16px; font-size:9pt; color:#555;">
    <strong>Terms & Conditions:</strong><br>{{ doc.terms }}
  </div>
  {% endif %}

</div>
```

## Key Jinja methods in print context

```jinja2
{# Format currency with locale and symbol #}
{{ frappe.format(doc.amount, {'fieldtype': 'Currency', 'currency': doc.currency}) }}

{# Format date per user locale #}
{{ frappe.format(doc.posting_date, {'fieldtype': 'Date'}) }}

{# Convenience method using the field's own fieldtype #}
{{ doc.get_formatted('grand_total') }}

{# Fetch a linked value (use sparingly - adds a DB call per use) #}
{{ frappe.db.get_value('Customer', doc.customer, 'customer_group') }}

{# Conditional block #}
{% if doc.is_return %}<strong>CREDIT NOTE</strong>{% endif %}
```

## Generate PDF from Python

```python
# Get PDF bytes
pdf = frappe.get_print(
    doctype="Sales Invoice",
    name=doc.name,
    print_format="My Invoice Format",
    as_pdf=True
)

# Attach PDF to document
frappe.attach_print(
    doctype=doc.doctype,
    name=doc.name,
    file_name=f"{doc.name}.pdf",
    print_format="My Invoice Format"
)
```

## Version notes

- v14/v15 (default): wkhtmltopdf renders PDFs. Limited CSS - avoid flexbox/grid
  for layout; use tables instead.
- v15+ option: weasyprint (better CSS support). Enable in PDF Settings.
  Check which engine the client's site uses before designing the layout.

## Anti-patterns

| Do NOT | Do Instead |
| --- | --- |
| `{{ doc.amount }}` raw for currency | `{{ frappe.format(doc.amount, {'fieldtype': 'Currency'}) }}` |
| `import datetime` in Jinja | Use `frappe.utils.getdate()`, `frappe.utils.formatdate()` |
| Screen flexbox/grid CSS for PDF layout | Use `<table>` for layout when targeting wkhtmltopdf |
| `@media print` CSS rules | Write print CSS directly - wkhtmltopdf ignores media queries |
| Fetch many linked values in the template | Pre-fetch in a controller or use `frappe.get_doc()` once |

## Definition of Done
- Print format saved and accessible on the DocType.
- PDF downloaded and verified: layout correct, currency formatted, GST amounts
  match the invoice, Letter Head logo and address appear.
- Tested in both Chrome preview (HTML) and actual PDF download.
- Tested with a long item list to verify page break behaviour.

## Related Skills
`frappe-syntax-print`, `frappe-impl-jinja`, `frappe-syntax-jinja`
