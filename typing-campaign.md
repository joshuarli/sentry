# Sentry typing hillclimb

## Status: active 2026-10-29 — resumed per owner "dont stop". Slice 1-5 committed on `typing-hillclimb` (test `def f() -> None`, grouptype parent-exact, HealthData stats narrowed, artifact index params, backup opaque rel models); exact `evaluate` vs `4f75fa69` running in background under `.work/tmp/evaluate-*`. Next: work evaluate punchlist, then precision long tail file-by-file until `complete`.
Resume prompt: "Resume the typing campaign from typing-campaign.md Status."
First command: `git status --short --branch` on `typing-hillclimb` (expect clean), then reread Status + Doctrine + Final measurement below.
Last revision: code `19a3c9627d6` (plus docs-only commits to this pause). Integration branch is NOT green: exact `evaluate` vs parent `4f75fa69` rejects with 59 reasons (53 precision + 5 Any + 1 all-strong); hard rows itemized in Final measurement.
Parked: 198 pre-rebase sideline branches (p3/p4/p5/lane/accel/wave/winddown families) — none merged; merging any of them would revert the Oct 28 rebase onto `upstream/master 625814f`. Their patch-novel commits are cataloged by the inventory script below; carve per-branch PRs at resume time. Kept as restore points: acceptance parent `typing-campaign-baseline-20261029`, pre-rebase backups `typing-hillclimb-backup-20261027` / `-20261029`.
Next slice: 1) tests `def f() -> None` (nested bare def, all-strong); 2) grouptype full revert to parent-exact; 3) release L69: audit `HealthData.stats` consumers, then narrow stats or split the return contract; 4) releasefile: annotate `initial_artifact_count` + `update_files` param (same-line), re-probe L405 with evaluator profile flags; 5) backup: opaque `rel_model` annotations (not casts) + non-generic isinstance construct; 6) precision long tail file-by-file until `complete`.

## Behavioral changes (complete log — every runtime-visible change the campaign made)
- `src/sentry/notifications/notification_action/grouptype.py`: `platform=project.platform or "javascript"` (NEW default when platform is None; parent passed None through). Unresolved: keep as bug-fix default (`load_data` requires `str`) or full-revert to bare (restores parent anchor, may clear the L60 row).
- `src/sentry/api/serializers/models/release.py` stats: `{str(k): v ...}` rebuilds the mapping (copy, `str` keys) instead of embedding the parent alias. Value-equal on str keys; pinned `or {}` default preserved; tests green. Keep, disclosed.
- `src/sentry/models/releasefile.py`: `assert index_data is not None` on the create=True path (AttributeError becomes AssertionError in the unreachable-None case). Alternative with zero runtime effect: `cast`. Unresolved — pick one post-resume.
- `tests/sentry/models/test_releasefile.py`: 2× `assert data is not None` (pre-existing Oct-27 wave) plus precise `_create_update_fn` / `writable_data` annotations (annotation-only, no runtime effect).
- `src/sentry/api/endpoints/source_map_debug.py`: `sourcemap_bytes` split off `sourcemap_header` + `None` init (fixed the UnboundLocalError the rename introduced; behavior equals parent; 61 tests green).
- `src/sentry/integrations/msteams/client.py`: `resp["id"]` indexed so a missing id raises KeyError (Oct 27, intentional contract fix + regression tests in `test_client.py`).
- `src/sentry/options/store.py`: init assertion saga (Oct 27: removed in `870ac8cea05`, restored per corrective defect 1 in `00910daf893`; `test_simple_without_cache` pins it).

## Doctrine (Any-debt rules — required for correct resume)
- The evaluator counts every new `Any` as debt: new `Any`-annotated signatures, `dict[str, Any]`, `type: ignore`, and `cast` to `Any`/`object` all reject; untyped code is neutral and precise typing earns credit.
- Casts do NOT remove inner `Any` (verified repeatedly): fix at the source (type the producer), never at the use site. Opaque annotations (`x: T = <Any-expr>`) do count as fixes; casts do not.
- One annotated binding per name per function scope (no-redef); `object` only for genuinely opaque unconsumed values; `Mapping[str, object]` for serializer `attrs` in strict files.
- `or {}` / `or 0` None-coercion behavior is pinned by tests — type around it, never drop it.
- Evaluator rows key (path, code, line, message) for diagnostics but (path, anchor, scope) for Any: line-adding edits rename surviving precision rows into new reasons, so keep edits line-count-neutral where rows survive. Any anchors embed inferred types, so whole-program drift (e.g. weaklist graduations) can flag byte-identical files — verify with `git diff <baseline> HEAD -- <file>` plus report anchors before assuming a local cause.

## Final measurement
- Acceptance parent: `4f75fa694441` = `upstream/master 625814f` + 4 evaluator policy files + 7 owner-owned files at preserved wip (mirrors the old `41a0d23` contract). Previous `41a0d23`-based reports are stale.
- Report progression vs new parent: 299 (b) → 204 (c) → 135 (d) → 94 (e) → 70 (f) → 63 (g) → 60 (h) → 59 (i). Zero weak/omission/configured/bypass/regression rows since (d).
- Report-i (candidate `1c4265f4`, code `19a3c9627d6`): 53 precision + 5 Any + 1 all-strong. Hard rows: `release.py` L69 `explicit` (the `-> HealthData | None` annotation references `HealthData.stats: dict[str, Any]`); `backup/dependencies.py` L454×2 `special_form` + L447 precision (byte-identical to parent — whole-program drift, see Doctrine); `releasefile.py` L405 `from_error` (not reproduced under ad-hoc strict flags — needs evaluator-profile repro, suspects: bare `update_files(files: dict)` + bare `initial_artifact_count` + decorated-generator type at L269/270); `grouptype.py` L60 `unannotated` (anchor changed by the local `or "javascript"` edit); `test_releasefile.py` L205 `no-untyped-def` (nested bare `def f()`).
- Precision long tail (~50 rows, ~30 files; largest: `seer/agent/tools` 19, `organization_details` 17, `test_committers` 16, `activity` 14, `test_release` 13, `groupactionlogentry` 12) is pre-existing wave debt, worked file-by-file after the hard rows.
- Rerun (background, ~25 min, `SENTRY_LOG_LEVEL=WARNING` required — an `options_store` INFO log otherwise leaks into mypy stdout and invalidates measurement; do not poll): `SENTRY_LOG_LEVEL=WARNING .venv/bin/python -m tools.mypy_helpers.typing_campaign evaluate --parent 4f75fa6944416e6c19b3ecda5af8e2b96d650117 --candidate-tree 'HEAD^{tree}' --output .work/evaluate-<DATE>`.

## Toolchain (condensed)
- All Python commands run in the venv: `.venv/bin/pytest`, `.venv/bin/python -m mypy`. Targeted mypy is necessary but NOT sufficient — only exact `evaluate` decides.
- Gate per file: `SENTRY_LOG_LEVEL=WARNING .venv/bin/python -m mypy <files>` clean + `ruff check --select F401,F821,F841` clean + `ruff format --check` clean (read-only; never run formatters).
- Behavioral evidence per wave: run the narrowest relevant pytest suites green; never weaken a test to pass.
- Every full `evaluate` takes ~25 min in background; `SENTRY_LOG_LEVEL=WARNING` must be set. Do not poll — notification arrives on completion.

## Typing extension packages (django) — vendoring and patch status
There is no `ty` (Astral) in this repo — no binary, no config. The Python type-check stack is **mypy 2.1.0** with three Django-typing extension packages, all installed from PyPI (via the devinfra mirror, pinned in `uv.lock`) — **none are vendored**:
- `django-stubs 5.2.9` — mypy plugin `mypy_django_plugin.main` (registered in `[tool.mypy] plugins`, configured via `[tool.django-stubs]` with `django_settings_module = "sentry.conf.server_mypy"`).
- `djangorestframework-stubs 3.16.8` — DRF companion stubs.
- `django-stubs-ext` — runtime helpers (`StrOrPromise`, `WithAnnotations`, …).
- `mypy-extensions`, `typing-extensions`, `pydantic.mypy` (third plugin in the list).
History — they **were** vendored as forks and were un-vendored in Feb 2026: commit `5b0f2ad7fa4` ("ref(typing): Upgrade mypy to 1.19.1 and switch to upstream django-stubs (#107710)") replaced `sentry-forked-django-stubs` / `sentry-forked-djangorestframework-stubs` with upstream 5.2.9 / 3.16.8. Per that commit message, the forks had exactly one active patch — disabling `MetaclassAdjustments` that stripped `objects` / `DoesNotExist` / `MultipleObjectsReturned` from model classes — replaced by `strict_model_abstract_attrs = false` in `[tool.django-stubs]`. That commit states "The forked packages had no other active patches." No patches to these packages exist in-tree today (`patches/` holds only JS patches: css-tree, jest-resolve, jest-runtime, zrender).
Vendored typing surface that IS in-tree (campaign-relevant, actively maintained):
- `fixtures/stubs-for-mypy/*.pyi` (~30 hand-written stubs for third-party packages with missing/incorrect types; wired via `mypy_path`). Campaign-relevant entries: `rest_framework/response.pyi` (opt-in generic `Response[T]` with `data: T` overload at `__init__`, added in `7624998ab35` "Type @extend_schema responses via Response[T] stub + linter (#116335)"); `rest_framework/serializers.pyi` (vendors DRF serializers with one change — `BaseSerializer` takes a second type parameter for `validated_data`, added in `808dd671b3e` (#123923)).
- `tools/mypy_helpers/plugin.py` (`SentryMypyPlugin`): enforces required `using=` on ORM calls, `Response[T]` schema narrowing, and wires `serializer_autoderive.py`, which auto-derives `Serializer[T]` from typed `serialize()` returns with an exemption denylist (`CommitSerializer`, `EventSerializer`, `GroupSerializerBase`, `OrganizationMemberSerializer`, `ProjectSerializer`, `ReleaseSerializer`, `BaseTeamSerializer`, …). Maintenance pattern: denylist entries are removed as the campaign types each serializer (`3717ae8b8`, `88a5e3ef8c4`, `1cbf96fbab`).
Rule for the campaign: these extension packages and the vendored stubs/plugin are **policy-adjacent infrastructure** — do not modify them to silence debt (the evaluator guards its own `tools/mypy_helpers/typing_campaign.py` policy set the same way). Type the call sites instead.

## Branch inventory (future upstream PRs)
Complete catalog of local branches as of 2026-10-29 (`typing-hillclimb @ 5fadd7d083d`; 200 branches). "Novel" = patch-id comparison with zero `+` lines meaning fully incorporated — `git cherry typing-hillclimb <branch>` (rebasing rewrites hashes, so counts use patch-ids, not commits; counts are an upper bound since rebase conflict resolutions also change patch-ids — review content at carve time). Regenerate any time with:
```bash
git branch --list | sed 's/^[* ] //' | while read b; do
  tip=$(git log -1 --format='%h|%ad|%s' --date=short "$b")
  nov=$(git cherry typing-hillclimb "$b" | grep -c '^+ ')
  echo "$b || $tip || novel=$nov"
done
# novel subjects for one branch: git cherry -v typing-hillclimb <branch>  # '+' lines are the PR slice
```
Family summary (novel = patch-novel commits vs hillclimb; tips Oct 20–24 except where noted):

| family | branches | patch-novel | role |
|---|---|---|---|
| `master` | 1 | 0 | upstream mirror (fork tracking upstream) |
| `typing-hillclimb` | 1 | 0 | main campaign line (current) |
| `typing-campaign-baseline-20261029` | 1 | 1 | acceptance parent for exact evaluate (keep) |
| `typing-hillclimb-backup-2026102[78]` | 2 | 21 | pre-rebase restore points (keep) |
| `typing-hillclimb-resume-20261022`, `-p10-…`, `typing-current-master-baseline-20261022` | 3 | 19 | old Oct-22 campaign states (keep until PRs land) |
| `typing-loop-speed*` | 2 | 10 | loop-speed experiments (keep until PRs land) |
| `p3-*` | 21 | 98 | phase-3 promotion snapshots; tips name the deliverable (keep until PRs land) |
| `p4-*` | 50 | 259 | phase-4 endpoint/serializer slices; tips name the deliverable (keep until PRs land) |
| `p5-*` | 3 | 13 | phase-5 containment/precision/guard slices (keep until PRs land) |
| `typing-p[3,4,6,7,8]-*`, `typing/p3-grouping-actions` | 6 | 38 | misc per-area waves (keep until PRs land) |
| `typing-lane-*` | 59 | 649 | per-area work lanes (keep until PRs land) |
| `typing-accel-*` | 15 | 157 | accel campaign lanes (keep until PRs land) |
| `typing-wave-*` | 9 | 98 | wave coordinations (keep until PRs land) |
| `typing-winddown-*` | 26 | 294 | prior winddown parks (keep until PRs land) |
| `typing-next-*` | 1 | 12 | next-slice staging (keep until PRs land) |

No branch was merged during this winddown (merging any sideline would revert the Oct 28 rebase onto `upstream/master 625814f`); nothing was deleted. To retire a branch later, prove integration first (`git merge-base --is-ancestor <branch> typing-hillclimb`, else patch-equivalence with no `+` lines via `git cherry`), then remove per the orchestrate worktree lifecycle.

## Resume
First commands on `typing-hillclimb`: `git status --short --branch` (expect clean), `git log --oneline -3`, reread Status + Doctrine + Final measurement above. Then work the Next slice in Status order, one commit per fix, with targeted mypy + ruff + narrowest pytest evidence per fix; launch exact `evaluate` (Final measurement) when a wave is ready and work its punchlist until `complete`.
