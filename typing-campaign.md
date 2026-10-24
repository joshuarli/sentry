# Sentry typing hillclimb

## Status: paused — 2026-10-24

### Resume

Resume the existing `typing-hillclimb` campaign from the last accepted source checkpoint `b628cbcf763bf36a8b1798dfb4ae9eab33a05c80`. First run:

```sh
git status --short --branch
```

Then reread current repository instructions and perform the parent steering checkpoint before selecting work from the parked branches. Do not treat branch preservation commits as accepted source work, or retry the rejected query-construction candidate without addressing its measured blockers.

Use only GPT-6-Luna High for campaign agents and remove Claude-specific guidance. If environment setup is needed, follow `devenv/sync.py` directly without invoking the `devenv` tool. Getsentry is unavailable on this machine; when its checkout is absent, skip Getsentry-specific verification. Do not run formatters, change CI, or push.

### State

The integration branch is `typing-hillclimb`. Its accepted source tip is `b628cbcf763bf36a8b1798dfb4ae9eab33a05c80` (tree `b6ff996179e34f36b2e69b8cc4d722eb4d06db5d`); later winddown commits on this branch only update this campaign document. The pinned upstream comparison base remains `503ad2e4e2a208a87d768a3e91bcfb55a778e7ba`. The branch has local commits ahead of `origin/typing-hillclimb`; nothing was pushed.

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

The last accepted source promotion remains `b628cbcf763`. No new source work was merged during winddown. Campaign status, exact results, and the remaining decision are recorded here; the optional raw evaluator report is not required to resume.

### Direction

The migration has delivered seven accepted source promotions since the earlier checkpoint, including concrete contracts in serializers, integrations, query helpers, and adapters. Core typing completion and precision completion remain separate objectives.

The limiting stage remains exact global acceptance and proposal correctness, not proposal supply. The latest candidate reduces aggregate debt but is rejected for local regressions. Preserve the corrected evaluator; do not reopen evaluator, cache, or reporting work without a demonstrated unsafe acceptance or invalid measurement. On resume, inspect candidate branches against the accepted source tree and select one coherent, testable source wave. Keep intermediate changes provisional until exact combined-tree acceptance.

Use one coordinator and at most two preparation lanes. Preserve the pinned comparison base and locked dependencies. If required services remain unavailable, record the blocker once and continue with independent, testable work.

### Open lanes

There are no active lanes and no remaining campaign worktrees. The unique dirty proposals found during winddown were committed to their existing lane branches or new `typing-winddown-*` branches so the checkouts could be removed. These are preservation commits, not source acceptance. Local edits identical to the accepted source tree were discarded from their worktrees. All branches listed below are parked; inspect their commit and diff before selecting any for a retry. Recreate a checkout at `.work/wt/<lane>` from its branch when needed. Retry only after reviewing current callers and tests, then run focused checks and exact wave acceptance.

The exact rejected candidate is `typing-wave-20261024-query-construction`. Its known blockers are recorded above. Other historical branches were not individually re-evaluated during winddown; do not infer acceptance from their branch names or earlier lane notes.

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

The closeout removed 101 campaign worktrees using Git's normal worktree removal and left only the integration checkout. Branch refs remain available for recreation. The rejected candidate report was losslessly compressed locally, with its inventory and canary output retained alongside it; the handoff above contains the facts required to resume.

Disk availability rose from 68 GiB to 178 GiB, recovering 110 GiB. The earlier requested ~300 GB target was not met. The large completed-evaluation trees and snapshots under `.work/tmp` remain because automatic review previously rejected their bulk removal; that deletion was not retried. The latest raw report was compressed losslessly. `.work/` is ignored by `.git/info/exclude` and resides on APFS.

The only retained worktree is the root integration checkout. It has seven owner-owned changes that were not modified or staged:

- `src/sentry/similarity/__init__.py`
- `src/sentry/templatetags/sentry_helpers.py`
- `src/sentry/unmerge.py`
- `src/sentry/utils/datastructures.py`
- `src/sentry/utils/eventuser.py`
- `tests/sentry/templatetags/test_sentry_helpers.py`
- `tests/sentry/utils/test_datastructures.py`

### Not started

No next source wave is selected. On resume, the coordinator should perform the parent steering checkpoint, compare parked proposals to the accepted source, and select one testable group. No owner decision is pending during this pause.

### Verified

- `git worktree prune` completed; the worktree list contains only the root integration checkout.
- All lane worktrees were clean before normal removal. Unique uncommitted proposals were committed to their lane branches; the only preserved unaccepted candidate, `a8125f3e92f87d4a0156dc9761e1b1849ff97ca2`, has its own branch.
- The root virtualenv has executable Python and pytest. No formatter was run.
- The root checkout is intentionally not clean because of the seven owner-owned changes above; the closeout did not alter them.
- The Stop hook configuration was inspected manually. `/hooks` was not exposed in this API session. `codex-campaign-closeout.py begin` reports closeout active; the root checkout is a baseline worktree and the guard did not require an allowance. Directly invoking its `hook` command returned a block because this API call did not include the Stop-event JSON; no synthetic event was supplied.
- Process checks found no campaign pytest, mypy, or evaluator process; no lane agents remain active. The user crontab and LaunchAgents contain no typing-campaign wakeup.
- The document path audit found only `.work/tmp`, which is under the ignored repo-local `.work/` directory. The branch list in this handoff matches `git branch --no-merged typing-hillclimb`.
- Resume rehearsal passed in a clean environment: the first command, integration branch, accepted source commit, rejected-candidate branch, and this handoff all resolved.

### Campaign log

2026-10-24 — Paused after exact rejection of the query-construction candidate; preserved unique proposals on branches, removed 101 worktrees, and reclaimed 110 GiB.
