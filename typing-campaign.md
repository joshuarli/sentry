# Sentry typing hillclimb

## Status: active — 2026-10-26 (resumed; AFK unattended)

### Resume

On the owner's next request, resume the existing typing migration from accepted source checkpoint `b628cbcf763bf36a8b1798dfb4ae9eab33a05c80`. First run:

```sh
git status --short --branch
```

Reread repository instructions and perform the parent steering checkpoint. Preserve the owner's source changes in the integration checkout. Fetch current GitHub master and rebase the typing source in a separate clean worktree, then establish the fixed policy baseline before selecting a parked proposal. The last fetched `upstream/master` was `f1a48d9501d2dd7567a831bc0b1297fd3af81418`; the campaign source was merged onto it as `594e7d8527a` (2 conflicts resolved as union) on 2026-10-26.

Use only GPT-6-Luna High for campaign agents and remove Claude-specific guidance. If environment setup is needed, follow `devenv/sync.py` directly without invoking the `devenv` tool. Getsentry is unavailable on this machine; when its checkout is absent, skip Getsentry-specific verification. Do not run formatters, change CI, or push.

### State

The integration branch is `typing-hillclimb`. Its accepted source tip is `fedf6d46155f16729ba9bf0fdfc2470ec405f30d` (exact acceptance 2026-10-26; prior tip `b628cbcf763bf36a8b1798dfb4ae9eab33a05c80`). The fixed policy baseline on `fedf6d4` is complete with no gaps: configured 115, unsuppressed 178, all-strong 11,231, missing signatures 23,724. Current fetched `upstream/master` is `f1a48d9501d2dd7567a831bc0b1297fd3af81418`; the source was merged onto it as `594e7d8527a` before promotion. The local branch is ahead of `origin/typing-hillclimb`; nothing was pushed.

Two promotions since the merge passed exact evaluation (`evaluate --parent 594e7d8 --candidate-tree HEAD`, outcome `complete`, adoption credit, core + precision complete, zero additions):
- `42ab342c55d` refactor(typing): type tagstore snuba filter helpers (`is_boolean_key`, `is_fuzzy_numeric_key`, `_translate_filter_keys`; 1 file, 3+/3-)
- `fedf6d46155` refactor(typing): type social auth backend flags (`uses_redirect`, `enabled` x2; 1 file, 4+/4-)

Two more promotions since the baseline passed exact evaluation with zero additions:
- `cacd6ea3683` refactor(typing): type project serializer helpers (`get_deploys_by_project`, `Plugin` TypedDict precision, `SharedProjectSerializer.serialize`; 1 file, 12+/4-; 6 omissions removed, 6 improved)
- `60e83cab897` refactor(typing): type mockdata core helpers (5 fully-annotated defs; 1 file, 18+/15-; 93 precision removals, 25 omissions removed)
- `756c6d5d887` refactor(typing): type release semver helpers (`ReleaseQuerySet` return narrowings x2, `is_semver_release -> bool` with `bool()` wrap; 1 file, 4+/4-; 94 precision removals incl. downstream importers, 1 omission removed)
- `a2a8fedcc67` refactor(typing): type receivers features handlers (see above; 37 removals, 3 residual notes, future work is typing `BaseEvent.data`/`tags`)
- `fad38db48a4` refactor(typing): type group serializer helpers (`-list/None` returns, `__init__`/`_expand`/`_collapse`/`_seen_stats`/`_get_group_snuba_stats` annotations; 1 file, 26+/22-; 53 precision removals, 21 omissions removed; `_get_status` TypedDict hunk dropped — precise container filled from `Any` is new debt)
- `870ac8cea05` refactor(typing): type options store accessors (see above; 128 removals, 27 omissions removed; 3 residual notes forgiven via preexisting anchors)
- `0f0d0f6c1ce` refactor(typing): type organization details endpoint (validators, save/delete paths, `flag_has_changed`, pii helpers; 2 files, 42+/31-; 154 precision removals, 56 omissions removed; needed helpers typed + `bool()` wrap + one local annotation)
- `fae67a3c66f` refactor(typing): type msteams client returns (send/update paths, `request` overloads, token locals; 1 file, 27+/12-; 21 precision removals, 10 omissions removed; dict-returning getters deliberately left untyped — callers treat results as live dicts)
- `bd2251b5d5c` refactor(typing): type tagkey and attachment endpoint params (3 endpoint `get()` signatures mined from baseline's lowest-diagnostic files; 3 files, 6+/3-; 17 precision removals, 6 omissions removed; first fully self-authored wave — parked list increasingly subsumed by upstream)
- `6414a0d859` refactor(typing): type project tags and setup wizard endpoints (2 files, 5+/4-; 17 precision removals, 3 omissions removed; transfer endpoint dropped — `dict[str, Any]` spelling is new bypass debt unless grandfathered)
- `8528df41839` refactor(typing): type committers and org stats endpoints (2 files, 4+/2-; 4 precision removals, 3 omissions removed; create-sample split out — `Project.platform` is `Optional` and poisons `dict.get` defaults)

| Measure | Parent (`594e7d8`) | Candidate (`fedf6d4`) | Change |
|---|---:|---:|---:|
| Configured additions / removals | — | — | +0 / −0 |
| Unsuppressed additions / removals | — | — | +0 / −0 |
| Precision additions / removals | — | — | +0 / −26 |
| New Any obligations | — | — | +0 |
| New / removed signature omissions | — | — | +0 / −10 |
| Signature regressions / improvements | — | — | +0 / +10 |

Credited modules: `sentry.tagstore.snuba.backend`, `social_auth.backends`. Targeted mypy, Ruff, and `git diff --check` pass on all touched files; `py_compile` passes. Focused pytest and devservices remain blocked (see Verified).

The latest candidate was commit `a8125f3e92f87d4a0156dc9761e1b1849ff97ca2` (tree `f7680fe9eb55dedfff2ef8ec3fabf2d97b8c8eb2`), on branch `typing-wave-20261024-query-construction`, against accepted parent `b628cbcf763bf36a8b1798dfb4ae9eab33a05c80`. Exact evaluation rejected it. The candidate changes `mep_to_eap.py` and `metrics/query_builder.py`; it is preserved as an unaccepted branch.

| Measure | Parent | Candidate | Change |
|---|---:|---:|---:|
| Configured diagnostics | 114 | 118 | +4 |
| Unsuppressed diagnostics | 177 | 181 | +4 |
| All-strong diagnostics | 11,227 | 11,204 | −23 |
| Missing signatures | 23,722 | 23,659 | −63 |
| Precision diagnostics | 545,928 | 545,598 | −330 |
| Any obligations | 1,440,399 | 1,439,764 | −635 |

The evaluator recorded `core_complete=true` and adoption credit, but rejected the candidate: four new configured/unsuppressed errors follow the optional `list[...] | None` MEP result contract and its stale test expectation; the metrics query change adds precision errors and Any obligations at the SNQL expression boundary. Focused tests passed 116 with 6 skipped. The scoped all-strong comparison found the same 25 existing metrics-builder diagnostics on parent and candidate after line relocation; MEP had none. Read-only Ruff and `git diff --check` passed. Independent source review found no concrete runtime behavior issue. This does not establish exact acceptance or campaign-wide precision completion.

The prior accepted source promotion was `b628cbcf763`. Two new source promotions (`42ab342`, `fedf6d4`) were merged and exactly accepted on 2026-10-26 (see State). No other new source work was merged. The seven owner-owned source and test files from `6f359a3` remain intact through the upstream merge (verified: `6f359a3..HEAD` diff empty for those paths). The optional raw evaluator report is not required to resume.

### Direction

The migration has delivered seven accepted source promotions since the earlier checkpoint, including concrete contracts in serializers, integrations, query helpers, and adapters. Core typing completion and precision completion remain separate objectives. The latest source candidate was rejected, and the owner has requested a clean stop.

The limiting stage remains exact global acceptance and proposal correctness. The latest candidate reduced aggregate debt but introduced four configured and unsuppressed errors and additional precision debt. Preserve the corrected evaluator. On resume, inspect the candidate branches against the rebased accepted source and select one testable source wave. Keep intermediate changes provisional until exact combined tree acceptance.

The campaign is frozen. No lanes are running, and no new work may start until the owner resumes it. On resume, use one coordinator and at most two preparation lanes. Keep locked dependencies. If required services remain unavailable, record the blocker once and continue with independent, testable work.

### Open lanes

No campaign lane is running and no campaign worktree remains. Every lane agent reported completion. Completed candidate reports are preserved on the branches listed below; none has current wave acceptance. Unique dirty proposals found during the previous winddown were committed to their existing lane branches or new `typing-winddown-*` branches. Those commits preserve work but do not establish source acceptance. Local edits identical to the accepted source were discarded from their worktrees.

Every unmerged campaign branch is listed below. The list exactly matches `git branch --no-merged typing-hillclimb`: 143 branches. Their branch names identify the work items. No current exact wave acceptance covers these proposals. They remain parked until the owner resumes the campaign and the coordinator selects a proposal after reviewing its diff, callers, and tests against the rebased accepted source. Recreate only the selected checkout under `.work/wt/<lane>`. The query construction branch has the specific rejection recorded above. Address its four downstream errors and metrics boundary precision debt before retry.

#### Parked branches
- `p3-apidocs-constants`
- `p3-auth-providers`
- `p3-codeowners-associations`
- `p3-frontend-version`
- `p3-integrations-analytics`
- `p3-issue-starred`
- `p3-member-invite`
- `p3-meta-three-accepted`
- `p3-metadata-jobs`
- `p3-metadata-next`
- `p3-model-followup`
- `p3-model-followup-2`
- `p3-project-key`
- `p3-release-details-types`
- `p3-release-search`
- `p3-search-base`
- `p3-serializer-types`
- `p3-utils-hashlib`
- `p3-warmup`
- `p3-web-followup`
- `p3-web-followup-2`
- `p4-api-application-serializer`
- `p4-api-tokens`
- `p4-auth-token-details`
- `p4-auth-token-details-after-artifactbundle`
- `p4-auth-token-details-rebased`
- `p4-auth-token-details-refresh`
- `p4-broadcast-details`
- `p4-broadcast-details-ready`
- `p4-broadcast-details-ready-2`
- `p4-broadcast-details-ready-3`
- `p4-broadcast-details-ready-4`
- `p4-broadcast-validator`
- `p4-catchall`
- `p4-debug-file-serializer`
- `p4-email-capture`
- `p4-event-apple-crash-report`
- `p4-filechange`
- `p4-geo-interface`
- `p4-health-middleware`
- `p4-internal-beacon`
- `p4-internal-beacon-2ba08f`
- `p4-internal-beacon-e69e`
- `p4-internal-beacon-ready`
- `p4-organization-api-key-index`
- `p4-organization-artifactbundle`
- `p4-organization-artifactbundle-current`
- `p4-organization-artifactbundle-fresh`
- `p4-organization-fork`
- `p4-organization-onboarding`
- `p4-organization-onboarding-4190`
- `p4-organization-onboarding-51fd32`
- `p4-organization-onboarding-current`
- `p4-organization-onboarding-de6a`
- `p4-organization-onboarding-latest`
- `p4-organization-recent-searches`
- `p4-project-artifact-file`
- `p4-project-commits`
- `p4-project-filter-details`
- `p4-project-filters`
- `p4-project-keys`
- `p4-project-member-index`
- `p4-user-org-integrations-2ba08f`
- `p4-user-org-integrations-4190`
- `p4-user-organizationintegrations`
- `p4-user-organizationintegrations-auth-token`
- `p4-user-organizationintegrations-current`
- `p4-user-organizationintegrations-de6a`
- `p4-user-organizationintegrations-latest`
- `p4-user-subscriptions`
- `p4-user-subscriptions-next`
- `p5-serializer-containment`
- `p5-stub-precision`
- `p5-typing-guard`
- `typing-accel-20261023-dashboard`
- `typing-accel-20261023-filestore-s3`
- `typing-accel-20261023-jira`
- `typing-accel-20261023-jira-server`
- `typing-accel-20261023-org-details`
- `typing-accel-20261023-r3-test-postgres-sort`
- `typing-accel-20261023-receiver`
- `typing-accel-20261023-sentryapps`
- `typing-accel-20261023-tagstore-snuba`
- `typing-accel-20261023-uptime`
- `typing-current-master-baseline-20261022`
- `typing-hillclimb-p10-explore-saved-queries`
- `typing-hillclimb-resume-20261022`
- `typing-lane-20261023-bitfield-models-next`
- `typing-lane-20261023-current-jira-server`
- `typing-lane-20261023-dashboard-serializer`
- `typing-lane-20261023-jira-integration`
- `typing-lane-20261023-r3-test-agent-client`
- `typing-lane-20261023-receiver-features`
- `typing-lane-20261023-search-events-fields`
- `typing-lane-20261023-snuba-utils`
- `typing-lane-20261023-uptime-validators`
- `typing-lane-max-20261023-api-paginator`
- `typing-lane-max-20261023-mockdata-core`
- `typing-lane-max-20261023-msteams-client`
- `typing-lane-max-20261023-receivers-features`
- `typing-lane-max-20261023-serializer-event`
- `typing-lane-next-20261024-receiver-features`
- `typing-loop-speed`
- `typing-loop-speed-20261021`
- `typing-next-20261024-uptime-validators`
- `typing-p3-projectplatform`
- `typing-p4-organization-pipeline`
- `typing-p6-transfer-draft`
- `typing-p7-organizationmember-wave`
- `typing-p8-gitlab-client`
- `typing-wave-20261023-accelerated-next`
- `typing-wave-20261023-accelerated-repair`
- `typing-wave-20261023-bitfield`
- `typing-wave-20261023-jira`
- `typing-wave-20261023-release`
- `typing-wave-20261024-query-construction`
- `typing-winddown-typing-20261024-next-group-serializer`
- `typing-winddown-typing-20261024-next-project-serializer`
- `typing-winddown-typing-accel-20261023-r3-aws-utils`
- `typing-winddown-typing-accel-20261023-r3-mep-to-eap`
- `typing-winddown-typing-accel-20261023-r3-options-store`
- `typing-winddown-typing-accel-20261023-r3-release`
- `typing-winddown-typing-accel-20261023-r3-releasefile`
- `typing-winddown-typing-accel-20261023-r3-stacktrace`
- `typing-winddown-typing-accel-20261023-r3-test-runner-init`
- `typing-winddown-typing-accel-20261023-r3-test-viewer-context`
- `typing-winddown-typing-accelerate-20261024-r4-filestore-s3`
- `typing-winddown-typing-accelerate-20261024-r4-issues-mixin`
- `typing-winddown-typing-accelerate-20261024-r4-jira`
- `typing-winddown-typing-accelerate-20261024-r4-mep-to-eap`
- `typing-winddown-typing-accelerate-20261024-r4-metrics-query`
- `typing-winddown-typing-accelerate-20261024-r4-receivers`
- `typing-winddown-typing-accelerate-20261024-r4-releasefile`
- `typing-winddown-typing-accelerate-20261024-r4-selenium-fixtures`
- `typing-winddown-typing-accelerate-20261024-r4-social-auth`
- `typing-winddown-typing-accelerate-20261024-r4-stacktrace`
- `typing-winddown-typing-next-20261024-mockdata-core`
- `typing-winddown-typing-next-20261024-org-details`
- `typing-winddown-typing-next-20261024-serializer-event`
- `typing-winddown-typing-query-parent-20261023`
- `typing-winddown-typing-wave-20261023-stacktrace`
- `typing-winddown-typing-wave-20261024-data-config`
- `typing/p3-grouping-actions`

### Cleanup

The previous cleanup removed 101 campaign worktrees using Git's normal worktree removal. This winddown ran `git worktree prune`; only the integration checkout remains, so this pass removed no additional worktrees. No branch refs were deleted. The rejected candidate report is losslessly compressed with its inventory and canary output in `.work/tmp/typing-campaign-winddown`. That 73 MiB bundle is optional and is not needed to resume.

The previous cleanup raised available disk space from 68 GiB to 178 GiB, recovering 110 GiB. The requested ~300 GB recovery target was not met. Available space remains 178 GiB. No non-root worktree remains eligible for cleanup. The `.work/` directory is ignored through `.git/info/exclude` and resides on APFS.

The only retained worktree is the root integration checkout. It has seven owner-owned changes that were not modified or staged:

- `src/sentry/similarity/__init__.py`
- `src/sentry/templatetags/sentry_helpers.py`
- `src/sentry/unmerge.py`
- `src/sentry/utils/datastructures.py`
- `src/sentry/utils/eventuser.py`
- `tests/sentry/templatetags/test_sentry_helpers.py`
- `tests/sentry/utils/test_datastructures.py`

### Not started

No next source wave is selected. On resume, fetch current master, rebase the source in a clean worktree, establish its fixed policy baseline, perform the parent steering checkpoint, then select one testable parked proposal.

### Verified

- Evaluator `baseline` on `fedf6d4`: `complete`, `core_complete=true`, no gaps; report at `.work/tmp/typing-baseline-20261026/report.json`.
- Evaluator `evaluate --parent 594e7d8 --candidate-tree HEAD`: `complete`, adoption credit, core + precision complete, zero additions; report at `.work/tmp/typing-eval-20261026/report.json`.
- Targeted mypy (`SENTRY_MYPY_PRE_PUSH=1`) passes on `src/sentry/tagstore/snuba/backend.py`, `src/sentry/integrations/gitlab/client.py`, `src/social_auth/backends/__init__.py`. Read-only Ruff and `git diff --check` pass; `py_compile` passes.
- Venv restored without devenv per `devenv/sync.py` python-deps step (`brew upgrade uv`, `uv python install 3.13`, `uv sync --frozen --inexact --active`) plus `python -m tools.fast_editable --path .` (required: without it mypy fails with `No module named 'sentry'`); `mypy 2.1.0` matches evaluator expectation. Evaluator runs need `SENTRY_LOG_LEVEL=WARNING`: a `sentry.options_store` INFO log otherwise leaks into mypy stdout and invalidates the measurement.
- Lane repair rules learned: partially-annotated defs get checked (missing return flagged as new error) while fully-untyped defs stay exempt — prefer full annotation or none; narrowing pass-through `*args/**kwargs` to `object` poisons downstream attribute uses (16 new errors) — leave pass-throughs untyped.
- Rejected and parked with repair recipes: api-paginator lane (`c1e26a9`, partial `get_result` + `CursorValue -> object` widening; 5 precision + 7 Any additions) — needs `CursorResult[object]` return plus queryset typing or a wave split. Filestore-s3 lane (`c758e8eeb99` + subsumed-hunk fix): attribute soup must be typed before methods — needs `_multipart`/`_entries`/`obj`/`file` attrs with boto3/Django stub types, `File` → `File[bytes]`, and investigation of `assert`-narrowing unreachables. Releasefile wave (`98a929da`, 36+/19-): needs multi-file treatment — `validate_pii_*` helpers are done in-lane but test file + endpoint callers + dunder renames need their own waves. Jira-server wave: blocked on untyped `ApiClient.get/post` (`-> Any`) base — type the shared base first. Release wave needed two repairs: `bool()` wrap for `Any is not None` no-any-return, and dropping the `follows_semver_versioning_scheme -> bool` hunk (body flows `cache.get` Any) — 4th-hunk lesson: review the FULL parked diff, not just its head. Group-serializer wave needed the same class of repair: dropped `_get_status` TypedDict hunk — rule: never newly-annotate a container that gets filled from `Any` sources (attrs dicts, untyped calls); the forgiveness path only covers preexisting anchors. Options-store wave needed three repairs: restored a dropped `None`-cache guard (behavior!), dropped the `model`/`model_cls -> type[...]` annotations (resolving Any-chains into Django generics creates explicit debt — only resolve into well-typed custom classes like `ReleaseQuerySet`), and dropped the `__init__`/`set`/`set_store`/`set_cache` Optional-cache web (leaks caller `Any` obligations into unchanged files + breaks a test) plus a redundant narrowing assert. Receivers wave accepted with 3 residual precision notes (`BaseEvent.data` still `Any`); repair sketch is typing `BaseEvent.data`/`tags`. Msteams wave needed one repair: dropped two `-> object` getters whose dict-style callers broke (narrow returns must match live usage, not just the body). Transfer-tagkeys wave dropped accept_project_transfer: explicit-`Any` spellings (`dict[str, Any]`) are new bypass debt unless the same spelling already exists in that file — tagstore passed only by grandfathering.
- Screening correction: symmetric `merge-base...branch` diffs mislead after the upstream merge (several parked branches are already subsumed by upstream or would regress it: search-events-fields, dashboard-serializer, test-runner-init). Gate on direct `git diff HEAD <branch>` showing the branch strictly improving on HEAD.
- Blockers (recorded once): `devservices up --mode migrations` fails (`DependencyError: sentry-shared-postgres`, HTTP 403); focused pytest fails on redis `localhost:6379` refused. No DB-backed tests until services are available.
- The root checkout is clean except this document; the merge preserved owner files; `.work/` holds only evaluator outputs (7.3G); no push, no formatters.

### Campaign log

2026-10-26 — Resumed AFK: merged `upstream/master f1a48d9` as `594e7d8`, promoted and exactly accepted tagstore-snuba (`42ab342`) and social-auth (`fedf6d4`) waves, established fixed-policy baseline, restored venv without devenv. Next: select one testable parked proposal (project-serializer pre-checked clean) and continue the hillclimb.
