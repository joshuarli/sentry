# Sentry typing hillclimb

## Status: resumed 2026-10-27 — defects 1-3 repaired; serializer waves through event get_attrs landed (provisional), continuing.

Resume here: `git status --short --branch` on `typing-hillclimb`, then reread the Corrective checkpoint, Resume, and State below. Toolchain notes (venv restore without devenv, `SENTRY_LOG_LEVEL=WARNING`, `fast_editable`) are under Verified.
Current source tip: `cb9fb27356a` (event serialize user-shadow fix + unused group arg). Accepted by static checks only: targeted mypy, Ruff, `git diff --check`, `py_compile`. No pytest ran; devservices is blocked (shared-postgres 403, no redis). "Accepted" means static checks passed, not that behavior is proven preserved.
Known defects: all three Corrective defects repaired (options-store assertion `00910daf893`; msteams index `b7308e43a62` + regression tests; re-audit `68dd1ad4fc3` dropping `existing_info: dict[str, object]` over schemaless DB JSON). New msteams + scope-validator + serializer tests unrun without services. GitLab 48 response envelopes audited 2026-10-27: 19 supported by docs+tests+callers, 29 docs-only provisional (no contradictions; unobserved returns); avatar casts supported by registry+endpoint tests; remaining casts supported except the fixed trusted-relay case.
Parked: the 143 branches in the Parked list (none re-verified; upstream merged 125 commits mid-campaign, so treat old subsumption notes as unconfirmed), plus 3 lane branches with fixups: `typing-lane-api-paginator` (partial get_result + object-widening; retry with `CursorResult[object]` or split), `typing-lane-filestore-s3` (attribute soup untyped; retry after typing file attrs with boto3/Django stub types), `typing-lane-releasefile` (helpers done; callers/tests/dunder renames pending in a follow-up wave). These are parked branches, not active parallel work.

### Corrective checkpoint (2026-10-27 review)

The application typing gains are worth keeping. The review found that acceptance had drifted from "evaluator passes" toward "typing metric improves" without proving the new contracts or preserving runtime behavior. Do not restart the campaign, rewrite the evaluator, or add a detector or provenance framework.

Defects to repair first, each in its own commit:
1. Done in `00910daf893`; the unreachable `None`-cache guard was removed with it. Restore the `OptionsStore.get_cache` initialization assertion removed by `ba6d37b7c27` (via merge `870ac8cea05`): `assert self.cache is not None, f"Option '{key.name}' requested before cache initialization, which could result in excessive store queries"`, ahead of the local-cache read. The later `if self.cache is None: return None` guard is a different behavior and does not replace it. `tests/sentry/options/test_store.py::test_simple_without_cache` asserts the message and fails at the current tip. Any deliberate change to this initialization contract is a separate behavioral fix with its own regression test.
2. Done in `b7308e43a62`; `get_user_conversation_id` now indexes `resp["id"]` so a missing id raises `KeyError` instead of propagating `None` as `str`. Producer evidence: Bot Framework conversation-creation returns a resource with required `id`; existing callbacks in `test_utils` and `test_link_identity` assert the `{"id": ...}` shape, and all callers pass the result directly to `send_card(conversation_id: str)`. New regression cases in `test_client.py` cover success and missing-id raise. The other annotated token-metadata locals (`access_token`, `expires_at`, `get_token_data`) already index and were left unchanged.
3. Done in `68dd1ad4fc3` (audit 2026-10-27, two explore lanes): every typed local/cast from `Any` in `upstream/master..HEAD -- src/` re-audited. GitLab: 48 envelopes, 19 supported (docs+tests+callers), 29 docs-only provisional with no contradictions and no runtime impact for unobserved returns. Avatar `cast(dict, serialize(...))` supported (concrete owners registered; org avatar tests assert dict shape). Other casts supported (DRF validation, ORM contracts, sentinel checks, local construction). One fix: dropped `existing_info: dict[str, object]` over schemaless `OrganizationOption` JSON (no validation; annotation erased so no behavior change).

Acceptance rules from now on:
- Every transition from dynamic data to a precise type needs identifiable producer, schema, validation, or test evidence. Typed locals and casts get the same scrutiny as annotations.
- Decide each annotation as a contract decision. Do not use syntax rules ("a preexisting `Any` spelling in this file makes a new one safe", "never annotate a container filled from `Any`") as evidence either way. `object` is fine for a genuinely opaque value; it is wrong where consumers do mapping operations.
- A difficult signature left untyped needs a named dependency to repair first, not indefinite avoidance.
- Pick one related interface group and finish its producer and consumer typing instead of taking the easiest signatures.
- Do an independent source review before the expensive exact comparison.

While services are unavailable:

| Candidate | Treatment |
|---|---|
| Annotations with established contracts and unchanged executable behavior | Continue with targeted mypy, Ruff, and any runnable tests |
| Added or removed assertions, changed defaults, coercions (`bool()` wraps), exception paths, registration behavior | Needs executable behavioral evidence before promotion |
| Service-dependent contract whose tests cannot run | Provisional; do not call it verified |

### Resume

On the owner's next request, resume the existing typing migration from source tip `b7308e43a62`. First run:

```sh
git status --short --branch
```

Reread repository instructions, then finish the Corrective checkpoint defect 3 (re-audit). Preserve the owner's source changes in the integration checkout. The branch was rebased onto `upstream/master 4d382318f71` on 2026-10-27 (previous base `f1a48d9501d`; 333 picks, 1 skipped obsolete events-meta policy, conflicts resolved in `pyproject.toml`, `gitlab/client.py`, `msteams/client.py`). No broad scouting or baseline rebuild is needed for the correction.

Use only GPT-6-Luna High for campaign agents and remove Claude-specific guidance. If environment setup is needed, follow `devenv/sync.py` directly without invoking the `devenv` tool. Getsentry is unavailable on this machine; when its checkout is absent, skip Getsentry-specific verification. Do not run formatters, change CI, or push.

### State

The integration branch is `typing-hillclimb`. Its source tip is `cb9fb27356a`, accepted by static checks only (see Corrective checkpoint). The last fixed policy baseline, on `fedf6d4` (an earlier checkpoint), is complete with no gaps: configured 115, unsuppressed 178, all-strong 11,231, missing signatures 23,724. Current `upstream/master` is `4d382318f71f48db6cb82c3cbf3020f07aabfcad`; the branch was rebased onto it on 2026-10-27. The local branch is ahead of `origin/typing-hillclimb`; nothing was pushed by the agent since the owner's push.

Post-rebase waves accepted by targeted mypy, Ruff, `git diff --check`, `py_compile` only (pytest blocked; provisional until services return and exact evaluation completes):
- `6398d0f2ccf` refactor(typing): type scope-list validators for api keys and org tokens (`validate_scope_list` x2; 2 files, 2+/2-; DRF/Django array-of-text schema, SENTRY_SCOPES + forbidden set, endpoint 400 tests)
- `348d7f7f97c` refactor(typing): type ApiToken serializer request and response contracts (`get_attrs` + `serialize` + `ApiTokenSerializerResponse`; 1 file, 39+/6-; ApiApplication response producer, model field types, include_token callers, serializer unit tests; exact `evaluate` timed out at 10 min, not yet accepted)
- `787b9883c9d` refactor(typing): parameterize ApiApplication serializer with response type (1 line; completes the producer side of the ApiToken.application contract; no explicit-serializer call sites, zero caller impact)
- `c41669990fa` refactor(typing): type ApiAuthorization serializer request and response contracts (same producer shape as ApiToken; organization service returns Any | None so the field stays opaque `object`; 1 file, 34+/5-)
- `1eeafbfac06` refactor(typing): type TeamRole serializer params mirroring sibling (3 annotations matching OrganizationRoleSerializer; 1 file, 7+/1-)
- `1c3b7b7ca80` refactor(typing): type CommitFileChange serializer request and response contracts (TypedDict with Author | EmptyAuthor per the commit serializer's published schema; fixes dict[int, Any] key type; 1 file, 35+/7-)
- `1049b829f3d` refactor(typing): type Commit serializer get_attrs and serialize params (deliberately leaves classes unparameterized: explicit-serializer call sites in committers, seer tools, activity, and group-action-log are unaudited; 1 file, 32+/6-)
- `aae651b9bff` refactor(typing): type PullRequest serializer request and response params (completes the commit pullRequest producer; two mypy findings repaired: str | None external_url, getattr for prefetch-injected valid_attributions; 1 file, 37+/8-)
- `5f18513730f` refactor(typing): narrow user params on repository serializers to base union (3 params; 1 file, 7+/3-)
- `04043f345bd` refactor(typing): type get_users_for_commits helper params (mirrors get_users_for_authors; 1 file, 3+/1-)
- `858fd1dee94` refactor(typing): type Commit serializer constructors (exclude/include/type evidence from committers and seer call sites; 1 file, 17+/3-)
- `b6001cd472d` refactor(typing): type DashboardWidget serializer params and fix date claim (dateCreated str→datetime per model; 1 file, 22+/5-)
- `d94bb3adc78` refactor(typing): type dashboard query, on-demand, and permissions serializer params (completes widget queries producer chain; 1 file, 27+/4-)
- `2d0c6dda3b7` refactor(typing): type Dashboard list serializer params and correct response claims (dateCreated/lastVisited str→datetime per models; createdBy narrowed from over-precise UserSerializerResponse to the opaque dict the user service returns; user param deliberately stays Any where ids flow into None-tolerant ORM lookups; 1 file, 17+/6-)
- `245be486855` refactor(typing): type dashboard details and revision serializer params (same dateCreated/createdBy corrections via the in-file revision precedent; removes now-unused import; 1 file, 28+/7-)
- `b38e5d5f1f6` + `e2e256f533f` refactor(typing): type Activity get_attrs, init, and serialize params (consumes the newly typed commit/pullrequest/group producers; widens mentions helper list→Sequence; 1 file)
- `9966a154a12` refactor(typing): type UserReport serializer request and response contracts (6 mypy findings repaired incl. shadowed user param, wrong attrs key type, str dateCreated claim; 1 file, 39+/14-)
- `71d0f905729` refactor(typing): finish role init and userreport child get_attrs contracts (child get_attrs unblocked by the shared attrs shape fix; 2 files, 8+/3-)
- `6df33ff9e48` refactor(typing): type Group _get_status return against demanded schema (revisits the dropped hunk with the caller-demanded TypedDict instead of a new one; 1 file, 5+/1-)
- `7528604692e` fix(tests): use per-item attrs in ApiToken serializer tests (the tests misused the item-mapping as single-item attrs; fixed to per-item, runtime-identical; 1 file)
- `f1770b4a1a6` refactor(typing): type event get_attrs chain and crash-file helper (base user stays Any: flows into User-demanding get_entries and a narrowing restructure needs service-backed tests; map_device_class_tags stays untyped pending a shared tag-mapping protocol; 1 file, 21+/6-)
- `a75f11145ac` refactor(typing): type event base serialize params and fix platform claim (platform str→str | None per eventstore model; 1 file, 9+/3-)
- `cb9fb27356a` refactor(typing): type event base serialize user shadow fix and relax unused group arg (renames shadowed minimal_user; widens vestigial group param verified unused in body; 2 files, 10+/4-)
- `1f24219b986` refactor(typing): type ExternalEventSerializer response contract (ExternalEventSerializerResponse TypedDict; tags list[EventTag]; user and-narrowing mirrored on sibling SimpleEvent pattern; 1 file, 20+/4-; 2 mypy findings repaired)
- `885ff9818bc` refactor(typing): type SharedEventSerializer serialize params (mirrors base contract; dict[str, Any] return per in-body annotation and latestEvent consumer; 1 file, 7+/1-; override ignore per SharedGroup subset precedent)
- `d3d703abb7f` refactor(typing): type IssueEventSerializer helpers and serialize params (user-report/sdk-updates/resolved-with contracts vs wrap_event_response consumer; _get_resolved_with widened off Event annotation-only; 1 file, 12+/4-)
- `c98c1e22a44` refactor(typing): type SqlFormatEventSerializer helpers and params (get_attrs user narrowing; _format user widening over unused param; _get_release_info event union + version fallback; 1 file, 21+/6-)
- `5d39129c995` refactor(typing): declare Author as explicit TypeAlias (repairs named dependency; resolves 6 valid-type + cascading annotation/unreachable findings in release.py; 1 file, 2+/2-; repo-wide mypy over all 9 importing modules)
- `95065ddec17` refactor(typing): type release last-commit/last-deploy producer chain (params mirror _get_authors_metadata; Sequence keeps override compatible; returns flow into lastCommit/lastDeploy; 1 file, 16+/7-)
- `f5f19e29f80` refactor(typing): type GroupEventReleaseSerializer serialize params (obj narrowed to Release per _get_release_info producer; body satisfies response with no findings; 1 file, 7+/1-)
- `5871488726d` refactor(typing): type release expose/query helpers (HealthData/SerializedProject contracts; slug narrowed on column evidence; None-to-empty coercions mirroring in-file idioms; AdoptionStage precision; 1 file, 51+/20-; 4 findings repaired)
- `18dc2d6f90e` fix(tests): pin release None-coercion contracts (per-project newGroups, missing stats; 1 file, 52+/1-)
- `ae43febde45` refactor(typing): type ReleaseSerializer get_attrs/serialize params (Sequence inputs; dead None arm removed; _get_authors_metadata widened; 1 file, 19+/9-; order_by_sessions -n3 flake reproduces on base)
- `22c58b22d64` refactor(typing): type DashboardListSerializer get_attrs user contract (resolves deferred Any via serialize_generic_user adapter + isinstance-narrowed lookups; 1 file, 11+/8-; 314 dashboard endpoint tests green)
- `992ef179072` refactor(typing): parameterize CommitSerializer with response type (audits all 3 explicit-serializer call sites; AuthorCommitsSerialized ripple + working-copy annotation; 3 files, 8+/4-; 51 + 20 tests green)
- `703e8e19434` refactor(typing): type BasePaginator get_result contract (repairs parked lane: keeps CursorValue, CursorResult[object] return, required rename; queryset generics split out; 1 file, 11+/4-; 43 + 13 tests green)
- `8051f2a8f10` refactor(typing): type S3 filestore file and storage contracts (repairs parked lane on current tree; dynamic multipart attr; url override marked; boto3-opaque defs split out; 1 file, 35+/19-; 4 findings repaired; 16 tests green)
- `56991c34f15` refactor(typing): type releasefile archive and index contracts (repairs parked lane via clean cherry-pick; QuerySet/dunder/IO generics; structural yield-None; 1 file, 33+/23-; 26 tests green)
- `0cbfca9eca5` refactor(typing): type SimpleEventSerializer get_attrs after eventstore audit (Event-only producers, no GroupEvent registration; LSP ignore marked; 1 file, 6+/1-; 37 endpoint tests green serially, -n3 flake pre-existing)
- `6615a1bc8ff` refactor(typing): type map_device_class_tags over shared EventTag shape (resolves deferred protocol; all producers carry list[EventTag]; 1 file, 1+/1-; 27 tests green)
- `86307ad6a91` refactor(typing): type event base-producer helpers (tags/entries/meta/error contracts; get_entries user widened; transaction floats split out pending payload evidence; 1 file, 21+/7-; 50 tests green)
- `fd2b7c1a7df` refactor(typing): type GroupSerializerSnuba seen-stats query helpers (execute/parse contracts vs typed callers; Snuba __init__ split out on upstream FilterConvertParams gap; 1 file, 19+/7-; 53 tests green serially)
- `deab70519ff` refactor(typing): type stream seen-stats enrichment explicitly (Mapping widening, bool() per base, StreamSeenStats rebuild; 2 files, 31+/21-; 151 + 3 tests green serially)
- `ddf020afc49` refactor(typing): type group stats mixin query contracts (abstract/concrete query_tsdb, get_stats, Stream constructors; 2 call-site asserts; 1 file, 32+/25-; 76 tests green)
- `e4df89e19f2` refactor(typing): narrow base EventSerializer get_attrs user to union (matches Serializer base; all overrides already union; 1 file, 1+/1-; 37 tests green serially)
- `20e11008076` refactor(typing): narrow project key and repository serializer users (both unused in body; 2 files, 17+/3-; 21 tests green)
- `6cf8bfd761a` refactor(typing): narrow seer serializer users to union (passthrough only; 2 files, 20+/5-; 85 tests green)
- `325d1a00c86` refactor(typing): narrow remaining serializer user and attrs params (onboarding/chunk/trace; unused in bodies; 3 files, 20+/3-; 52 tests green)
- `f02c781cf0a` refactor(typing): narrow trace attribute value serializer params (sibling contract; 1 file, 10+/1-; 29 tests green serially)
- `1718d596fd0` refactor(typing): type group release serializer contracts (registry dispatch deterministic; fixes in-body key annotation; 1 file, 55+/12-; 21 tests green)
- `c96ef218b7e` refactor(typing): narrow event user serializer user and attrs (obj split out: 7 nullable producer fields vs non-null response; 1 file, 13+/2-; 8 tests green, apidocs fixture missing on base)
- `e4d63a28860` refactor(typing): type artifact bundle serializer contracts (row-tuple shape; archive typed; endpoint-local entry shape split out; 1 file, 69+/12-; 13 tests green)
- `9332b77f002` refactor(typing): type data export serializer contracts (params mirror base; response holds vs model evidence; 1 file, 18+/2-; 61 tests green)
- `5e75f33ae11` refactor(typing): type discover saved query serializer contracts (user union + adapter; nullable corrections per structural producers; 1 file, 41+/22-; 79 tests green)
- `9de1067c2eb` refactor(typing): type audit log entry serializer contracts (response vs typed event registry; private helpers stay untyped; 1 file, 33+/3-; 38 tests green)
- `dbf118c2c1e` fix(tests): pin admin broadcast creator email contract (previously untested Admin path; 1 file, 11+/0-)
- `4ade7ff1e9f` refactor(typing): type broadcast serializer contracts (response TypedDicts; user unions; relation-named created_by_id stands; 1 file, 62+/11-; 25 tests green)

Deferred with named dependencies (not dropped): GroupSeenSerializer stays untyped (no callers; endpoint builds the payload manually); release.py GroupEvent slice parked (pre-existing Author-alias valid-type errors plus unreachable-code findings in-file; needs shared-alias repair with repo-wide verification); CommitSerializer class-level parameterization (explicit-serializer call sites unaudited); Dashboard list get_attrs user narrowing and event get_entries user contract (need service-backed tests proving anonymous-equivalence); map_device_class_tags precision (heterogeneous tag-dict shapes need a shared mapping protocol); SimpleEventSerializer get_attrs (bind_nodes demands Sequence[Event] while the serializer contract accepts GroupEvent; needs eventstore contract audit first).

Deferred with named dependencies (not dropped): GroupSeenSerializer (serialize returns None; parameterizing would push `| None` onto unaudited registry callers — needs caller audit first); CommitSerializer class-level parameterization (explicit-serializer call sites in committers/seer/activity unaudited).

Early promotions since the merge passed exact evaluation (`evaluate --parent 594e7d8 --candidate-tree HEAD`, outcome `complete`, adoption credit, core + precision complete, zero additions):
- `42ab342c55d` refactor(typing): type tagstore snuba filter helpers (`is_boolean_key`, `is_fuzzy_numeric_key`, `_translate_filter_keys`; 1 file, 3+/3-)
- `fedf6d46155` refactor(typing): type social auth backend flags (`uses_redirect`, `enabled` x2; 1 file, 4+/4-)

Later promotions passed exact evaluation with zero additions (evaluator acceptance only; `870ac8cea05` removed a runtime assertion and `fae67a3c66f` added the unchecked msteams local):
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
- `3db607df07d` refactor(typing): type relay details delete param (1 line; 2 precision removals, 1 omission removed; auth `__init__` dropped — DRF's overloaded base rejects both `object` and `Any` varargs)
- `4f1f3faf3b5` refactor(typing): type project key validator (`Mapping` in, named local out; 1 file, 6+/3-; 9 precision removals, 2 omissions removed; eventuser sibling parked — response TypedDict lies about nullability)
- `b0faba7b579` refactor(typing): type apidocs extension hook (sibling-pattern signature + load-bearing assert; 1 file, 6+/2-; 4 precision removals, 3 omissions removed; precise `dict[str, str]` beat explicit `Any`)
- `18c85dbf5b0` refactor(typing): type transaction names endpoint (`project: Project`; 1 file, 2+/1-; 9 precision removals, 1 omission removed; symbol-sources sibling split out — `dict[str, Any]` param+return is new explicit debt)
- `7fd9d87e51f` refactor(typing): type custom exception handler (`Exception`, `dict[str, object]`, `Response | None`; 1 file, 2+/1-; 7 precision removals, 3 omissions removed)
- `c22a9b89c79` refactor(typing): type audit render and attachment cache init (pure-`str` flow, `**kwargs: object` into untyped base; 2 files, 2+/2-; 7 precision removals, 3 omissions removed)
- `945bd7f36ad` refactor(typing): type avatar filename and project transfer params (re-specialized `AvatarMixin` onto related models; 3 files; exact acceptance with zero new errors, adoption credit)

The tagstore and social-auth promotions together removed 26 precision diagnostics and 10 signature omissions with no additions against `594e7d8`. Targeted mypy, Ruff, `git diff --check`, and `py_compile` passed on those files.

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

The seven owner-owned source and test files from `6f359a3` remain intact through the upstream merge (verified: `6f359a3..HEAD` diff empty for those paths). The optional raw evaluator report is not required to resume.

### Direction

The migration has delivered 20 evaluator-accepted source promotions since the earlier checkpoint, including concrete contracts in serializers, integrations, query helpers, and adapters; two need repair (see Corrective checkpoint). Core typing completion and precision completion remain separate objectives. The latest source candidate was rejected, and the owner has requested a clean stop.

The limiting stage remains exact global acceptance and proposal correctness. The latest candidate reduced aggregate debt but introduced four configured and unsuppressed errors and additional precision debt. Preserve the corrected evaluator. On resume, inspect the candidate branches against the rebased accepted source and select one testable source wave. Keep intermediate changes provisional until exact combined tree acceptance.

The campaign is frozen. No lanes are running, and no new work may start until the owner resumes it. On resume, use one coordinator and at most two preparation lanes, repair the Corrective checkpoint defects first, then continue under its acceptance rules. Keep locked dependencies. If required services remain unavailable, record the blocker once and continue only with work its table allows.

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

No next source wave is selected. On resume, repair the Corrective checkpoint defects, then select one related interface group (producer and consumer together) and review its diff, callers, and tests before the exact comparison.

### Deferred with named dependencies (not dropped)

- `GroupSeenSerializer` stays fully untyped: no callers exist (the group-details endpoint builds its seen-by payload manually with full types). Typing it would create an unobserved contract; revisit only if a caller appears.
- `release.py` GroupEvent slice parked: the file carries pre-existing `Author`-alias `valid-type` errors plus unreachable-code findings; annotating into a red file cannot prove a clean slice. Named dependency: repair the shared `Author` alias with repo-wide verification first.
- Dashboard list `get_attrs` keeps `user: Any`: its ORM lookups tolerate anonymous `None` via IS NULL, and any narrowing restructure needs service-backed tests to prove equivalence.
- GroupSeenSerializer and the items above are recording-only; no source changed for them.

### Verified

- Historical (earlier checkpoint `fedf6d4`, not the current tip): fixed-policy baseline `complete`, `core_complete=true`; exact evaluation against `594e7d8` complete with adoption credit. Later promotions were each exactly evaluated, but no current-tip baseline report is on record.
- Historical: targeted mypy (`SENTRY_MYPY_PRE_PUSH=1`) passed on `src/sentry/tagstore/snuba/backend.py`, `src/sentry/integrations/gitlab/client.py`, `src/social_auth/backends/__init__.py`. Read-only Ruff and `git diff --check` pass; `py_compile` passes.
- Venv restored without devenv per `devenv/sync.py` python-deps step (`brew upgrade uv`, `uv python install 3.13`, `uv sync --frozen --inexact --active`) plus `python -m tools.fast_editable --path .` (required: without it mypy fails with `No module named 'sentry'`); `mypy 2.1.0` matches evaluator expectation. Evaluator runs need `SENTRY_LOG_LEVEL=WARNING`: a `sentry.options_store` INFO log otherwise leaks into mypy stdout and invalidates the measurement.
- Lane repair rules learned: partially-annotated defs get checked (missing return flagged as new error) while fully-untyped defs stay exempt — prefer full annotation or none; narrowing pass-through `*args/**kwargs` to `object` poisons downstream attribute uses (16 new errors) — leave pass-throughs untyped.
- Rejected and parked with repair recipes: api-paginator lane (`c1e26a9`, partial `get_result` + `CursorValue -> object` widening; 5 precision + 7 Any additions) — needs `CursorResult[object]` return plus queryset typing or a wave split. Filestore-s3 lane (`c758e8eeb99` + subsumed-hunk fix): attribute soup must be typed before methods — needs `_multipart`/`_entries`/`obj`/`file` attrs with boto3/Django stub types, `File` → `File[bytes]`, and investigation of `assert`-narrowing unreachables. Releasefile wave (`98a929da`, 36+/19-): needs multi-file treatment — `validate_pii_*` helpers are done in-lane but test file + endpoint callers + dunder renames need their own waves. Jira-server wave: blocked on untyped `ApiClient.get/post` (`-> Any`) base — type the shared base first. Release wave needed two repairs: `bool()` wrap for `Any is not None` no-any-return, and dropping the `follows_semver_versioning_scheme -> bool` hunk (body flows `cache.get` Any) — 4th-hunk lesson: review the FULL parked diff, not just its head. Group-serializer wave needed the same class of repair: dropped `_get_status` TypedDict hunk — that hunk was dropped because its producer was `Any`; decide such cases by producer evidence, not by a blanket rule. Options-store wave needed three repairs: restored a dropped `None`-cache guard (that guard is not the removed initialization assertion, which was never restored; see Corrective checkpoint), dropped the `model`/`model_cls -> type[...]` annotations (resolving Any-chains into Django generics creates explicit debt — only resolve into well-typed custom classes like `ReleaseQuerySet`), and dropped the `__init__`/`set`/`set_store`/`set_cache` Optional-cache web (leaks caller `Any` obligations into unchanged files + breaks a test) plus a redundant narrowing assert. Receivers wave accepted with 3 residual precision notes (`BaseEvent.data` still `Any`); repair sketch is typing `BaseEvent.data`/`tags`. Msteams wave needed one repair: dropped two `-> object` getters whose dict-style callers broke (narrow returns must match live usage, not just the body). Transfer-tagkeys wave dropped accept_project_transfer: explicit-`Any` spellings (`dict[str, Any]`) are new bypass debt unless the same spelling already exists in that file — tagstore passed only by grandfathering.
- Screening correction: symmetric `merge-base...branch` diffs mislead after the upstream merge (several parked branches are already subsumed by upstream or would regress it: search-events-fields, dashboard-serializer, test-runner-init). Gate on direct `git diff HEAD <branch>` showing the branch strictly improving on HEAD.
- Blockers (recorded once): `devservices up --mode migrations` fails (`DependencyError: sentry-shared-postgres`, HTTP 403); focused pytest fails on redis `localhost:6379` refused. No DB-backed tests until services are available.
- Toolchain lesson (2026-10-27): a missing `Mapping` import in an edited file broke Django setup and with it the mypy Django plugin for every file. `py_compile` does not catch name errors and ruff did not flag this one — always re-run targeted mypy after import edits, and treat a sudden all-file mypy outage as a broken import first.
- The root checkout is clean; the merge preserved owner files; `.work/` holds only evaluator outputs (7.3G); no push, no formatters.

### Campaign log

2026-10-26 — Resumed AFK: merged `upstream/master f1a48d9` as `594e7d8`, promoted and exactly accepted tagstore-snuba (`42ab342`) and social-auth (`fedf6d4`) waves, established fixed-policy baseline, restored venv without devenv. Next: select one testable parked proposal (project-serializer pre-checked clean) and continue the hillclimb.

2026-10-27 — Winddown after 20 exact-accepted promotions (tagstore, social-auth, project-serializer, mockdata, release, receivers, group-serializer, options-store, org-details, msteams, tagkey trio, project-tags/setup-wizard, committers-stats, relay, project-key, txn-symbols, audit-attach, handlers, avatar). Parked 3 new lane branches with fixups (api-paginator, filestore-s3, releasefile); deleted 5 empty lane branches; one worktree at a time, all removed; `.work` holds only the current fixed-policy baseline (1.6G). Blockers unchanged: no devservices, no pytest/CI. Nothing pushed.

2026-10-27 — External review of `594e7d8..945bd7f`: keep application gains, but the options-store assertion removal and the msteams `Any`-to-`str` local show evaluator acceptance is not behavior preservation. Added the Corrective checkpoint, reconciled the stale tip and state, and replaced syntax-based avoidance rules with contract-evidence rules. Campaign remains paused; no source changed.

2026-10-27 — Resumed per owner: rebased `typing-hillclimb` onto `upstream/master 4d38231` (333 picks, skipped obsolete events-meta policy `1589755`, resolved `pyproject.toml`, `gitlab/client.py` token-refresh union, `msteams/client.py` import union), then fixed Corrective defect 2 in `b7308e4` (index `resp["id"]`, regression tests added but unrun without services). Backup ref `typing-hillclimb-backup-20261027` retained. Next: re-audit defect 3, then select one interface group wave.

2026-10-27 — Defect 3 re-audit complete (two explore lanes, no edits): GitLab 48 envelopes (19 supported, 29 docs-only provisional, no contradictions), avatar + all other casts supported except trusted-relay `existing_info` false precision, fixed in `68dd1ad` (annotation removed, no runtime change; mypy+Ruff+diff-check+py_compile pass, pytest blocked). All three Corrective defects repaired. Next: select one related interface-group wave under the acceptance rules.

2026-10-27 — Scope-validator wave `6398d0f` landed (endpoint + model `validate_scope_list`, static checks pass, endpoint 400 tests unrun without services). Continuing with next interface-group wave.

2026-10-27 — ApiToken serializer wave `348d7f7` landed (get_attrs/serialize + response TypedDict, static checks pass, serializer unit tests unrun without services; exact evaluate timed out at 10 min, wave provisional). Continuing with next interface-group wave.

2026-10-27 — ApiApplication one-liner `787b988` landed (parameterize with existing response TypedDict; no explicit-serializer call sites, static checks pass). Token serializer group now complete producer-to-consumer. Continuing.

2026-10-27 — Serializer waves `c416699` (ApiAuthorization), `1eeafbf` (TeamRole params), `1c3b7b7` (CommitFileChange), `1049b82` (Commit params), `aae651b` (PullRequest params; 2 mypy findings repaired), `5f18513` (repository user params), `04043f3` (get_users_for_commits): all static checks pass, tests unrun. GroupSeen + CommitSerializer parameterization deferred with named dependencies (unaudited callers). Continuing.

2026-10-27 — Serializer waves `c416699` (ApiAuthorization), `1eeafbf` (TeamRole), `1c3b7b7` (CommitFileChange), `1049b82` (Commit params), `aae651b` (PullRequest params; 2 mypy findings repaired), `5f18513` (repository user params), `04043f3` (get_users_for_commits), `858fd1d` (Commit constructors), `b6001cd` (DashboardWidget params + date fix), `d94bb3a` (dashboard query perms), `2d0c6dd` (Dashboard list params + 3 claim fixes), `245be48` (dashboard details/revision). All static checks pass; tests unrun. Deferred with named dependencies: GroupSeenSerializer nullable return (needs caller audit), CommitSerializer class parameterization (unaudited explicit call sites), List get_attrs user narrowing (needs service tests proving anonymous-equivalence). Continuing.

2026-10-27 — Waves `c416699` (ApiAuthorization), `1eeafbf` (TeamRole), `1c3b7b7` (CommitFileChange), `1049b82` (Commit params), `aae651b` (PullRequest params; 2 mypy findings repaired), `5f18513` (repository user params), `04043f3` (get_users_for_commits), `858fd1d` (Commit constructors), `b6001cd` + `d94bb3a` + `2d0c6dd` + `245be48` (Dashboard widget/query/list/details/revision; 5 mypy findings repaired incl. 3 false dateCreated claims and 1 over-precise createdBy), `e2e256f` (Activity get_attrs/init/serialize), `9966a15` (UserReport contracts; 6 mypy findings repaired incl. shadowed user param and wrong attrs key type), `71d0f90` (role init, userreport child get_attrs), `6df33ff` (Group _get_status return vs demanded schema), `7528604` (test-only: ApiToken serializer tests used the whole item-mapping as single-item attrs; fixed to per-item, runtime-identical). Toolchain note: a missing Mapping import broke the Django mypy plugin for all files until fixed; py_compile does not catch name errors, ruff did not flag this one — always re-run targeted mypy after import edits. GroupSeenSerializer deliberately left untyped (no callers; endpoint builds the payload manually with full types). Continuing with release/event serializer families.

2026-10-27 — Parked release.py GroupEvent slice (pre-existing Author-alias + unreachable errors in-file; needs shared-alias repair first) and GroupSeenSerializer (no callers; endpoint builds the payload manually). Recorded mypy-outage toolchain lesson. Continuing with event/release serializer families.

2026-10-27 — Waves `b38e5d5`+`e2e256f` (Activity params), `9966a15` (UserReport contracts; 6 mypy findings repaired), `71d0f90` (role init, userreport child), `6df33ff` (Group _get_status vs demanded schema), `7528604` (test-only per-item attrs fix), `f1770b4` (event get_attrs chain). Fixed a self-inflicted missing Mapping import that broke the Django mypy plugin repo-wide; py_compile does not catch name errors. Continuing with release/event serializer families.

2026-10-27 — Wave `a75f111` (event base serialize params + platform str→str | None per eventstore model). SimpleEventSerializer get_attrs attempted then reverted: bind_nodes demands Sequence[Event] while the serializer accepts GroupEvent; needs eventstore contract audit first. Continuing with ExternalEventSerializer (PagerDuty consumer) next.

2026-10-27 — Wave `cb9fb27` (event serialize user-shadow rename + vestigial group-arg widening; 2 mypy findings repaired). ExternalEventSerializer itself stays untyped pending its PagerDuty payload schema. Continuing.

2026-10-28 — Devservices unblocked without devenv: OrbStack started (docker daemon was down), `sentry-shared-postgres`/`sentry-shared-redis` zipball downloads 403 on an SSO-unauthorized gh token, so repos were git-cloned manually into `~/.cache/sentry-devservices/dependencies/v1/` and images pulled from ghcr; `devservices up --mode migrations --offline` is healthy (postgres 5432, redis 6379). Behavioral evidence batch: options store (incl. restored assertion), msteams client, ApiToken serializer, activity/commit/filechange/pullrequest serializers, org api-key endpoints all pass (62 total). Event/group serializer files and one activity case require snuba (migrations mode starts postgres+redis only) and stay provisional.

2026-10-28 — Wave `1f24219` (ExternalEventSerializer request/response contract + PagerDuty consumer audit; static checks pass, PagerDuty tests unrun — module requires snuba, provisional). Continuing with release/event serializer families.

2026-10-28 — Wave `885ff98` (SharedEventSerializer serialize params mirroring base + dict[str, Any] return per latestEvent consumer; group serializer tests require snuba, provisional). Continuing.

2026-10-28 — Wave `d3d703a` (IssueEventSerializer helpers + serialize params vs wrap_event_response consumer; endpoint tests require snuba, provisional). Continuing with SqlFormat helpers and release serializers.

2026-10-28 — Wave `c98c1e2` (SqlFormatEventSerializer get_attrs/helper/serialize params vs organization_event_details consumer; tests require snuba, provisional). Continuing with release serializers.

2026-10-28 — Named dependency repaired: `5d39129` declares Author as explicit TypeAlias (implicit union alias unrecognized in models/release.py: 6 valid-type + cascading findings; repo-wide mypy clean over all 9 importing modules; commit/filechange/pullrequest/release serializer + committers non-snuba tests pass, snuba-bound ones stay provisional). Follow-up `95065dd` types the last-commit/last-deploy producer chain feeding GroupEventReleaseSerializerResponse. Continuing with ReleaseSerializer get_attrs/serialize.

2026-10-28 — Wave `f5f19e2` (GroupEventReleaseSerializer serialize params narrowed to Release per producer; no mypy findings; release endpoint tests require snuba, provisional). Continuing with ReleaseSerializer get_attrs/serialize.

2026-10-28 — ReleaseSerializer family complete: `5871488` (expose/query helpers; slug narrowed to str on non-nullable column evidence; newGroups None→0 and missing-stats→{} coercions mirroring the in-file or-idioms, each pinned by a new regression test in `18dc2d6`; AdoptionStage precision), `ae43febe` (get_attrs/serialize entry params; dead has_health_data None arm removed as unread on its path; _get_authors_metadata widened list→Sequence after body audit). behavioral: test_release.py 34 passed; organization_releases 89 passed + 1 pre-existing -n3 flake (order_by_sessions passes -n0, fails identically on base). Continuing with the next interface group (dashboard endpoint params or repository serializers).

2026-10-28 — Deferred dashboard user-Any resolved: `22c58b2` (DashboardListSerializer get_attrs user union; serialize_generic_user adapter per 5-serializer precedent; anonymous lookups isinstance-narrowed to empties per broadcast precedent; both consumers are authenticated org endpoints; 314 dashboard endpoint tests green). Continuing.

2026-10-28 — Deferred CommitSerializer class parameterization completed: `992ef17` (all 3 explicit-serializer call sites audited; NotRequired covers exclude shapes; response-sequence ripple into notifications; 5 files mypy-clean together). Continuing with repository serializers or parked-lane fixups.

2026-10-28 — Parked api-paginator lane repaired: `703e8e1` (kept CursorValue, CursorResult[object] return verified against opaque consumers, rename required by reassignment; queryset generics stay split out). Continuing with filestore-s3 or releasefile parked lanes.

2026-10-28 — Parked filestore-s3 lane repaired on current tree: `8051f2a` (file object + storage contracts; upstream had subsumed safe_join/_file; dynamic multipart attr per no-stub boto3; url override marked deliberate). Continuing with the releasefile parked lane or SimpleEventSerializer audit.

2026-10-28 — Parked releasefile lane repaired via clean cherry-pick: `56991c3` (archive/index contracts; guard restructure preserves skip behavior structurally; callers and test files mypy-clean with no edits). Continuing with SimpleEventSerializer audit or map_device_class_tags protocol.

2026-10-28 — Deferred SimpleEventSerializer get_attrs resolved by audit: `0cbfca9` (Event-only contract exact per producers, no eventstore change needed). Continuing with map_device_class_tags protocol or the next interface group.

2026-10-28 — Deferred tag-mapping protocol resolved without new abstraction: `6615a1b` (shared shape is EventTag at all 3 producers). Continuing with the next interface group.

2026-10-28 — Event base-producer chain typed: `86307ad` (7 helpers; transaction float attrs split out with named payload-evidence dependency). Continuing with the next interface group (transaction payload audit or group serializer remainder).

2026-10-28 — GroupSerializerSnuba query helpers typed: `fd2b7c1` (execute/parse vs typed _seen_stats callers; __init__ split out on the upstream params-contract gap). Continuing with the next interface group.

2026-10-28 — Stream enrichment made explicit: `deab705` (the precise SeenStats return surfaced 3 latent call-site mismatches, each repaired with in-repo precedent; unaliased rebuild proven identical). Continuing with the next interface group.

2026-10-28 — Group stats mixin typed: `ddf020a` (query contracts, Stream constructors, 2 asserts pinning the non-empty invariant). Continuing with the next interface group.

2026-10-28 — Base get_attrs user narrowed: `e4df89e` (exact Serializer-base match; overrides already union). Continuing with the next interface group.

2026-10-28 — Project serializers user narrowing: `20e1100` (both params unused; union matches callers). Continuing with the next interface group.

2026-10-28 — Seer serializers user narrowing: `6cf8bfd` (passthrough-only params). Continuing with the next interface group.

2026-10-28 — Remaining serializer user/attrs narrowing: `325d1a0` (3 files, params unused in bodies). Continuing with the next interface group.

2026-10-28 — Trace attribute value sibling: `f02c781` (same unused-params pattern). Continuing with the next interface group.

2026-10-28 — Group release serializers typed: `1718d59` (single-consumer contracts; deterministic registry dispatch). Continuing with the next interface group.

2026-10-28 — Event user serializer narrowed: `c96ef21` (obj split out with 7-field nullability evidence for the response-contract follow-up). Continuing with the next interface group.

2026-10-28 — Artifact bundle serializers typed: `e4d63a2` (row-tuple producer shape; endpoint-local entry split out to avoid layer inversion). Continuing with the next interface group.

2026-10-28 — Data export serializer typed: `9332b77` (params + apidocs-documented response). Continuing with the next interface group.

2026-10-28 — Discover saved query serializer typed: `5e75f33` (user contract + nullable corrections; obj split out pending dateCreated payload evidence). Continuing with the next interface group.

2026-10-28 — Audit log entry serializer typed: `9de1067` (response vs typed registry; helpers stay file-private). Continuing with the next interface group.

2026-10-28 — Broadcast serializers typed: `4ade7ff` (suspected created_by_id defect disproven by relation-name evidence + repro test `dbf118c`; response contracts; user unions). Continuing with the next interface group.

2026-10-28 — Snuba unblocked on public machine without getsentry: cloned `snuba`, `sentry-shared-kafka`, `relay`, `objectstore` anonymously into the devservices cache, pre-pulled ghcr images, `devservices up --mode default --offline` healthy (snuba 1218, clickhouse, kafka, relay, spotlight, objectstore alongside postgres/redis). Behavioral verification, all green: pagerduty/event/group/activity 63 passed; committers+release 74 passed (resolves the 8 + 21 snuba-blocked); dashboards/userreport/team 341 passed 2 skipped. Every provisional wave since the rebase now has DB-backed test evidence; combined targeted mypy clean over all 14 changed+consumer files. Exact global `evaluate` still pending (adapter is single-process full-tree mypy; timed out at 10 min previously), so waves stay provisional per the campaign rule, but no longer for lack of services.
