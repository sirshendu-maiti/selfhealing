# Phase 1 task board (GitHub Projects-ready)

Suggested columns: **Backlog → Ready → In progress → In review → Done**. Priority labels: `P0`, `P1`, `P2`. Track labels: `track:A`, `track:B`, `track:C`, `track:D`, `integration`. Phase label: `phase:1`.

## P0 — start immediately
- [ ] **A1 — Ratify typed interface contract** (Track A + Integration): locate authoritative §6.0, compare it to `contract.py`, add JSON examples and schema compatibility tests. Blocked: uploaded PDF contains no §6.0 Pydantic model definitions.
- [ ] **C1 — Demo app v1 login page** (Track C): responsive login page, success/failure states, stable data-testid hooks; demo-only credentials.
- [ ] **B1 — Run 20-pair scorer spike** (Track B): execute `python -m selfheal.scorer.spike`, record confusion matrix, inspect false positives, do not tune only to maximize this small synthetic set.
- [ ] **I1 — Create repository and protect `main`** (Integration): create repository, enable PR review and status checks, prohibit force pushes/deletion.
- [ ] **I2 — Create Phase 1 GitHub Project** (Integration): create board, add columns and labels, link initial issues.

## P1 — architecture and test scaffolding
- [ ] **A2 — Define package/API boundaries** (Track A): sync Playwright integration first; document async support decision.
- [ ] **B2 — Specify candidate acceptance policy** (Track B): threshold + runner-up margin + uniqueness + visible/enabled checks + postcondition.
- [ ] **C2 — Add login positive/negative Playwright tests** (Track C): correct credentials, wrong credentials, required fields, mobile viewport.
- [ ] **D1 — Draft SQLite/event schema** (Track D): runs, test results, fingerprints, locator history, healing events, audit log.
- [ ] **D2 — Add CI workflow** (Track D): pytest + lint on Python 3.11/3.12; install Chromium for browser tests.

## Phase 1 exit criteria
- Contract version and owner signed off; unresolved model mismatch documented.
- Demo app launches locally and positive/negative login paths pass.
- 20 labeled pairs produce a reproducible score report; every false positive is manually reviewed.
- CI runs on pull requests; branch protection has required checks once first workflow is green.
- Team ownership and Integration Lead are mapped to real GitHub usernames.

## Contract status

**Not frozen:** the uploaded PDF has no Section 6.0 defining Pydantic models. `src/selfheal/models/contract.py` is a provisional draft only. Do not treat it as a signed interface contract until the authoritative Section 6.0 is supplied and reviewed.
