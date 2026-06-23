---
name: erpnext-assets
description: >-
  Use when configuring the Assets module in ERPNext. Triggers on "fixed asset",
  "depreciation", "asset register", "asset movement", "asset disposal", "asset
  maintenance", "AMC", "asset category". Covers asset categories, depreciation
  schedules, physical verification, maintenance, and disposal for Indian
  companies.
---

# ERPNext Assets - Fixed Asset Management

Get the depreciation method and GL accounts right at setup. Changing them after
assets are live requires cancelling and re-creating all depreciation entries.

## Prerequisites
Chart of Accounts must include fixed asset accounts: Asset Account (under
Fixed Assets), Accumulated Depreciation (contra-asset), Depreciation Expense
(under Indirect Expenses), Capital Work in Progress (for assets under
construction). Fiscal Year configured.

## Key decisions - confirm with client's CA before configuring

**Depreciation method:**
- Straight Line (SLM): equal depreciation every period. Used under Companies Act (Schedule II rates).
- Written Down Value (WDV): higher depreciation early, lower later. Used under Income Tax Act.
- Many companies maintain two sets: SLM for books (Companies Act), WDV for tax (Income Tax). Vanilla ERPNext supports one method per asset - discuss with client's CA how they want to handle dual depreciation.

**Useful life:**
Defined by Schedule II of Companies Act 2013 by asset category. Examples:
- Buildings: 30-60 years (RCC frame 60 years).
- Plant & Machinery: 15 years.
- Computers and Peripherals: 3 years.
- Furniture: 10 years.
- Vehicles: 8 years.

## Configuration sequence

**1. Asset Category**
Assets → Asset Category. One per asset type.

| Field | Notes |
| --- | --- |
| Asset Category Name | Computers, Furniture, Vehicles, Plant & Machinery, Buildings |
| Depreciation Method | SLM or WDV (per CA's advice) |
| Total Number of Depreciations | Useful life × frequency (e.g., 3 years monthly = 36) |
| Frequency of Depreciation (months) | 1 = monthly (recommended), 12 = yearly |
| Asset Account | e.g., "Computers and Peripherals" under Fixed Assets |
| Accumulated Depreciation Account | e.g., "Accumulated Depreciation - Computers" |
| Depreciation Expense Account | e.g., "Depreciation - Computers" |
| Capital Work in Progress Account | Used when asset is under construction before commissioning |

**2. Asset master**
Assets → Asset. Required fields:
- Asset Name, Asset Category, Company, Purchase Date, Gross Purchase Amount.
- Location: the physical location (office, warehouse, site).
- Custodian: the employee responsible for the asset.
- Is Existing Asset: Yes for assets purchased before ERPNext go-live.
  For existing assets also set: Accumulated Depreciation (to date) and
  Next Depreciation Date (so ERPNext starts from the right point).

**3. Asset from Purchase Invoice**
For new asset purchases: create Purchase Invoice for the asset item.
On the item line, check "Is Fixed Asset". After submitting the PI,
ERPNext prompts to create the Asset record. Link the PI → Asset is created with
the purchase amount pre-filled. This avoids double-counting in CoA.

**4. Depreciation Schedule**
Auto-generated on Asset save based on category settings.
Review: Assets → Asset → Depreciation Schedules tab.
Check that total depreciation = gross purchase amount (for SLM; WDV approaches
but never reaches zero - set a write-off rule with client's CA).
Submit the Asset to activate depreciation.

**5. Monthly depreciation posting**
Accounts → Depreciation → Post Depreciation Entries.
Or runs automatically on the scheduled date via the Frappe scheduler.
Posts a Journal Entry: Dr Depreciation Expense / Cr Accumulated Depreciation.
Run this check monthly - if the scheduler missed a posting, run it manually.

**6. Asset Movement**
Assets → Asset Movement. Transfer asset between locations or change custodian.
Records an audit trail. No GL impact (physical movement only).
Use this before every physical asset verification.

**7. Asset Maintenance**
Assets → Asset Maintenance. Schedule recurring tasks per asset:
- Annual: insurance renewal, AMC renewal.
- 6-monthly: vehicle service, generator maintenance.
- Monthly: UPS battery check.
Assign to a maintenance team. Tracks completion status and cost.

**8. Asset Repair**
Assets → Asset Repair. Log ad-hoc repair costs.
Capitalise the repair (adds to asset value) or expense it - set via "Capitalize
Repair Cost" checkbox. Consult CA for the threshold (typically only capitalise
if repair extends the asset's useful life).

**9. Asset Disposal - Scrap**
Assets → Asset → "Scrap Asset" button.
Posts Journal Entry: Dr Accumulated Depreciation + Dr Loss on Disposal (or Cr
Gain on Disposal) / Cr Asset Account.
Post all pending depreciation before scrapping.

**10. Asset Disposal - Sale**
Assets → Asset → "Sell Asset" button. Link to Sales Invoice.
ERPNext calculates gain/loss automatically:
- If Sale Price > Net Book Value: Gain on Sale (income).
- If Sale Price < Net Book Value: Loss on Sale (expense).

**11. Physical verification**
No dedicated scanning tool in vanilla ERPNext. Process:
- Assets → Reports → Asset Register → export to Excel.
- Physically verify each asset against the list.
- Update Location and Custodian via Asset Movement for discrepancies.
- Scrap missing/lost assets after management approval.

## Fit-gaps

| Vanilla ERPNext | What's missing | Solution |
| --- | --- | --- |
| One depreciation method per asset | Dual depreciation (Companies Act + IT Act) | Custom Report for IT Act WDV depreciation alongside SLM books |
| No QR/barcode scanning | Mobile asset verification | Custom app or Snipe-IT integration |
| No insurance policy tracking | Renewal alerts, insurer details | Use Asset Maintenance for renewal reminders |
| No IT asset details | Hardware specs, OS, software licences | Separate ITAM tool (Snipe-IT, etc.) |

## Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Asset not linked to Purchase Invoice → double-counting | Always create Asset from PI; verify the PI's "Asset" field is populated |
| Monthly depreciation not posted → year-end GL rush | Schedule monthly run; verify via Trial Balance for depreciation account balance |
| Existing assets entered without accumulated depreciation | Set "Is Existing Asset" = Yes and enter accumulated depreciation to go-live date |
| Scrap/disposal without posting depreciation to date | Run Post Depreciation Entries up to the disposal date before scrapping |
| Custodian empty → no accountability | Mandatory custodian on every asset; update on every movement |

## Definition of Done
- Asset categories created with correct method, accounts, and useful life (CA verified).
- All existing assets entered with accumulated depreciation to go-live date.
- One monthly depreciation posting tested and GL entries verified.
- Asset Movement and Maintenance workflows demonstrated to client.
- Asset Register exported and reconciled with physical count.

## Related Skills
`erpnext-accounts-gst`, `erpnext-buying`
