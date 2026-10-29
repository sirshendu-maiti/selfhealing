# GitHub repository setup and branch protection

The current GitHub connection exposes repository read/write operations for existing repositories but does not expose repository creation, project-board creation, or branch-protection/ruleset mutation. These steps therefore need to be applied in GitHub UI or by an administrator with an appropriately scoped token.

## Repository defaults
- Name: `ai-self-healing-ui-automation`
- Description: `AI-powered self-healing UI automation framework using Playwright, Pydantic and similarity scoring`
- Visibility: Private while in early development; change to public only after reviewing demo credentials, secrets, license, and documentation.
- Default branch: `main`
- Add `.gitignore`, `LICENSE` (choose before release), and this README before inviting collaborators.

## Protect `main`
GitHub → Settings → Rules → Rulesets (or Branches → Add branch protection rule):
1. Target branch: `main`.
2. Require a pull request before merging; require 1 approval.
3. Dismiss stale approvals when new commits are pushed.
4. Require conversation resolution.
5. Require status checks: `pytest` and `ruff` after the workflow names are stable.
6. Require branches to be up to date before merging (optional if it causes excessive queueing).
7. Block force pushes and branch deletion.
8. Restrict bypass to a small administrator set; do not allow routine bypass.
9. CODEOWNERS should require Integration Lead + Track A review for `src/selfheal/models/**`.

## Phase 1 project board
Create a GitHub Project (board view) with Backlog, Ready, In progress, In review, Done. Add the issues listed in `PHASE1_BOARD.md`, labels `phase:1`, `track:A`–`track:D`, `integration`, and priorities `P0`–`P2`.
