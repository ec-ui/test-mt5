---
id: "202603021619-2S6YGJ"
title: "Add output section and screenshots to README"
status: "DOING"
priority: "med"
owner: "DOCS"
depends_on: []
tags:
  - "docs"
verify: []
plan_approval:
  state: "approved"
  updated_at: "2026-03-02T16:20:59.249Z"
  updated_by: "ORCHESTRATOR"
  note: "Plan approved by user on 2026-03-02 (PNG screenshots)."
verification:
  state: "pending"
  updated_at: null
  updated_by: null
  note: null
commit: null
comments:
  -
    author: "DOCS"
    body: "Start: Adding output section and PNG screenshots to README."
events:
  -
    type: "status"
    at: "2026-03-02T16:21:07.571Z"
    author: "DOCS"
    from: "TODO"
    to: "DOING"
    note: "Start: Adding output section and PNG screenshots to README."
doc_version: 2
doc_updated_at: "2026-03-02T16:30:23.474Z"
doc_updated_by: "DOCS"
description: "Add a README section describing output files and include PNG screenshots of the charts stored in the repository."
id_source: "generated"
---
## Summary

Add a README section for output files and include PNG screenshots of both charts stored in the repository. Success is documented outputs and visible images in README.

## Scope

In-scope: README.md updates and new PNG screenshots under images/. Out-of-scope: changing existing script behavior.

## Plan

1. Generate PNG screenshots of both charts using local data files.\n2. Add images/ directory and save PNGs there.\n3. Update README.md with a section describing output files and embed the screenshots.

## Risks

Generating PNGs requires installing plotting dependencies; ensure they are not committed and screenshots represent current script behavior.

## Verify Steps

1. Open README.md and confirm the output section and embedded images render.\n2. Verify images/ contains PNG files for both charts.

## Verification

### Plan

### Results

<!-- BEGIN VERIFICATION RESULTS -->
<!-- END VERIFICATION RESULTS -->

## Rollback Plan

Remove the added images and revert README.md changes.

## Context

User requested a separate README section about output files and to add chart screenshots as PNGs in the repository.

## Notes

### Approvals / Overrides\n- Network access approved by user on 2026-03-02 to install plotly/kaleido for PNG rendering.\n\n### Decisions\n- Store screenshots under images/ and embed them in README.\n\n### Implementation Notes\n- Added images/eurusd_ticks.png and images/gazpf_funding_yield.png.\n- Updated README.md with output section and embedded screenshots.\n\n### Evidence / Links\n- Generated screenshots from local CSV inputs using Plotly/Kaleido.
