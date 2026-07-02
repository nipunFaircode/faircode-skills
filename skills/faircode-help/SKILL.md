---
name: faircode-help
description: >-
  Use when the user types /faircode-help, asks "what faircode skills are
  available", or is new to this plugin and needs an entry point. Lists every
  faircode-* skill and hands off to faircode-delivery for phase-based routing.
---

# Faircode Help

This is the front door for the Faircode Frappe skill suite. It does one
thing: tell you what's installed and where to go next.

## Installed skills (v0.1 pilot)

- `faircode-delivery` — orchestrator; routes to the right skill for the
  current project phase. Start here for anything phase-specific.
- `faircode-requirements-discovery` — structured requirements interviews.
- `faircode-task-breakdown` — decompose a blueprint into ERPNext tasks with
  acceptance criteria.
- `faircode-frappe-development` — write code the Frappe way.
- `faircode-test-driven-development` — TDD workflow for Frappe/ERPNext.
- `faircode-cicd-guardrails` — GitHub/GitLab CI guard-rails before merge.

## What to do next

- Starting or picking up delivery work → invoke `faircode-delivery`.
- Just want the list again → invoke `faircode-help`.

> Pilot note: only the six skills above ship in v0.1. If `faircode-delivery`
> references a skill not in this list, it isn't installed yet — fall back to
> the closest available skill and say so.
