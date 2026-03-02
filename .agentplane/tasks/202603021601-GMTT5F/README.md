---
id: "202603021601-GMTT5F"
title: "Use trading days in funding yield formula"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags:
  - "code"
verify: []
plan_approval:
  state: "approved"
  updated_at: "2026-03-02T16:02:30.858Z"
  updated_by: "ORCHESTRATOR"
  note: "Plan approved by user on 2026-03-02."
verification:
  state: "pending"
  updated_at: null
  updated_by: null
  note: null
commit: null
comments:
  -
    author: "CODER"
    body: "Start: Updating annualization factor to trading days per year."
events:
  -
    type: "status"
    at: "2026-03-02T16:02:36.387Z"
    author: "CODER"
    from: "TODO"
    to: "DOING"
    note: "Start: Updating annualization factor to trading days per year."
doc_version: 2
doc_updated_at: "2026-03-02T16:02:59.959Z"
doc_updated_by: "CODER"
description: "Replace the 365-day factor with trading days per year in the funding yield calculation."
id_source: "generated"
---
## Summary

Update the funding yield formula to use trading days per year instead of 365. Success is the new factor applied consistently without breaking output generation.

## Scope

In-scope: update formula constant in plot_funding_yield.py. Out-of-scope: calendar holiday logic or other calculations.

## Plan

1. Replace the annualization factor in plot_funding_yield.py with trading days per year (default 252).\n2. Update any related labels or comments if needed.\n3. Run the script to ensure output is generated.

## Risks

Using a fixed trading-days factor may not match a specific exchange calendar; verify the desired constant if needed.

## Verify Steps

1. Run: python plot_funding_yield.py.\n2. Confirm the script prints output and the generated HTML reflects the updated annualization factor (252).

## Verification

### Plan

### Results

<!-- BEGIN VERIFICATION RESULTS -->
<!-- END VERIFICATION RESULTS -->

## Rollback Plan

Revert plot_funding_yield.py to restore the prior factor if needed.

## Context

User requested replacing 365 with the number of working (trading) days per year in the annualized funding yield formula.

## Notes

### Approvals / Overrides\n- None.\n\n### Decisions\n- Use 252 trading days per year for annualization.\n\n### Implementation Notes\n- Added TRADING_DAYS_PER_YEAR constant and updated formula.\n\n### Evidence / Links\n- Local run: python plot_funding_yield.py.
