---
id: "202602261009-HWFRFE"
title: "Add console progress for funding yield CSV parse"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags:
  - "code"
verify: []
plan_approval:
  state: "approved"
  updated_at: "2026-02-26T10:10:05.679Z"
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
    body: "Start: Adding progress output to funding yield CSV parsing."
events:
  -
    type: "status"
    at: "2026-02-26T10:10:12.582Z"
    author: "CODER"
    from: "TODO"
    to: "DOING"
    note: "Start: Adding progress output to funding yield CSV parsing."
doc_version: 2
doc_updated_at: "2026-02-26T10:10:39.461Z"
doc_updated_by: "CODER"
description: "Add progress reporting to plot_funding_yield.py while reading the GAZPF CSV so users see parsing progress in the console."
id_source: "generated"
---
## Summary

Add console progress reporting to the funding yield CSV parser so long reads show percent and row counts. Success is visible progress output without changing computed results or output HTML.

## Scope

In-scope: plot_funding_yield.py progress reporting while reading CSV. Out-of-scope: changing calculation, chart output, or input format.

## Plan

1. Add file-size-based progress tracking to the CSV read loop.\n2. Throttle console updates to avoid excessive output.\n3. Confirm the script still outputs the HTML chart and prints a final summary.

## Risks

Progress tracking could be inaccurate if buffering hides file position; updates should be throttled to avoid performance hits.

## Verify Steps

1. Run: python plot_funding_yield.py.\n2. Observe console output showing progress percent and row count while parsing.\n3. Confirm HTML output is generated and script exits normally.

## Verification

### Plan

### Results

<!-- BEGIN VERIFICATION RESULTS -->
<!-- END VERIFICATION RESULTS -->

## Rollback Plan

Revert changes in plot_funding_yield.py to remove progress reporting.

## Context

User reported no visible progress during CSV parsing; add progress updates to improve UX for large files.

## Notes

### Approvals / Overrides\n- None.\n\n### Decisions\n- Track progress by file position and throttle updates to ~0.25s.\n\n### Implementation Notes\n- Added CSV parsing progress output in plot_funding_yield.py.\n\n### Evidence / Links\n- Local run: python plot_funding_yield.py (progress shown).
