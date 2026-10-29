# 🛡️ AI-Powered Self-Healing UI Automation Framework

> **Phase 1** — Scoring engine, contract models, and demo app scaffold

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![Playwright](https://img.shields.io/badge/Playwright-1.44%2B-45BA4B?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Scoring Algorithm](#scoring-algorithm)
- [Demo Application](#demo-application)
- [Running Tests](#running-tests)
- [Phase 1 Scope & Roadmap](#phase-1-scope--roadmap)
- [Safety Boundary](#safety-boundary)
- [Contributing](#contributing)

---

## Overview

When web UI elements change — renamed IDs, modified CSS classes, shifted layouts — automated tests break. This framework solves that by **automatically identifying the most likely matching element** on the current page using a weighted multi-feature similarity scoring algorithm.

Instead of hard-coded selectors that fail silently, the framework captures a rich **element fingerprint** (text, classes, attributes, position, ARIA role, parent context) and scores candidates against it, proposing a healed locator with a confidence score.

**Phase 1** establishes the foundational scoring engine, Pydantic data contracts, a benchmark suite, and a demo login page for testing.

---

## Key Features

- 🔍 **Weighted Similarity Scorer** — Six-feature scoring engine combining text, CSS classes, attributes, position, parent context, and ARIA roles
- 📐 **Pydantic v2 Contracts** — Strict, schema-versioned data models for element fingerprints, locator specs, and healing decisions
- 🧪 **Benchmark Suite** — 20 hand-authored labeled pairs with confusion matrix reporting
- 🖥️ **Demo Login App** — A polished, responsive login page with stable `data-testid` hooks for testing
- 🛡️ **Human-in-the-Loop** — Healing decisions default to requiring human review; no automatic clicking

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Test Runner                        │
│            (Playwright-based tests)                  │
└──────────────┬──────────────────────────┬────────────┘
               │  Locator fails?          │
               ▼                          │
┌──────────────────────────┐              │
│   Element Fingerprint    │              │
│   (stored snapshot)      │              │
└──────────────┬───────────┘              │
               │                          │
               ▼                          │
┌──────────────────────────┐     ┌────────┴─────────┐
│   Similarity Scorer      │────▶│ Healing Decision  │
│   (6 weighted features)  │     │ (candidate/accept/│
│                          │     │  reject/ambiguous) │
└──────────────────────────┘     └──────────────────┘
```

---

## Project Structure

```
selfhealing_phase1/
├── src/selfheal/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py          # Re-exports all contract models
│   │   └── contract.py          # Pydantic models: LocatorSpec, ElementFingerprint,
│   │                            #   ScoringWeights, HealingDecision
│   └── scorer/
│       ├── __init__.py
│       ├── scorer.py            # Core scoring engine (score_pair function)
│       └── spike.py             # 20-pair benchmark runner
│
├── tests/
│   ├── test_scorer.py           # Pytest tests for the scorer
│   └── fixtures/
│       └── scorer_pairs.json    # 20 labeled test pairs (10 same-target, 10 different)
│
├── demo_app/
│   ├── app.py                   # Flask app entry point
│   ├── index.html               # Static login page (v1)
│   ├── static/style.css         # Responsive CSS with gradients & animations
│   └── templates/login.html     # Jinja2 login template with data-testid hooks
│
├── docs/
│   ├── PHASE1_BOARD.md          # Task board with P0/P1 priorities
│   ├── TEAM_AND_TRACKS.md       # Team ownership across 4 tracks
│   ├── SCORER_SPIKE.md          # Spike documentation and caveats
│   ├── SCORER_SPIKE_RESULTS.txt # Confusion matrix output
│   └── BRANCH_PROTECTION.md     # Branch protection recommendations
│
├── .github/workflows/ci.yml    # CI pipeline
├── pyproject.toml               # Package config & dependencies
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- **Python 3.11+**
- **pip** (comes with Python)
- **Git**

### Installation (Windows PowerShell)

```powershell
# Clone the repository
git clone https://github.com/sirshendu-maiti/selfhealing-ui-automation.git
cd selfhealing-ui-automation

# Create and activate virtual environment
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install the package in development mode
python -m pip install -e ".[dev]"

# Install Playwright browsers (needed for UI automation)
python -m playwright install chromium
```

### Installation (macOS / Linux)

```bash
# Clone the repository
git clone https://github.com/sirshendu-maiti/selfhealing-ui-automation.git
cd selfhealing-ui-automation

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the package in development mode
pip install -e ".[dev]"

# Install Playwright browsers
python -m playwright install chromium
```

---

## Scoring Algorithm

The scorer computes a **weighted similarity score** (0.0–1.0) between an original element fingerprint and a candidate element using 6 features:

| Feature | Weight | Method |
|---------|--------|--------|
| **Text content** | 30% | `SequenceMatcher` ratio on normalized text |
| **CSS classes** | 20% | `SequenceMatcher` ratio on sorted, joined class lists |
| **Attributes** | 15% | Average per-key similarity across the union of attribute keys |
| **Position** | 15% | Linear decay: `1 − |Δ|/300px` per dimension (x, y, width, height) |
| **Parent context** | 10% | `SequenceMatcher` ratio on `parent_tag + parent_text` |
| **ARIA role** | 10% | `SequenceMatcher` ratio on role strings |

**Threshold:** 0.75 (inherited from project plan; requires calibration on real DOM captures)

### Running the Scorer Benchmark

```powershell
python -m selfheal.scorer.spike
```

**Sample output:**

```
Scorer spike: 20 hand-authored pairs | threshold=0.75
id   truth  score  predicted  note
P01  True   0.950  True       Exact text match, same classes
P02  True   0.873  True       Minor class rename
...

TP=10 FP=6 TN=4 FN=0
accuracy=0.700 precision=0.625 recall=1.000
```

---

## Demo Application

A responsive login page that serves as the test target for the automation framework.

### Start the demo server

```powershell
python -m http.server 5000 --directory demo_app
```

Open **http://127.0.0.1:5000** in your browser.

### Demo Credentials

| Field | Value |
|-------|-------|
| Email | `demo@example.com` |
| Password | `demo123` |

> **Note:** This is a front-end simulation only. No real authentication occurs. Do not enter real credentials.

The demo app includes stable `data-testid` attributes on all interactive elements:
- `login-form`, `email-input`, `password-input`, `login-submit`
- `login-success`, `login-error` (feedback alerts)

---

## Running Tests

```powershell
# Run the full test suite
pytest

# Run with verbose output
pytest -v

# Run a specific test
pytest tests/test_scorer.py -v
```

### Test Coverage

| Test | Description |
|------|-------------|
| `test_fixture_count` | Verifies exactly 20 fixture pairs exist |
| `test_scores_bounded` | All scores are within [0.0, 1.0] |
| `test_identical_element` | An identical element scores exactly 1.0 |

---

## Phase 1 Scope & Roadmap

### Current Phase (Phase 1) ✅

- [x] Pydantic v2 contract models (provisional)
- [x] Weighted element similarity scorer
- [x] 20-pair hand-authored benchmark
- [x] Demo login app with `data-testid` hooks
- [x] CI pipeline setup
- [x] Scorer spike with confusion matrix analysis

### Future Phases 🚧

- [ ] Tag-name equality enforcement
- [ ] Locator uniqueness validation
- [ ] Visibility and enabled-state checks
- [ ] Ambiguity margin analysis
- [ ] Action postcondition verification
- [ ] Real DOM capture calibration
- [ ] Threshold optimization on production data
- [ ] Full Playwright integration for automated healing

---

## Safety Boundary

> ⚠️ **The scorer proposes candidates only.** Do not automatically click or persist a healed locator based on score alone.

A production healing decision must also check:
- **Ambiguity margin** — gap between top candidate and runner-up
- **Visibility / enabled state** — element must be interactive
- **Uniqueness** — proposed locator must match exactly one element
- **Postcondition** — test-specific verification that the healed action produced the expected result

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

### Development Setup

```powershell
# Install with dev dependencies
pip install -e ".[dev]"

# Run linter
ruff check src/ tests/

# Run tests
pytest -v
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| Data Models | Pydantic v2 |
| String Matching | difflib (SequenceMatcher) |
| Fuzzy Matching | RapidFuzz |
| UI Automation | Playwright |
| Testing | Pytest |
| Linting | Ruff |
| CI | GitHub Actions |

---

<p align="center">
  <b>Built for reliable regression testing</b><br>
  <i>When interfaces change, your automation adapts with confidence.</i>
</p>
