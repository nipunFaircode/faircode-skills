---
name: erpnext-buying
description: >-
  Use when setting up or troubleshooting the Buying module in ERPNext. Triggers
  on "purchase setup", "supplier", "purchase order", "GRN", "goods receipt",
  "purchase invoice", "RFQ", "landed cost", "subcontracting", "debit note".
  Covers the full purchase-to-pay flow for Indian businesses.
---

# ERPNext Buying - Purchase to Pay

The buying flow is: Material Request → RFQ → Supplier Quotation → Purchase
Order → Purchase Receipt (GRN) → Purchase Invoice → Payment Entry. Each step
has a specific purpose - skipping GRN before invoice causes stock and valuation
errors.

## Prerequisites
Items, warehouses, Chart of Accounts, GST tax templates (`erpnext-accounts-gst`),
payment terms.

## Configuration sequence

**1. Buying Settings**
Buying → Settings → Buying Settings:
- Supplier Naming By: Supplier Name or Naming Series.
- Purchase Order Required: Yes (before Purchase Receipt - prevents unauthorised receipts).
- Purchase Receipt Required: Yes (before Purchase Invoice - ensures stock is updated before payable is booked).

**2. Supplier master**
Buying → Supplier. Required fields:
- Supplier Name, Supplier Group (for reporting and pricing).
- GST Category and GSTIN (input tax credit depends on supplier's valid GSTIN).
- Currency (INR default; USD/EUR for imports).
- Default Payment Terms: Net 30, Advance 100%, etc.
- Bank details: Accounts tab → Bank Account (for payment advice/NEFT).
- Tax Withholding Category: link the applicable TDS section (194C, 194J, 194H).

**3. Material Request**
Stock → Material Request. Raised by stores or production when stock is needed.
Type: Purchase. Approver reviews and approves before RFQ.
Material Requests feed into the Production Plan's MRP run.

**4. RFQ (Request for Quotation)**
Buying → Request for Quotation. Created from Material Request or directly.
Add 2-3 suppliers per item. Send via ERPNext email → each supplier fills their
quote via the Supplier Quotation DocType (or you enter on their behalf).

**5. Supplier Quotation comparison**
Buying → Supplier Quotation → List → "Compare Quotations" tool. Side-by-side
rate and delivery date comparison per item. Select winning supplier → "Make
Purchase Order".

**6. Purchase Order**
Buying → Purchase Order. Confirm quantity, rate, delivery date, payment terms,
tax template. Submit to commit. Multi-level approval requires a Workflow
(not default - configure separately).

**7. Purchase Receipt (GRN)**
Stock → Purchase Receipt. Create from PO when goods arrive at warehouse.
Record actual received quantity (may differ from PO if partial delivery).
Optionally link to a Quality Inspection. Submit → stock updated, landed cost
can now be added.

**8. Landed Cost Voucher**
Stock → Landed Cost Voucher. Link to the Purchase Receipt. Add freight,
customs duty, insurance, loading charges. These costs are distributed across
items by qty, amount, or weight and added to item valuation.
Create this immediately after the GRN - before any stock is consumed.

**9. Purchase Invoice**
Accounts → Purchase Invoice. Create from Purchase Receipt. ERPNext checks
quantity matches the GRN. Submit → GL posted (Stock Received But Not Billed
cleared, Creditors/Accounts Payable credited, GST Input Tax debit).
Input Tax Credit (ITC) is available only if the supplier's GSTIN is valid
and the supplier has filed their GSTR-1.

**10. TDS on Purchase Invoice**
If Tax Withholding Category is set on the supplier: on the Purchase Invoice,
check "Apply Tax Withholding Amount". ERPNext calculates TDS, deducts from
payable, and creates a TDS payable liability.

**11. Payment Entry**
Accounts → Payment Entry → Pay. Select Supplier, amount, bank account.
Allocate to outstanding invoices. Submit → GL posted (Creditors Dr / Bank Cr).
PDC (Post-Dated Cheque): create Payment Entry with a future date.

**12. Purchase Return (Debit Note)**
Purchase Invoice → Return button. Creates a negative invoice.
Physical goods return: create Purchase Return from the original Purchase Receipt
first (updates stock), then link to the Debit Note.

## Fit-gaps

| Vanilla ERPNext | What's missing | Solution |
| --- | --- | --- |
| Basic PO approval | Multi-level approval (Manager → Finance → Director) | Configure Workflow on Purchase Order |
| No NEFT batch file | Bank payment file export for bulk NEFT | Manual upload to bank portal; or custom export report |
| Partial GRN handling | Complex partial delivery matching across multiple GRNs | Train users to use "Quantity Not Received" column in PO |
| Basic import duty | Complex customs entry with BoE-linked accounting | Custom Landed Cost logic or accountant journal entry |

## Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Invoice created without GRN → stock not updated | Enable "Purchase Receipt Required" in Buying Settings |
| Landed cost not added → wrong item valuation | Create Landed Cost Voucher immediately after GRN, before stock consumption |
| Supplier GSTIN not set → ITC disallowed | Mandatory GSTIN on all registered suppliers before first purchase |
| PO vs GRN quantity mismatch found at invoice | Run "Purchase Order Items to Receive" report weekly; resolve discrepancies before invoice |
| Advance to supplier not reconciled → risk of double payment | Use Payment Reconciliation Tool after every advance payment |

## Definition of Done
- Supplier masters complete: GSTIN, payment terms, TDS category, bank details.
- Full test cycle: Material Request → RFQ → Supplier Quotation → PO → GRN → Purchase Invoice → Payment.
- Landed Cost Voucher tested on one import purchase.
- Purchase Return (Debit Note + stock return) tested.
- GST input credit entries verified on test invoice.

## Related Skills
`erpnext-accounts-gst`, `erpnext-stock`, `erpnext-selling`
