---
name: erpnext-stock
description: >-
  Use when setting up or troubleshooting the Stock/Inventory module in ERPNext.
  Triggers on "inventory setup", "warehouse", "item master", "valuation method",
  "batch tracking", "serial number", "stock reconciliation", "reorder level",
  "UOM conversion". Covers warehouse hierarchy, item setup, valuation, batch/
  serial tracking, and opening stock.
---

# ERPNext Stock - Inventory Setup

The valuation method and warehouse structure are the two decisions you cannot
easily change after transactions start. Lock these down before opening stock.

## Prerequisites
Company, Chart of Accounts (stock accounts: Stock In Hand, Stock Received But
Not Billed, Stock Adjustment Account), items (at minimum, item names and groups).

## Key decisions - confirm with client before any configuration

**Valuation method:** FIFO or Moving Average?
- FIFO: stock value reflects actual purchase cost layers. Used by traders where
  purchase price varies. Required by some statutory auditors.
- Moving Average: item cost is a running average of all purchases. Used by most
  manufacturers. Simpler for production costing.
- Set at company level in Stock Settings. Cannot change after transactions exist
  without closing all stock and doing a full reconciliation.
- If unsure: ask the client's CA.

**Batch tracking:** which items need batch numbers?
Used for: pharmaceuticals, food, chemicals (expiry dates), dye lots, fabric rolls.
Batch tracking adds a mandatory batch field on every stock transaction for those items.

**Serial number tracking:** which items need serial numbers?
Used for: electronics, machinery, assets tracked individually (warranty, AMC).
Serial tracking adds a mandatory serial number field on every stock transaction.

**Warehouse granularity:** how many warehouse locations?
ERPNext warehouse is the minimum unit (no bin/rack/shelf in vanilla).
Confirm the number of physical stores before building the hierarchy.

## Configuration sequence

**1. Stock Settings**
Stock → Settings → Stock Settings:
- Valuation Method: FIFO or Moving Average (company-wide default).
- Allow Negative Stock: No. Set this before go-live and don't change it.
- Automatically Set Serial No Based on FIFO: Yes if using serial numbers.
- Item Naming By: Item Code (recommended for imports) or Naming Series.

**2. Warehouse hierarchy**
Stock → Warehouse. Build top-down:
```
Faircode Ltd (Company)
├── Bangalore (Zone/City - optional grouping level)
│   ├── Raw Material Store
│   ├── Work In Progress
│   ├── Finished Goods
│   └── Rejection / Scrap
└── Mumbai (if multi-location)
    └── ...
```
Each leaf warehouse must have an Account (GL link for stock valuation).
Group warehouses (non-leaf) have no account.

**3. Item master**
Stock → Item. Key fields:
- Is Stock Item: Yes for physical inventory.
- Item Group: for pricing rules, reports, and default tax templates.
- Default Unit of Measure: the base UOM (Nos, Kg, Litre, Metre).
- UOM Conversion: define conversions if the item is bought in one UOM and sold
  in another (e.g., Box of 12 Nos → enter conversion factor 12 on the item).
- Valuation Method: leave blank to inherit company default, or override per item.
- Has Batch No: Yes for batch-tracked items.
- Has Serial No: Yes for serially-tracked items.
- Has Expiry Date: Yes for batch items with expiry (enables FEFO picking).
- Re-order Level and Re-order Qty: for Material Request auto-generation report.
- Default Warehouse: where stock lands on purchase receipt.

**4. Opening stock**
Stock → Stock Reconciliation. Enter opening balances per item per warehouse.
Set posting date to the go-live date (not before - past dates pull stale rates).
Submit once reviewed - cancelled stock reconciliations create correction entries.
For batch/serial items: use Stock Entry → Material Receipt instead (allows batch/serial assignment).

**5. Batch setup**
If Has Batch No = Yes: batches auto-created on Purchase Receipt.
Stock → Batch Numbering Series: set a series (BATCH-.####).
For expiry-tracked items: Has Expiry Date = Yes on item. Enter expiry date on
batch at time of receipt.
Batch-wise stock balance: Stock → Reports → Batch-wise Balance History.

**6. Serial number setup**
If Has Serial No = Yes: serial numbers created on Purchase Receipt (auto or
manual entry). Serial numbering convention: confirm with client (often based on
the vendor's serial number).
Serial number status: Stock → Serial No → filter by status (Active/Delivered/Expired).

**7. Reorder report**
Stock → Reports → Itemwise Recommended Reorder Level. Run weekly.
Items below reorder level appear here. Manually create Material Request or
enable auto-creation via Scheduler (Stock Settings → Auto Material Request).

**8. Stock Reconciliation (periodic)**
Use for physical count discrepancies. Stock → Stock Reconciliation.
Difference (positive or negative) posts to Stock Adjustment Account in GL.

**9. Inter-warehouse transfer**
Stock → Stock Entry → Purpose: Material Transfer.
Source Warehouse and Target Warehouse. GL posts stock value movement between
warehouse accounts.

## Fit-gaps

| Vanilla ERPNext | What's missing | Solution |
| --- | --- | --- |
| Warehouse = lowest unit | Bin/rack/shelf tracking | Custom app or third-party WMS |
| Basic barcode (scan to fill field) | Full WMS scanning workflow (pick/pack/put-away) | Custom app or Frappe WMS app |
| Manual FEFO picking | Auto FEFO batch selection on Delivery Note | Custom Client Script or batch selection override |
| Lot traceability | Forward/backward trace is manual via Batch Traceability report | Use Stock → Reports → Batch-wise Balance History + filter |

## Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Valuation method changed after transactions | Lock at day 1. Change requires closing all stock and a full reconciliation |
| UOM conversion factor wrong | Audit all conversions before opening stock entry - errors compound |
| Allow Negative Stock = Yes in production | Set No before go-live. Negative stock hides process gaps |
| Opening stock on wrong posting date | Use go-live date exactly. Past dates can create negative stock scenarios |
| Batch not assigned on delivery → FEFO not respected | Make batch mandatory on Delivery Note via custom validation for batch-tracked items |

## Definition of Done
- Valuation method confirmed and locked (client and CA sign-off if needed).
- Warehouse hierarchy built with GL accounts on all leaf warehouses.
- All active items in system: UOM, item group, reorder levels, batch/serial flags.
- Opening stock entered and submitted for go-live date.
- Batch/serial tracking tested end-to-end (receipt → delivery) for applicable items.
- Stock Reconciliation process demonstrated to client.

## Related Skills
`erpnext-selling`, `erpnext-buying`, `erpnext-manufacturing`
