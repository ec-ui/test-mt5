---
id: "202602261000-XSP60E"
title: "Build funding yield plotter for GAZPF CSV"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags:
  - "code"
verify: []
plan_approval:
  state: "approved"
  updated_at: "2026-02-26T10:01:07.652Z"
  updated_by: "ORCHESTRATOR"
  note: "Plan approved by user on 2026-02-26."
verification:
  state: "pending"
  updated_at: null
  updated_by: null
  note: null
commit: null
comments:
  -
    author: "CODER"
    body: "Start: Implementing CSV parser, yield calc, and interactive Plotly chart per spec."
events:
  -
    type: "status"
    at: "2026-02-26T10:01:12.135Z"
    author: "CODER"
    from: "TODO"
    to: "DOING"
    note: "Start: Implementing CSV parser, yield calc, and interactive Plotly chart per spec."
doc_version: 2
doc_updated_at: "2026-02-26T10:02:22.811Z"
doc_updated_by: "CODER"
description: "Create a Python utility to read the GAZPF contract results CSV, compute annualized funding yield (SWAPRATE/CLOSE * 365 * 100) with weekends forced to zero, and generate an interactive plot."
id_source: "generated"
---
## Summary

Implement a Python utility that reads the GAZPF contract results CSV, computes annualized funding yield from SWAPRATE and CLOSE, and produces an interactive HTML plot. Success is an HTML chart that loads interactively and reflects zero yield on weekends.

## Scope

In-scope: contractresults-GAZPF-25022025-25022026.csv; new Python script to compute yield and generate an interactive HTML plot; minimal README update if needed. Out-of-scope: installing dependencies or modifying unrelated utilities.

## Plan

1. Inspect the CSV format and confirm required columns and separators.\n2. Implement a Python script to parse the CSV (skip header markers), convert decimal commas, parse dates, and compute annualized funding yield = (SWAPRATE / CLOSE) * 365 * 100 with weekends forced to zero.\n3. Build an interactive Plotly line chart and save it to an HTML file.\n4. Add brief run instructions if needed.

## Risks

CSV parsing may fail if format deviates (extra lines, different delimiter, decimal point instead of comma). Weekend detection must be correct for the locale calendar. Interactive plot requires Plotly availability in the environment.

## Verify Steps

1. Run: python plot_funding_yield.py\n2. Confirm it generates an HTML file (e.g., gazpf_funding_yield.html).\n3. Open the HTML and verify the plot is interactive (zoom/pan) and weekend dates show zero yield.

## Verification

### Plan

### Results

<!-- BEGIN VERIFICATION RESULTS -->
<!-- END VERIFICATION RESULTS -->

## Rollback Plan

Delete the new script and any README changes added for this task; remove the generated HTML if committed.

## Context

User requested a Python tool for the provided GAZPF CSV format (semicolon-delimited, decimal comma) to calculate annualized funding yield in percent and plot it interactively. Funding must be forced to zero on weekends.

## Notes

### Approvals / Overrides\n- None.\n\n### Decisions\n- Use Plotly (CDN) to provide an interactive HTML chart without Python plotting deps.\n\n### Implementation Notes\n- Added plot_funding_yield.py for CSV parsing, annualized yield calculation, and HTML chart output.\n\n### Evidence / Links\n- Local run: python plot_funding_yield.py -> gazpf_funding_yield.html.
