# Sentry typing hillclimb

## Status: acceptance complete; review and publication remain

The exact evaluator reported `complete` with zero reasons for candidate `9acb5860c21` against parent `66941a85b51`. Its `precision_complete` flag is false because it counts precision additions in test files. The accepted source tree remains unchanged on `origin/typing-hillclimb` at `4f5c9df6b5e`. The report was in `.work/tmp/evaluate-20261030-postrebase4/report.json` on the original computer and is not committed. The acceptance parent is not an ancestor of the campaign branch.

The branch review is incomplete. Do not treat acceptance as proof that the changes are ready to land. The export `origin/typing-hillclimb-upstream` is an older snapshot and has not been updated to the accepted tree. On 2026-10-31, `upstream/master` advanced from `c8f1ef5e` to `063a6cb279f`; the intervening commit changed three frontend files. Fetch again before publication.

The parked branches and acceptance parent are preserved on the fork under `origin/typing-campaign-parked/`, using their original local branch names after that prefix. Fetch the fork and recreate a local branch from the matching remote-tracking ref when needed. Do not merge the old sideline branches directly: they predate the final rebase. Compare and carve their changes onto a current base.

## Resume review and publication

1. Fetch `origin` and `upstream`. Check out `typing-hillclimb-campaign` and read this status and the inventory below.
2. Review the full diff from acceptance parent `origin/typing-campaign-parked/typing-campaign-baseline-20261029` to `origin/typing-hillclimb`, including callers and runtime changes. The diff covers 256 files. The previous review was partial.
3. Resolve `ReleaseFile.save`: the campaign makes its arguments keyword-only, while the parent override and Django `Model.save` accept positional arguments. The signature change is verified; an affected existing caller has not been established. Preserve the contract or explicitly decide to change it, then verify and re-evaluate affected work.
4. Resolve the `update_artifact_index` assertion versus a cast. The accepted branch has no `grouptype` platform default: both its untyped function and `platform=project.platform` match the acceptance parent. The older upstream export does add `or "javascript"`; do not carry that stale behavior forward without a decision.
5. Rebuild and verify `typing-hillclimb-upstream` from the accepted changes on a current upstream base. Exclude the evaluator, campaign log, and owner-owned baseline changes. Push the updated export. Review the parked inventory and push or carve suitable PRs, checking patch content rather than relying on patch-id counts.
6. Authorize the GitHub CLI token for the Sentry organization if PR inspection or creation fails with SAML enforcement. Decide whether to retain the parked refs after their useful changes land.

The previous handoff reports 147 callers mypy-clean, ruff check and format checks clean, and focused paginator, releasefile, file, group-index, backup comparator, and invariant suites green. Those results apply to the measured tree and its original environment. For a new exact evaluation, see the environment and command under Final measurement. The original computer's `~/.sentry/sentry.conf.py` uses a deprecated TSDB setting; decide whether to migrate that local setting. The final run used a temporary `SENTRY_CONF` with `sentry.tsdb.snuba.SnubaTSDB` and removed the temporary copy afterward.

## Behavioral changes (complete log — every runtime-visible change the campaign made)
- `src/sentry/notifications/notification_action/grouptype.py`: the accepted branch preserves the parent behavior. The older upstream export adds `platform=project.platform or "javascript"`; resolve that difference when rebuilding the export.
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
- Final acceptance: parent `66941a85b51` (tree `7d425682` = `upstream/master c8f1ef5e` + 4 evaluator policy files + 7 owner-owned files), candidate `9acb5860c21` (tree `68cc9efe`), outcome `complete` with 0 reasons. The report is local to the original computer.
- Historical acceptance parent: `4f75fa694441` = `upstream/master 625814f` + 4 evaluator policy files + 7 owner-owned files at preserved wip (mirrors the old `41a0d23` contract). All `4f75fa69`-based reports are superseded by the final parent above.
- Report progression vs new parent: 299 (b) → 204 (c) → 135 (d) → 94 (e) → 70 (f) → 63 (g) → 60 (h) → 59 (i). Zero weak/omission/configured/bypass/regression rows since (d).
- Report-i (candidate `1c4265f4`, code `19a3c9627d6`): 53 precision + 5 Any + 1 all-strong. Hard rows: `release.py` L69 `explicit` (the `-> HealthData | None` annotation references `HealthData.stats: dict[str, Any]`); `backup/dependencies.py` L454×2 `special_form` + L447 precision (byte-identical to parent — whole-program drift, see Doctrine); `releasefile.py` L405 `from_error` (not reproduced under ad-hoc strict flags — needs evaluator-profile repro, suspects: bare `update_files(files: dict)` + bare `initial_artifact_count` + decorated-generator type at L269/270); `grouptype.py` L60 `unannotated` (anchor changed by the local `or "javascript"` edit); `test_releasefile.py` L205 `no-untyped-def` (nested bare `def f()`).
- Precision long tail (~50 rows, ~30 files; largest: `seer/agent/tools` 19, `organization_details` 17, `test_committers` 16, `activity` 14, `test_release` 13, `groupactionlogentry` 12) is pre-existing wave debt, worked file-by-file after the hard rows.
- Rerun (background, ~25-90 min, `SENTRY_LOG_LEVEL=WARNING` required — an `options_store` INFO log otherwise leaks into mypy stdout and invalidates measurement; do not poll): `SENTRY_CONF=<dir with sentry.conf.py + config.yml, SENTRY_TSDB migrated> SENTRY_LOG_LEVEL=WARNING .venv/bin/python -m tools.mypy_helpers.typing_campaign evaluate --parent 66941a85b514f9acd8f097b42fb8e3854d260069 --candidate-tree 'HEAD^{tree}' --output .work/tmp/evaluate-<DATE>`.

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
Historical catalog of local branches as of 2026-10-29 (`typing-hillclimb @ 5fadd7d083d`; 200 branches). The fork now holds the parked branches under `origin/typing-campaign-parked/`. "Novel" means a patch-id comparison with zero `+` lines indicating full incorporation. Counts are an upper bound because conflict resolutions change patch IDs. Review the content when carving a PR. Regenerate after fetching with:
```bash
git for-each-ref --format='%(refname:short)' refs/remotes/origin/typing-campaign-parked | while read -r branch; do
  tip=$(git log -1 --format='%h|%ad|%s' --date=short "$branch")
  nov=$(git cherry origin/typing-hillclimb "$branch" | rg -c '^\+ ' || true)
  printf '%s || %s || novel=%s\n' "$branch" "$tip" "${nov:-0}"
done
# Inspect a branch with git cherry -v origin/typing-hillclimb <remote-branch>.
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
Follow “Resume review and publication” above. The evaluator commands and earlier campaign details remain here as historical context.
