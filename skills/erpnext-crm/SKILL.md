---
name: erpnext-crm
description: >-
  Use when configuring the CRM module in ERPNext. Triggers on "lead", "CRM
  setup", "opportunity", "sales pipeline", "lead source", "sales funnel",
  "follow-up tracking", "lost reason", "sales stage". Covers lead-to-quotation
  flow, pipeline configuration, and sales activity tracking.
---

# ERPNext CRM - Lead to Quotation

CRM is only useful if the sales team actually uses it. Keep the setup simple - 
fewer stages, fewer mandatory fields. Add complexity only when the team has
adopted the basics.

## Prerequisites
Sales Persons created, Territory hierarchy set up, Customer Groups defined,
user accounts for the sales team. Selling module configured (`erpnext-selling`).

## Configuration sequence

**1. Lead Sources**
CRM → Lead Source. Create all acquisition channels:
Website Enquiry, WhatsApp, Referral, Trade Show, Cold Call, Google Ads,
LinkedIn, Indiamart, Email Campaign.
These appear in Lead reports and channel effectiveness analysis.

**2. Industry Types**
CRM → Industry Type. List the industries your customers operate in.
Used for segmentation. Examples: Manufacturing, Retail, Healthcare, Education,
FMCG, Pharma, Real Estate, IT Services.

**3. Opportunity Types**
CRM → Opportunity Type. Match to your service/product categories:
New ERPNext Implementation, Customisation, AMC, Upgrade, Training, Support Contract.

**4. Lost Reasons**
CRM → Lost Reason. Mandatory for every Closed Lost opportunity.
Examples: Price too high, Chose competitor (name), Project postponed,
No budget approved, Decision delayed, Poor product fit.
Without lost reasons you have no data to improve win rate.

**5. Sales Stages (on Opportunity)**
Standard stages in ERPNext Opportunity: Prospecting, Qualification, Needs
Analysis, Value Proposition, Perception Analysis, Identify Decision Makers,
Proposal/Price Quote, Negotiation/Review, Closed Won, Closed Lost.
You can customise via DocType Customisation → Opportunity → Sales Stage field
→ edit Options. Keep it to 5-6 stages for adoption.

**6. Lead creation**
CRM → Lead. Fields: Lead Name, Company Name, Source, Mobile, Email,
Industry, Territory, Lead Owner (assigned sales person), Status.
Status flow: Lead → Open → Replied → Opportunity → Converted → Do Not Contact.

**7. Lead → Opportunity conversion**
From Lead form: "Create Opportunity" button. Fill:
- Opportunity From: Lead (or Customer if existing customer).
- Opportunity Type, Sales Stage, Probability (% chance of winning).
- Expected Closing Date (mandatory - drives pipeline value calculation).
- Next Contact Date and Next Contact By.

**8. Activity logging**
From Opportunity timeline: log calls, meetings, emails as Comments or
use the Activity DocType. For incoming emails: configure IMAP on the outgoing
sales email account so incoming customer replies auto-attach to the opportunity
thread.

**9. Pipeline view**
CRM → Opportunities → Kanban View (group by Sales Stage).
Used in weekly sales reviews. Drag card to advance stage.
Filter by: sales person, territory, expected close month.

**10. Quotation from Opportunity**
Opportunity → "Make Quotation" button. Pulls customer/lead details and
opportunity type. Complete item table, verify tax template, set Valid Till date.
On win: close Opportunity as Won, Quotation converts to Sales Order.
On loss: close Opportunity as Lost, select Lost Reason (mandatory).

**11. CRM reports**
CRM → Reports:
- Lead Details: all leads with source, owner, status.
- Opportunity Summary: pipeline value by stage and owner.
- Sales Funnel: conversion rates between stages.
- Sales Person-wise Transaction Summary: quota tracking.

## Fit-gaps

| Vanilla ERPNext | What's missing | Solution |
| --- | --- | --- |
| IMAP email polling (5-15 min delay) | Real-time email sync | Zapier webhook or custom email processor |
| No WhatsApp/LinkedIn lead capture | Leads from messaging platforms | Meta Cloud API webhook → ERPNext whitelisted endpoint |
| No call recording | Phone call logging | Third-party CTI integration (Exotel, Ozonetel) |
| Basic probability-weighted forecast | Advanced sales forecasting | Custom Script Report or Metabase |

## Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Leads not assigned to a sales person → no follow-up | Enable auto-assign in CRM Settings or add validation: Lead Owner mandatory on save |
| Sales Stage not updated → pipeline report wrong | Weekly pipeline review: all open opportunities must have a stage and next contact date |
| Lost Reason skipped → no win/loss data | Make Lost Reason mandatory via DocType Customisation → Opportunity → Lost Reason → Mandatory |
| Duplicate leads from same contact | Check existing leads by email before creating; ERPNext validates email uniqueness on Lead |
| Quotation created without going through Lead/Opportunity | Sales training: all new business starts as Lead → Opportunity → Quotation |

## Definition of Done
- Lead sources, industry types, opportunity types, and lost reasons configured.
- Sales team user accounts linked to Sales Person masters.
- Territory hierarchy set and assigned to sales persons.
- Full test cycle: Lead → Opportunity → pipeline update → Quotation → Won and Lost.
- Lost Reason made mandatory on Opportunity.
- IMAP email integration configured and tested (if applicable).
- Pipeline Kanban view and funnel report demonstrated to sales team.

## Related Skills
`erpnext-selling`, `erpnext-accounts-gst`
