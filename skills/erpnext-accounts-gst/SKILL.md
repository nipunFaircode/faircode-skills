---
name: erpnext-accounts-gst
description: >-
  Use when setting up GST, e-invoicing, or TDS/TCS in ERPNext for an Indian
  company. Triggers on "GST setup", "e-invoicing", "GSTR", "TDS", "tax
  template", "IRN", "HSN", "Place of Supply", "reverse charge". Covers the
  full India tax configuration from Chart of Accounts to e-invoice submission.
---

# ERPNext Accounts - GST & India Tax

Every Indian ERPNext implementation needs this done before the first transaction.
Get it wrong here and every invoice, every GSTR report, and every IRN is wrong.

## Prerequisites
- Company created with India as country.
- Chart of Accounts set up using the India template (auto-creates GST accounts).
- Fiscal Year configured (1 Apr - 31 Mar).

## Configuration sequence

**1. GST accounts in CoA**
If you used the India CoA template these exist already. Verify:
- CGST Payable, SGST Payable, IGST Payable, CESS Payable (under Duties and Taxes)
- CGST Receivable, SGST Receivable, IGST Receivable (under Current Assets)

**2. Company GSTIN and state**
Setup → Company → Tax ID field: enter the company's GSTIN (15-character).
Set the State field - this drives the CGST/IGST split on all invoices.

**3. Accounts Settings**
Accounts → Settings → Accounts Settings:
- Enable "Round Off GST": Yes (rounds GST to 2 decimal places per GST rules).
- Enable "Determine Address Tax Category From": Bill To Address (default and correct).

**4. GST Category on all parties**
Every Customer and Supplier must have a GST Category:
- Registered - has GSTIN, gets ITC.
- Unregistered - no GSTIN, no ITC (B2C or unregistered B2B).
- SEZ - special economic zone, zero-rated or exempt.
- Overseas - exports, zero-rated.
- Consumer - individual consumer, no GSTIN.

**5. GSTIN on all registered parties**
Customer/Supplier → GST Details section → GSTIN. Validate format: 15 chars,
first 2 = state code, next 10 = PAN, position 13 = entity number, 14 = Z, 15 = check digit.
Wrong GSTIN → IRN rejection at NIC portal.

**6. HSN/SAC codes on all items**
Item master → HSN/SAC field. Mandatory for e-invoicing. Bulk-set via:
Stock → Data Import → Item → download template → fill HSN column → upload.

**7. Tax templates**
Accounts → Tax Templates → Sales Taxes and Charges Template. Create:
- "GST 18% In-State": CGST 9% (account: CGST Payable) + SGST 9% (account: SGST Payable).
- "GST 18% Inter-State": IGST 18% (account: IGST Payable).
- Repeat for 5%, 12%, 28% rates as needed.
Set default tax template on Item Group or individual Item.

**8. Place of Supply logic**
ERPNext determines CGST/SGST vs IGST by comparing:
- Company's state (from Company master).
- Customer's Place of Supply (billing state, pulled from Customer address).
Same state → CGST + SGST. Different state → IGST.
Always verify Place of Supply on the invoice before submission.

**9. TDS setup**
Accounts → Tax Withholding Category. Create per section:
- 194C (contractors): Individual/HUF 1%, Others 2%, threshold ₹30,000 single / ₹1,00,000 aggregate.
- 194J (professional/technical): 10%, threshold ₹30,000.
- 194H (commission/brokerage): 5%, threshold ₹15,000.
Link Tax Withholding Category to Supplier master → Accounts tab.
On Purchase Invoice: "Apply Tax Withholding Amount" checkbox → Yes.

**10. Reverse Charge Mechanism (RCM)**
For RCM supplies (e.g., GTA freight, legal services from unregistered):
On the Purchase Invoice tax line, check "Is Reverse Charge". This posts GST
liability to the output tax account instead of input credit.

**11. E-invoicing (IRN generation)**
Vanilla ERPNext does not generate IRN. Requires the India Compliance app.
Install: `bench get-app india_compliance && bench --site sitename install-app india_compliance`.
Configure: GST Settings → E-Invoicing → enable per company, enter NIC API credentials.
After enabling: Sales Invoice submit → IRN generated automatically → QR code attached to print format.

**12. GSTR reports**
Accounts → GST Reports:
- GSTR-1: monthly outward supplies. Run before the 11th of the following month.
- GSTR-3B: monthly summary return. Run before the 20th.
- GSTR-2A: auto-populated from supplier filings. Download from GST portal and compare.

## Fit-gaps

| Vanilla ERPNext | What's missing | Solution |
| --- | --- | --- |
| No IRN/QR generation | E-invoicing for turnover > ₹5 crore | India Compliance app |
| No GSTR-2A reconciliation | Auto-match purchases with portal data | India Compliance app |
| No e-way bill generation | Transport documents for goods > ₹50,000 | India Compliance app or third-party |
| No TDS challan/Form 26Q | Quarterly TDS return filing | TRACES portal manual / ClearTax |

## Common pitfalls

| Pitfall | Fix |
| --- | --- |
| GSTIN not set on party → IRN rejection | Mandatory GSTIN on all registered parties before go-live |
| Wrong Place of Supply → CGST instead of IGST | Verify billing address state matches GSTIN state prefix for every inter-state customer |
| HSN not set on item → e-invoice fails at NIC | Bulk-set HSN before enabling e-invoicing |
| TDS not applied on advance payments | Apply Tax Withholding Category on Payment Entry, not just Purchase Invoice |
| RCM not flagged on applicable purchases | Train accounts team: GTA, legal, security services from unregistered → RCM checkbox |

## Definition of Done
- GST accounts present in CoA; GSTIN set on company and all registered parties.
- Tax templates created for all applicable rates (5/12/18/28%), in-state and inter-state.
- HSN/SAC set on all active items.
- TDS categories created and linked to applicable suppliers.
- Place of Supply verified on test invoices (in-state and inter-state).
- E-invoicing tested end-to-end on staging (if India Compliance installed).
- GSTR-1 report runs without errors for the test period.

## Related Skills
`erpnext-selling`, `erpnext-buying`, `erpnext-payroll-india`
