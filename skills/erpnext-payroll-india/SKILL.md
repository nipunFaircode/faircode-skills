---
name: erpnext-payroll-india
description: >-
  Use when setting up HR and Payroll in ERPNext for an Indian company. Triggers
  on "payroll setup", "salary structure", "PF", "ESI", "professional tax",
  "TDS on salary", "Form 16", "payslip", "attendance", "leave". Covers employee
  master, statutory deductions, monthly payroll run, and India compliance.
---

# ERPNext Payroll - India

Get PF, ESI, and PT wrong and you expose the client to statutory penalties.
Verify every rate and threshold before the first payroll run.

## Prerequisites
Company, Department and Designation masters, HR Settings configured, bank
accounts set up in Company master (for payment advice).

## Current statutory rates (verify annually - rates change)
- PF employee: 12% of basic (capped at ₹1,800/month - ceiling wage ₹15,000/month).
- PF employer: 12% of basic (3.67% to EPF, 8.33% to EPS - handled by EPFO split, not ERPNext).
- ESI employee: 0.75% of gross (only if gross ≤ ₹21,000/month).
- ESI employer: 3.25% of gross (only if gross ≤ ₹21,000/month).
- Professional Tax: slab varies by state. Karnataka: ₹200/month for salary > ₹15,000. Maharashtra: different slabs. Verify from state notification.

## Configuration sequence

**1. HR Settings**
HR → Settings → HR Settings. Set: standard working hours (8), max working hours
per day (9), leave approval notification, payroll frequency (Monthly default).

**2. Employee master**
HR → Employee. Mandatory fields:
- Date of Birth, Date of Joining, Department, Designation, Gender.
- PAN (mandatory - without PAN, TDS deducted at 20% flat rate).
- Aadhaar Number.
- UAN (Universal Account Number for PF member; get from previous employer or EPFO portal).
- Bank Account: under Accounts tab - IFSC, account number (for payment advice export).
- Salary Mode: Bank / Cash / Cheque.

**3. Salary Components**
Payroll → Salary Component. Create all components before building structures.

Earnings:
- Basic: type Earning, formula-based (`base * 0.40`) or fixed amount.
- HRA: `basic * 0.40` (metro cities) or `basic * 0.20` (non-metro). Tax-exempt up to actual/formula limits.
- Special Allowance: balance after other components (`base - basic - hra - lta`).
- LTA: fixed or annual, partially tax-exempt.
- Medical Allowance: ₹15,000/year tax-exempt (pre-2018 regime; now taxable under new regime).

Deductions:
- PF Employee: `min(basic * 0.12, 1800)` - cap at ₹1,800.
- PF Employer: `min(basic * 0.12, 1800)` - shown in CTC, not deducted from salary.
- ESI Employee: condition `gross_pay <= 21000`, formula `gross_pay * 0.0075`.
- ESI Employer: condition `gross_pay <= 21000`, formula `gross_pay * 0.0325`.
- Professional Tax: use a Python formula with state-specific slabs or a fixed amount.
- Income Tax (TDS): calculated by projection formula in ERPNext based on declared investments.

**4. Salary Structure**
Payroll → Salary Structure. One structure per grade/band. Add all components.
Set "Is Active" = Yes. Check "Calculate Net Pay Based on Flexible Benefit" only
if using flexible benefit plan.

**5. Salary Structure Assignment**
Payroll → Salary Structure Assignment. Link employee, salary structure, base
amount (CTC or monthly gross depending on structure design). Set effective
from date (must be first day of the payroll period or earlier).

**6. Payroll Period**
Payroll → Payroll Period. Set fiscal year dates (1 Apr - 31 Mar). Used for
TDS projection calculation across the year.

**7. Income Tax (TDS on salary)**
Employees submit investment declarations (HRA receipts, 80C investments, 80D
health insurance). Enter in HR → Employee Tax Exemption Declaration.
ERPNext projects the annual taxable income and calculates monthly TDS
automatically in the salary slip. Verify the first payslip manually.

**8. Monthly Payroll Entry**
Payroll → Payroll Entry:
1. Select Company, Payroll Frequency (Monthly), Start Date, End Date, Cost Center.
2. Click "Get Employees" - verify list against active headcount.
3. "Create Salary Slips" - generates one slip per employee.
4. Review 3-5 slips manually for accuracy.
5. Submit Payroll Entry - posts GL entries (Salary Expense Dr / Salaries Payable Cr).
6. Create Payment Entry - Salaries Payable Dr / Bank Cr.

## Fit-gaps

| Vanilla ERPNext | What's missing | Solution |
| --- | --- | --- |
| No PF ECR file generation | Monthly PF filing on EPFO portal | Manual download from EPFO after getting gross data from ERPNext |
| No ESI return generation | Monthly ESI filing | Manual on ESIC portal |
| No PT challan generation | Monthly/quarterly PT payment | Manual on state portal |
| No Form 24Q / Form 16 | Quarterly TDS return and annual certificate | ClearTax, Gen TDS, or TRACES manual |
| Basic TDS projection | Doesn't auto-calculate HRA exemption or 80C optimisation | Manual adjustment by accounts team on HR → Employee Tax Exemption |

## Common pitfalls

| Pitfall | Fix |
| --- | --- |
| PF deducted on full salary above ₹15,000 | Cap PF formula: `min(basic * 0.12, 1800)` |
| ESI deduction continues after ₹21,000 | Add condition `gross_pay <= 21000` on ESI component; mid-year: deduction continues till end of contribution period |
| PT slab incorrect for the state | Verify from state government notification; review annually |
| No PAN on employee → 20% TDS flat | PAN mandatory before first payroll run |
| Salary slips created but not submitted | Drafts don't post to GL. Submit salary slips and payroll entry both. |
| Payroll entry for wrong date range | Once submitted, can't change. Cancel payroll entry, cancel all salary slips, recreate. |

## Definition of Done
- All employee masters complete: PAN, Aadhaar, UAN, bank account.
- Salary structures created, assigned; test payslip reviewed for correct statutory amounts.
- PF capped at ₹1,800; ESI condition verified; PT slab correct for state.
- Payroll Entry run for one test period; GL entries verified.
- Process walkthrough done with client HR team.

## Related Skills
`erpnext-accounts-gst`, `erpnext-stock`
