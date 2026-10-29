# Phase 1 ownership proposal

No team roster or GitHub usernames were supplied, so tracks are assigned by workstream, not to named individuals. Integration lead is a role placeholder until a person is nominated.

| Owner | Track | Scope | Deliverables | Dependencies |
|---|---|---|---|---|
| Track A — Framework/Core | Automation engine and public API | Playwright wrapper, baseline capture/read, typed interfaces, package layout | Engine skeleton, contract tests, public API notes | Interface contract ratification |
| Track B — Scoring/Healing | DOM scan and candidate scoring | Fingerprints, candidate extraction, feature normalization, score calibration, ambiguity policy | 20-pair scorer spike, benchmark harness, decision rules | Contract + demo DOM |
| Track C — Demo/Test | Demo app and test fixtures | Login page, controlled DOM variants, positive/negative flows, Playwright tests | Demo app v1, reproducible scenarios | None; supplies test target to A/B |
| Track D — Data/Reporting/CI | Persistence and observability | SQLite schema, event log format, report skeleton, lint/test CI | schema draft, CI workflow, report format | Contract + event schema |
| Integration Lead — TBD | Architecture and release coordination | Own interface decisions, integration PRs, weekly demo, conflict resolution, release checklist | Integration branch, contract sign-off, phase exit report | All tracks |

## Working agreements
- One issue per independently testable deliverable; PRs target `main` and require at least one reviewer.
- `main` is protected; no direct pushes or force pushes.
- Changes to `src/selfheal/models/contract.py` require approval from the Integration Lead and one track owner.
- Any score-threshold change must include benchmark output and false-positive analysis.
- Do not automatically commit healed selectors to baseline in Phase 1.
