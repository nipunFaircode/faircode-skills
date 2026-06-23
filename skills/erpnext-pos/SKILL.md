---
name: erpnext-pos
description: >-
  Use when configuring Point of Sale in ERPNext for a retail or F&B business.
  Triggers on "POS setup", "cashier", "retail", "point of sale", "POS profile",
  "shift closing", "UPI payment at counter", "offline POS", "POS closing entry".
  Covers POS profile, payment modes, shift management, returns, and GST
  compliance at the counter.
---

# ERPNext Point of Sale

POS has a separate permission and configuration layer from the rest of ERPNext.
Set up the POS Profile correctly before any cashier touches the terminal.

## Prerequisites
Items with "Is Sales Item" = Yes, warehouses, Chart of Accounts (Cash account,
UPI/card clearing accounts), GST tax templates, user accounts for cashiers,
print format for GST-compliant receipt.

## Key decisions - confirm before configuring

- How many POS terminals (physical or browser tabs)?
- Payment modes accepted: Cash / Card / UPI / Credit?
- Customer required on every transaction or walk-in allowed?
- Returns policy: refund to original mode or store credit?
- Offline mode needed? (test thoroughly before go-live)

## Configuration sequence

**1. Walk-in Customer**
Create a generic Customer: "Walk-In Customer" with GST Category = Consumer.
This is the default customer for anonymous retail transactions.
For B2B customers wanting a GST invoice: cashier creates a new customer at the
counter with GSTIN.

**2. POS Profile**
Accounts → Point of Sale → POS Profile. One per terminal type or branch.

| Field | Setting |
| --- | --- |
| Company | Select the entity |
| Warehouse | Stock source for POS sales |
| Customer | "Walk-In Customer" (default) |
| Currency | INR (or USD for export counter) |
| Price List | The applicable price list |
| Taxes and Charges Template | In-state GST template for the store's location |
| Print Format | Your GST-compliant POS receipt format |
| Applicable for Users | Add cashier user accounts - only these users see this profile |

**3. Payment Methods (on POS Profile)**
Add each payment mode as a row:

| Mode | Account |
| --- | --- |
| Cash | Cash account (under Current Assets) |
| Card | Credit/Debit Card Clearing account |
| UPI | UPI Receivable account |
| Credit | Customer's Receivable account (for credit sales) |

Each payment method maps to a GL account. Wrong mapping = closing entry
posting error.

**4. Item visibility in POS**
Default: all "Is Sales Item" items appear. To restrict:
- Add item group filter in POS Profile → "Item Groups" table.
- To hide specific items: Item master → "Hide in POS" = Yes.
- High-value or non-saleable items should be hidden to avoid cashier errors.

**5. POS Opening Entry**
Cashier logs in → opens POS → "Open POS" → enters opening cash balance
(by denomination: ₹500 × 10, ₹100 × 20, etc.). This creates a POS Opening Entry.
Without opening the shift, the cashier cannot process transactions.

**6. POS Transaction flow**
1. Search item by name or scan barcode → adds to cart.
2. Set quantity. Apply item-level discount if allowed (set discount allowed % in POS Profile).
3. Select Customer if GST invoice is requested.
4. Choose payment mode. Split payment across multiple modes if needed.
5. "Complete Order" → Sales Invoice created and submitted automatically.
6. Print receipt.

**7. Customer creation at counter (B2B)**
POS → "New Customer" button (if enabled in POS Profile). Quick form:
Customer Name, GSTIN, State/UT. Creates a Customer record instantly.
Required for customers who want input tax credit on their purchase.

**8. POS Closing Entry**
End of shift: POS → "Close POS" → enter actual cash in drawer by denomination.
System shows expected cash (opening + cash sales) vs actual (what cashier counts).
Variance is posted to a Cash Difference account.
Submit Closing Entry to close the shift. Cashier cannot process transactions after closing.

**9. Returns at POS**
POS → Returns → select original POS Invoice → create return.
Refund via the same payment mode or a different mode (e.g., cash refund for card purchase).
Stock returned automatically to the POS warehouse.
Do not create a new POS transaction for a return - always use the Return button against the original invoice.

**10. Offline mode**
Enable in POS Profile → "Allow POS Offline". POS stores transactions in the
browser's IndexedDB. When network is restored, cashier clicks "Sync" to post
pending invoices to ERPNext.
Test offline sync in staging before go-live. Check browser console for sync
errors. Train cashiers: do not close the browser tab while transactions are
unsynced.

**11. GST receipt compliance**
The POS receipt print format must include:
- Business GSTIN, address, state.
- HSN/SAC code per item.
- Tax breakdown: CGST and SGST amounts separately.
- QR code (if business turnover > ₹5 crore and India Compliance app installed).

## Fit-gaps

| Vanilla ERPNext | What's missing | Solution |
| --- | --- | --- |
| Basic barcode scan (fills item field) | Weighing scale integration (qty from scale barcode) | Custom hardware bridge script |
| No loyalty/points system | Customer loyalty rewards | Custom app |
| No kitchen display | F&B order routing to kitchen screen | Custom real-time integration (`frappe-core-realtime`) |
| No GST QR on POS receipt | Mandate for turnover > ₹5 crore | India Compliance app |
| No BNPL/EMI at counter | Financing options | Third-party fintech integration |

## Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Cashier not in POS Profile → "No POS Profile found" error | Add cashier user account to "Applicable for Users" in POS Profile |
| Payment account not mapped → GL error on closing | Verify every payment method has a valid account before go-live |
| Offline sync failure → invoices lost | Test sync in staging; never close browser tab with unsynced transactions |
| Return done as new sale, not via Return button | Always use "Return Against POS Invoice" - free-form return breaks stock and GL |
| POS Closing variance unresolved → carry-forward error | Investigate before submitting; get manager sign-off on any variance |

## Definition of Done
- POS Profile created per terminal type; cashier users assigned.
- All payment methods mapped to correct GL accounts.
- Walk-in customer created and set as default.
- GST-compliant receipt format configured and tested.
- Full test: open shift → sale → split payment → close shift → GL entries verified.
- Return transaction tested.
- Offline mode tested: disconnect network, make sale, reconnect, sync, verify invoice.

## Related Skills
`erpnext-selling`, `erpnext-accounts-gst`, `erpnext-stock`
