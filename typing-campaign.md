# Sentry typing hillclimb

## Status: paused — 2026-10-24

### Resume

On the owner's next request, resume the existing typing migration from accepted source checkpoint `b628cbcf763bf36a8b1798dfb4ae9eab33a05c80`. First run:

```sh
git status --short --branch
```

Reread repository instructions and perform the parent steering checkpoint. Preserve the owner's source changes in the integration checkout. Fetch current GitHub master and rebase the typing source in a separate clean worktree, then establish the fixed policy baseline before selecting a parked proposal. The last fetched `upstream/master` was `86b1728a40fc57fd64ca6fb5e7c892b17c061b8c`; the campaign source has not been rebased onto it.

Use only GPT-6-Luna High for campaign agents and remove Claude-specific guidance. If environment setup is needed, follow `devenv/sync.py` directly without invoking the `devenv` tool. Getsentry is unavailable on this machine; when its checkout is absent, skip Getsentry-specific verification. Do not run formatters, change CI, or push.

### State

The integration branch is `typing-hillclimb`. Its accepted source tip is `b628cbcf763bf36a8b1798dfb4ae9eab33a05c80` (tree `b6ff996179e34f36b2e69b8cc4d722eb4d06db5d`). Commits after that source tip only update this campaign document. The prior fixed policy comparison used base `503ad2e4e2a208a87d768a3e91bcfb55a778e7ba`. Current fetched `upstream/master` is `86b1728a40fc57fd64ca6fb5e7c892b17c061b8c`; no source rebase or new baseline was done before this winddown. The local branch is ahead of `origin/typing-hillclimb`; nothing was pushed.

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

The last accepted source promotion remains `b628cbcf763`. No new source work was merged during this winddown. Seven owner-owned source and test files remain modified in the integration checkout. Keep them intact when resuming. The optional raw evaluator report is not required to resume.

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

- `git worktree prune` completed; the worktree list contains only the root integration checkout. No additional cleanup candidate existed.
- The 143 unmerged branch refs exactly match the parked branch list. Branches were preserved; none was deleted.
- All lane agents reported completion. Process, user crontab, and LaunchAgents checks found no campaign job or wakeup.
- `codex-campaign-closeout.py begin` succeeded. The configured Stop hook points to `codex-campaign-closeout.py hook` and has a trusted configuration hash. The `/hooks` UI command is not exposed in this API session, so it could not be run here. A direct hook invocation needs Stop-event JSON and was not fabricated.
- The root virtualenv has executable Python and pytest. No formatter was run.
- The root checkout remains dirty only in the seven owner-owned files listed above. The campaign did not modify or stage them.
- `.work/` is ignored through `.git/info/exclude`; `df -h .work` confirmed it resides on APFS.
- Current fetched master is `86b1728a40fc57fd64ca6fb5e7c892b17c061b8c`; the source branch remains unrebased.
- Resume rehearsal passed in a clean environment. The first command, accepted source commit, current master commit, rejected candidate branch, and handoff document all resolved.

### Campaign log

2026-10-24 — Froze the campaign after the query-construction rejection, confirmed all 143 unmerged branches are recorded as parked, and verified that no additional worktrees or running lanes remain. Preserved seven owner-owned changes and recorded the current-master rebase as the next resume step.
