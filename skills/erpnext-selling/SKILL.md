---
name: erpnext-selling
description: >-
  Use when setting up or troubleshooting the Selling module in ERPNext.
  Triggers on "sales setup", "customer", "quotation", "sales order", "delivery
  note", "price list", "pricing rules", "sales invoice", "sales return",
  "credit note". Covers the full quote-to-cash flow for Indian businesses.
---

# ERPNext Selling - Quote to Cash

The selling flow is: Quotation → Sales Order → Delivery Note → Sales Invoice →
Payment Entry. Each step has a specific purpose. Skipping steps causes stock
and GL mismatches.

## Prerequisites
Items, warehouses, Chart of Accounts, GST tax templates configured
(`erpnext-accounts-gst`), payment terms.

## Configuration sequence

**1. Selling Settings**
Selling → Settings → Selling Settings:
- Customer Naming By: Customer Name or Naming Series (use Naming Series for large customer bases).
- Default Price List: "Standard Selling" (create specific lists per tier later).
- Sales Order Required: Yes (before Delivery Note - prevents unconfirmed deliveries).
- Delivery Note Required: Yes (before Sales Invoice - ensures stock is updated before billing).
  Set to No only if the client invoices without physical delivery (services, software).

**2. Customer master**
Selling → Customer. Required fields:
- Customer Name, Customer Group (for pricing rules and reporting), Territory.
- GST Category and GSTIN (see `erpnext-accounts-gst`).
- Currency (default INR; set USD/EUR for export customers).
- Default Price List: which tier of prices this customer sees.
- Payment Terms: Net 30, Advance, etc.
- Credit Limit: enforced on Sales Order submission if Credit Controller role is active.

**3. Price Lists**
Selling → Price List. One per pricing tier: "Retail", "Wholesale", "Distributor", "Export".
Set currency and "For Selling" = Yes. Assign to Customer master.

**4. Item Prices**
Stock → Item Price. Set rate per item per price list. Set effective dates for
time-limited promotions. Bulk-load via Data Import (Stock → Item Price).

**5. Pricing Rules**
Selling → Pricing Rule. Use for:
- Quantity-based discount: buy 10+ units → 5% off. Set Min Qty.
- Customer Group discount: Distributors get 10% off Standard Selling.
- Date-range promotion: Diwali offer 8-15 Nov, 15% off item group "Electronics".
- Free item: buy Product A, get Product B free (set as product bundle).
- Priority field: higher number wins when multiple rules apply to the same transaction.

**6. Quotation**
Selling → Quotation. Select Customer (or Lead for pre-customer prospects).
Add items, verify tax template (in-state vs inter-state), set Valid Till date.
Send via ERPNext email. On customer acceptance: Quotation → "Make Sales Order".

**7. Sales Order**
Confirms the sale. Sets delivery date and reserves stock (if Stock Reservation
is enabled in Stock Settings). Triggers procurement if material is short.
SO cannot be edited after submission - amend and resubmit if changes needed.

**8. Delivery Note**
Stock → Delivery Note. Create from Sales Order. Physically records goods
leaving the warehouse. Submit updates stock immediately (deducts from warehouse).
Required before Sales Invoice if "Delivery Note Required" is on.

**9. Sales Invoice**
Accounts → Sales Invoice. Create from Delivery Note or directly from SO
(if "Update Stock" is checked on the invoice - only if skipping Delivery Note).
Submit triggers GL posting and GST output tax entries.
For e-invoicing: IRN generated automatically on submit (India Compliance app).

**10. Payment Entry**
Accounts → Payment Entry → Receive. Select Customer, received amount, received
account (bank or cash). In the "Outstanding Invoices" table: allocate to the
specific invoice. Submit to post GL.

**11. Sales Return (Credit Note)**
Sales Invoice → Return button. Creates a negative invoice. If physical goods
are returned, also create a Return Delivery Note from the original Delivery Note.
The Return Delivery Note updates stock back into the warehouse.

**12. Sales analytics**
Selling → Reports: Sales Order Trends, Item-wise Sales History, Sales Person-wise
Transaction Summary, Territory-wise Sales.

## Fit-gaps

| Vanilla ERPNext | What's missing | Solution |
| --- | --- | --- |
| Pricing Rules handle most cases | Complex multi-tier distributor schemes with zone/scheme combos | Custom pricing logic in Sales Order controller |
| Manual advance allocation | Auto-apply advance to oldest invoice | Payment Reconciliation Tool (manual run) |
| Standard print formats | Branded invoice with company logo, PO number, bank details | Custom Jinja print format (`frappe-impl-print-format`) |

## Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Delivery Note not created → stock not updated | Enable "Delivery Note Required" in Selling Settings; or use "Update Stock" on Sales Invoice |
| Pricing rule not applying | Check: priority conflicts, customer group assignment, valid date range, Min Qty threshold |
| Wrong tax template → CGST instead of IGST | Fix GST Category on Customer and verify Place of Supply on invoice |
| Credit limit not enforced | Enable "Credit Controller" role; set Credit Limit on Customer master |
| Quotation expired but still converted to SO | Set "Valid Till" on quotation; expired quotations block SO creation |

## Definition of Done
- Customer masters complete: GST category, GSTIN, price list, payment terms.
- Item prices set for all active items in all applicable price lists.
- Full test cycle: Quotation → SO → Delivery Note → Sales Invoice → Payment.
- Sales Return (Credit Note + Return Delivery Note) tested.
- GST amounts verified on in-state and inter-state test invoices.

## Related Skills
`erpnext-accounts-gst`, `erpnext-stock`, `erpnext-buying`, `erpnext-crm`
