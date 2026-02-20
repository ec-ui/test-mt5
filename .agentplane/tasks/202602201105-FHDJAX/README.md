---
id: "202602201105-FHDJAX"
title: "Build interactive ASK/BID tick chart utility"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags:
  - "code"
verify: []
plan_approval:
  state: "approved"
  updated_at: "2026-02-20T11:06:55.471Z"
  updated_by: "ORCHESTRATOR"
  note: "Approved implementation scope and verification contract."
verification:
  state: "ok"
  updated_at: "2026-02-20T11:10:58.636Z"
  updated_by: "CODER"
  note: "CLI checks passed: --help works; chart generation succeeded on EURUSD_202601020000_202601291513.csv (2,226,151 rows parsed). Manual browser validation of pan/zoom and legend toggle is pending user-side visual check."
commit: null
comments:
  -
    author: "CODER"
    body: "Start: Implement MT5 tick parser and interactive Plotly ASK/BID chart utility with documented usage and verification."
events:
  -
    type: "status"
    at: "2026-02-20T11:07:06.316Z"
    author: "CODER"
    from: "TODO"
    to: "DOING"
    note: "Start: Implement MT5 tick parser and interactive Plotly ASK/BID chart utility with documented usage and verification."
  -
    type: "verify"
    at: "2026-02-20T11:10:58.636Z"
    author: "CODER"
    state: "ok"
    note: "CLI checks passed: --help works; chart generation succeeded on EURUSD_202601020000_202601291513.csv (2,226,151 rows parsed). Manual browser validation of pan/zoom and legend toggle is pending user-side visual check."
doc_version: 2
doc_updated_at: "2026-02-20T11:11:09.936Z"
doc_updated_by: "CODER"
description: "Create a Python utility that reads MT5 tick CSV/TSV format and builds an interactive ASK/BID chart with zoom, pan, and per-series toggle."
id_source: "generated"
---
## Summary

Build a Python CLI utility that reads MT5 tick export format and generates an interactive ASK/BID chart as HTML.

## Scope

In scope: add Python script to parse MT5 tick TSV/CSV format and generate interactive ASK/BID chart; update README usage. Out of scope: data modification, strategy analytics, external services.

## Plan

1. Inspect sample tick format and delimiter handling.\n2. Implement Python CLI parser for DATE+TIME with independent BID/ASK series accumulation.\n3. Build interactive Plotly chart with two traces, pan/zoom tools, and legend-based toggling.\n4. Export chart to HTML and print summary metrics.\n5. Update README usage and dependency details.\n6. Run verify commands and record results.

## Risks

Large tick files can create heavy HTML and high browser memory usage. Missing/partial BID/ASK rows may affect visual continuity. Mitigation: stream parse and keep independent series arrays; document optional row limit/downsampling.

## Verify Steps

1) python plot_ticks.py --help (prints usage)\n2) python plot_ticks.py --input EURUSD_202601020000_202601291513.csv --output eurusd_ticks.html (generates HTML without errors)\n3) Open eurusd_ticks.html and confirm zoom/pan tools work and ASK/BID can be toggled independently from legend.

## Verification

### Plan

### Results

<!-- BEGIN VERIFICATION RESULTS -->
#### 2026-02-20T11:10:58.636Z — VERIFY — ok

By: CODER

Note: CLI checks passed: --help works; chart generation succeeded on EURUSD_202601020000_202601291513.csv (2,226,151 rows parsed). Manual browser validation of pan/zoom and legend toggle is pending user-side visual check.

VerifyStepsRef: doc_version=2, doc_updated_at=2026-02-20T11:07:06.316Z, excerpt_hash=sha256:ea2bd27762acd1b41ad4364a67ba964ad828a680e00f6585d8c59e8cbf3c5cb6

<!-- END VERIFICATION RESULTS -->

## Rollback Plan

If verification fails, remove added script and README edits, then rerun verification baseline. If needed, revert task commit via agentplane-integrated workflow and mark task rework with failure reason.

## Notes

### Approvals / Overrides\nNo overrides requested.\n\n### Decisions\nImplemented standalone HTML generation with Plotly CDN to avoid Python plotting dependencies in runtime environment.\n\n### Implementation Notes\nAdded plot_ticks.py with MT5 tick parser, optional downsampling, and interactive ASK/BID chart export. Updated README.md with usage and behavior notes.\n\n### Evidence / Links\nVerification command recorded via agentplane verify: help output OK; HTML generation OK on provided EURUSD file.
