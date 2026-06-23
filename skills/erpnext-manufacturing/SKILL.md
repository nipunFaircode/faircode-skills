---
name: erpnext-manufacturing
description: >-
  Use when configuring the Manufacturing module in ERPNext. Triggers on "BOM",
  "bill of materials", "work order", "production", "job card", "workstation",
  "routing", "subcontracting", "capacity planning", "WIP warehouse". Covers BOM
  setup, work orders, job cards, routing, and subcontracting for Indian
  manufacturers.
---

# ERPNext Manufacturing

The BOM is the foundation. Get the BOM wrong and every work order, every cost
calculation, and every material requirement is wrong.

## Prerequisites
Items created (raw materials, WIP items, finished goods), warehouses set up
(Raw Material Store, WIP, Finished Goods, Rejection/Scrap), CoA includes WIP
Account and COGS Account (`erpnext-stock`).

## Key decisions - confirm before configuring

- Use job cards? (shop-floor time tracking per operation per worker - adds process overhead but gives costing data)
- WIP warehouse separate? (Yes for manufacturing; No for simple assembly)
- Subcontracting? (send raw material to vendor, receive finished goods)
- Multi-level BOM? (sub-assemblies that are themselves produced - increases complexity)
- Backflush method: BOM (theoretical consumption) or Material Transferred (actual consumption)?

## Configuration sequence

**1. Manufacturing Settings**
Manufacturing → Settings → Manufacturing Settings:
- Default WIP Warehouse: the work-in-progress store.
- Default Finished Goods Warehouse: where completed production goes.
- Backflush Raw Materials Based On: "BOM" (simpler, use theoretical qty) or
  "Material Transferred for Manufacture" (use what was actually issued - more accurate).
- Job Cards Required: Yes if tracking actual time per operation.
- Allow Overtime: Yes if workers can log more than standard hours.

**2. Workstations**
Manufacturing → Workstation. One record per machine or work centre.
Fields: Workstation Name, Workstation Type, Working Hours per day (for capacity),
Hour Rate (labour/machine cost in ₹/hr - used for work order costing).
Link to a Holiday List for capacity planning.

**3. Operations**
Manufacturing → Operation. One per production step (Cutting, Welding, Painting,
Assembly, QC). Set default Workstation and standard time (in minutes).

**4. Routing**
Manufacturing → Routing. A reusable sequence of Operations. One routing per
product family. Assign to multiple BOMs. Saves re-entering operations on every BOM.

**5. Bill of Materials (BOM)**
Manufacturing → BOM. One BOM per finished product (or per variant).

Key fields:
- BOM Item: the finished good.
- Quantity: the batch size this BOM produces (e.g., BOM for 100 units).
- Is Active: Yes. Is Default: Yes (only one default BOM per item).
- Raw Materials table: Item, Qty (per batch qty above), UOM, Source Warehouse.
  Rate auto-pulled from item's valuation rate.
- Scrap Items: expected wastage items and their qty (posted to Scrap/Rejection Warehouse).
- Operations table (if using Routing): pull from Routing or add directly.
  Each operation has: workstation, time in mins, operating cost.

Submit the BOM. Review the costing section - it shows raw material cost +
operating cost = total production cost per unit.

**6. Work Order**
Manufacturing → Work Order. Created from BOM or Production Plan.
Fields: Item (finished good), BOM, Qty to Manufacture, Planned Start Date,
WIP Warehouse, Target Warehouse (Finished Goods).
Status flow: Draft → Submitted → In Process → Completed.
Submit to generate material requirements.

**7. Material Transfer for Manufacture**
Stock → Stock Entry → Material Transfer for Manufacture.
Created from Work Order → "Transfer Raw Materials" button.
Moves items from Raw Material Store to WIP Warehouse.
Qty pulled from BOM × work order qty (or actual if backflush = Material Transferred).

**8. Job Cards**
Auto-created per operation per work order (if Job Cards Required = Yes).
Worker opens the job card, logs: actual start time, end time, completed qty.
Submit job card to mark operation complete.
Incomplete job cards block work order completion.

**9. Manufacture Entry (Finish Production)**
Stock → Stock Entry → Manufacture.
Created from Work Order → "Finish Production" button.
Records: finished goods into Finished Goods Warehouse, raw material consumption
(from BOM or actual), scrap into Rejection Warehouse.
Submit → stock updated, GL posted.

**10. Subcontracting**
Buying → Subcontracting Order. Link to BOM. Specify: service item (the vendor's
service charge), raw materials to send, finished goods to receive.
Stock Entry → Send to Subcontractor: moves raw materials to the vendor's "virtual"
warehouse (a Supplier Warehouse in ERPNext).
Subcontracting Receipt: records finished goods received, raw material consumption,
and the vendor's invoice for the service charge.

**11. Production Plan (MRP)**
Manufacturing → Production Plan.
Input: Sales Orders (what is demanded) or Material Requests.
Output: planned Work Orders + Material Requests for raw material procurement.
Run monthly or weekly to keep production and procurement aligned.

## Fit-gaps

| Vanilla ERPNext | What's missing | Solution |
| --- | --- | --- |
| Basic capacity planning (hours per workstation) | Machine-level scheduling, Gantt drag-drop | Third-party scheduling tool or Frappe Manufacturing Suite |
| Theoretical yield from BOM | Actual vs theoretical yield variance report | Custom Script Report on Stock Entry |
| Desktop job card update | Shop-floor tablet/mobile app for workers | Custom portal or Frappe Manufacturing Suite |
| No IoT integration | Real-time machine data to ERPNext | Custom webhook bridge from machine PLC/SCADA |

## Common pitfalls

| Pitfall | Fix |
| --- | --- |
| BOM not marked as default → Work Order won't auto-pick BOM | Set "Is Default" = Yes on the active BOM after submission |
| WIP warehouse not set in Manufacturing Settings → Material Transfer fails | Set Default WIP Warehouse before creating first Work Order |
| Scrap not in BOM → actual scrap has nowhere to post | Add expected scrap items to BOM; actual scrap goes to Rejection/Scrap Warehouse |
| Backflush = BOM but actual consumption differs → wrong costing | Switch to "Material Transferred for Manufacture" for accurate actual costing |
| Job cards not submitted → Work Order stuck "In Process" | Train workers to submit job cards; add a daily check by the production supervisor |

## Definition of Done
- Workstations and operations created; routing defined for main product families.
- BOMs created, submitted, and marked as default for all finished goods.
- Full test cycle: Work Order → Material Transfer → Job Cards → Manufacture Entry → stock updated.
- Production costing verified on the manufacture entry (raw material + operating cost).
- Subcontracting tested end-to-end (if applicable).
- Production Plan run for a sample set of Sales Orders.

## Related Skills
`erpnext-stock`, `erpnext-buying`, `erpnext-accounts-gst`
