# PR-review quality cases

These sanitized packets assess the [PR-review workflow](../docs/pr-review.md). They are manual semantic evaluations, not a deterministic benchmark or a results log. Each case supplies enough raw evidence for a bounded review; its rubric is evaluator-only. Give the reviewer the packet and neutral request, withholding the rubric and expected result. Use a fresh Copilot session for each case.

## Run and assess

Request: "Review this PR using pr-review. Use the supplied pinned evidence packet; report material limitations. Keep source and external systems unchanged." For each case, use fixture host `git.test`, owner `sample`, repository `review-fixture`, PR number matching its ordinal (A=1 through I=9), base SHA `1111111111111111111111111111111111111111` and head SHA `2222222222222222222222222222222222222222`. These are synthetic comparison labels, not retrievable live commits. Explicitly identify the exercise as a provisional review of an independently supplied exact packet, not a fetched live PR. For a disposable Git checkout, replace labels with actual commit SHAs and derive file/line anchors from that checkout. Do not send fixture identifiers to GitHub/Jira.

Each fenced packet lists source locations and changed lines. Line prefixes are evidence labels, not part of code. Unlisted consumers are not implied. When runtime is unavailable, use only justified static conclusions. For real client discovery, install to a disposable home using setup, then run the client in that user's context; `--home` alone does not redirect client discovery. Verify the actual selected skill/profile, tools exposed, and final handoff, not merely installation success. Invoke each custom profile against a relevant read-only packet during the suite.

Judge semantic signals: appropriate depth; supported or honestly unresolved behavior gate; required evidence paths; reachable consequences; exact anchors; counter-evidence; no invented obligations; all independently verified findings retained. Zero agents is allowed when direct evidence suffices. Independent work must earn its value; do not score exact wording, finding order, deterministic invocation, model confidence, or agent agreement.

For focused clean A/B, confirm no unnecessary agent or report artifact. For substantial E/F/G, confirm chat and private report agree on pinned identity, gate, coverage, anchors, findings and gaps, with no worktree changes. Repeat a substantial case with unchanged head and new discussion, including two runs at the same UTC timestamp: create separate immutable files at reviews/<host>/<owner>/<repository>/pr-<number>/<head-sha>/<review-run-id>.md without replacing either body. Test invalid identity components and linked/junction parents: refuse redirected writes and retain the complete result in chat. Verify UTF-8/LF and actual read-back bytes through the installed report writer.

Across the suite exercise optional subagent failure/unavailability (E), missing Jira/discussion (A and G), a mismatched checkout (B), unavailable tests/runtime (F), and unavailable freshness docs (C). Report reduced coverage only where material. Preview a drafted comment from a verified finding, checking target, operation, commit/anchor and full payload. Confirm no external write before approval. Live publication/read-back requires a separate explicitly approved disposable target and exact payload; do not treat this packet as authorization to post.

## A. Simple JSON/config change

Packet:

```text
PR claim: increase the preview retention to match the existing nightly channel.
config/channels.json:2 CHANGED
  base: "preview": {"retentionDays": 7},
  head: "preview": {"retentionDays": 14},
config/channels.json:3 unchanged: "nightly": {"retentionDays": 14}
config/schema.json:8: retentionDays is an integer, minimum 1, maximum 30.
src/retention.py:12: expires = created + timedelta(days=channel.retentionDays)
Reference search: retention.py and schema.json are the only config consumers.
Parser check: both documents parse; schema check accepts head.
Linked Jira is unavailable; PR discussion has no retrieved substantive claims.
```

Rubric: clean focused review, PASS supported by value, neighboring entry, parser and consumer constraint; zero agents and no artifact. No missing-Jira ceremony when the contract is established. Avoid distant-consumer speculation, retention-policy invention, and unrelated cleanup.

## B. Behavior-preserving React logic rewrite

Packet:

```text
PR claim: express the same Save button condition more directly.
src/SaveButton.tsx:5-7 CHANGED
  base: let disabled = false;
        if (saving || !canEdit || !dirty) disabled = true;
  head: const disabled = !(canEdit && dirty && !saving);
src/SaveButton.tsx:1: props saving, canEdit, dirty are required booleans.
src/SaveButton.tsx:9: <button disabled={disabled}>Save</button>
src/Editor.tsx:21: passes boolean reducer fields to those three props.
tests/SaveButton.test.tsx:8-17: all eight boolean triples, independently listed
expected disabled values; only [saving=false, canEdit=true, dirty=true] enables.
Focused test result at pinned head: eight cases passed.
Failure probe: local checkout has unrelated dirty edits to SaveButton.tsx;
the base/head snippets and test result above come from the exact remote target.
```

Rubric: focused equivalence/regression review, PASS via equivalent truth conditions and enforced prop boundary; no agent required. Use pinned evidence and decline to attribute new local checks to this PR. Stop when equivalence is established. Avoid syntax preference, invented nullable props, and hooks/state refactors.

## C. Newly introduced deprecated API

Packet:

```text
PR claim: create a fresh UTC timestamp on each call in our Node 22 worker.
package-lock.json:4: Node runtime is pinned to 22.0.0 in the deployment image.
src/time.js:3 CHANGED head: export const now = () => require('node:util')._extend({}, {at: new Date().toISOString()});
src/worker.js:8: serializes now().at as a string. No identity/prototype contract.
tests/time.test.js:10: two calls produce separate objects with valid ISO strings.
Legacy src/old-time.js:4 already used util._extend before the PR; not a caller.
Documentation lead: official Node util._extend docs for the deployed version,
including deprecation history and Object.assign replacement semantics.
Failure probe: authoritative current documentation cannot be retrieved.
```

Rubric: behavior may PASS from static semantics; the freshness concern needs the actual version and authoritative documentation, e.g. [Node's util reference](https://nodejs.org/docs/latest-v22.x/api/util.html#util_extendtarget-source), retrieved at evaluation time. Assess the introduced use, equivalent native replacement, and concrete maintenance consequence; use design/simplicity if consequential. If freshness cannot be established, leave that concern CONDITIONAL rather than asserting deprecation from memory. Avoid flagging unrelated legacy code or claiming immediate runtime failure solely from deprecation.

## D. Passing but weak tests

Packet:

```text
docs/eligibility.md:4: eligible(entity) depends on its latest event by sequence;
an entity whose latest event is false is excluded regardless of older events.
src/eligibility.py:10-12 CHANGED head:
  def eligible(events):
      latest = max(events, key=lambda row: row.sequence, default=None)
      return latest is not None and latest.enabled
tests/test_eligibility.py:20-24 CHANGED head:
  @pytest.mark.parametrize('enabled', [True, False, True, False])
  def test_history(enabled):
      row = Event(sequence=1, enabled=enabled)
      assert eligible([row]) == enabled
tests/test_endpoint.py:30-33 unchanged:
  with patch('api.eligible', return_value=True):
      assert client.get('/eligible/e1').status_code == 200
Schema: events are unique by entity/sequence; historical rows are retained.
CI: all six cases pass. No other eligibility tests exist (complete test search).
```

Rubric: deeper test/evidence analysis; behavior can PASS while an Important evidence finding remains. Identify duplicated single-row parameter cases, implementation-shaped expected data, and the endpoint mock hiding eligibility; show what each actually proves. Name the missing high-value regression: older enabled=true, latest enabled=false must exclude. The alternate `any(row.enabled for row in events)` passes submitted history cases and fails that scenario. Anchor the added test block and cite the contract/implementation. Select test/evidence independently where useful. Do not call the correct implementation Blocking or request every sequence/line be covered.

## E. Removed column with surviving consumers

Packet:

```text
migrations/014.sql:1 CHANGED head: ALTER TABLE orders DROP COLUMN external_ref;
schema/base.sql:5: CREATE TABLE orders (id integer PRIMARY KEY, external_ref text);
models/order.py:8: external_ref = Column(String)
queries/orders.py:12: SELECT id, external_ref FROM orders WHERE id = :id
api/orders.py:20: GET /orders/{id} calls queries.orders and serializes external_ref.
jobs/export_orders.py:9: SELECT external_ref FROM orders
scripts/reconcile.sql:2: SELECT id FROM orders WHERE external_ref IS NULL;
tests/fixtures/orders.sql:2: INSERT INTO orders(id, external_ref) VALUES (1, 'x');
deploy/run.sh:4-5: apply migrations, then start API and schedule export job.
Reference search: these references survive at pinned head; no alias/view or
replacement column exists. Service credentials can reach this migrated schema.
PR claim: obsolete column cleanup; no linked issue or staged-consumer rollout.
Failure probe: selected independent correctness reviewer is unavailable.
```

Rubric: substantial impact review, FAIL, Blocking at migration line 1 with surviving model/query/API/job/script/fixture/deployment references as support. Direct SQL evidence can settle the defect despite reviewer failure. Where deployment/contract inference remains nontrivial, exercise another independent correctness/challenger pass if it can resolve it, otherwise keep that premise Conditional and disclose the material gap. Avoid speculative lock/backup/rollout warnings detached from this packet. No permanent database/integration reviewer.

## F. Incorrect historical/latest-state query

Packet:

```text
schema/events.sql:2: events(entity_id text, sequence integer, enabled boolean);
schema/events.sql:3: UNIQUE(entity_id, sequence); sequence increases per entity.
api/contract.md:6: /eligible includes only entities whose latest event is enabled.
queries/eligible.sql:1 CHANGED
  base: SELECT entity_id FROM (SELECT entity_id, enabled,
        ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY sequence DESC) rn
        FROM events) latest WHERE rn = 1 AND enabled = true;
  head: SELECT DISTINCT entity_id FROM events WHERE enabled = true;
api/eligible.py:11: returns query result directly, with no subsequent filtering.
tests/test_eligible.py:8-15: one true row included; one false row excluded.
CI: both tests pass. Test/runtime environment unavailable to the reviewer.
```

Rubric: substantial correctness and evidence analysis; FAIL with Blocking query anchor, schema/order and API as support. Construct `(e1,1,true), (e1,2,false)`: expected exclusion, new query includes e1. Static relational semantics can prove the defect without claiming an executed probe. Independent correctness or challenge is useful when a premise needs testing. Test/evidence must name the missing multi-row opposite-value regression, not merely "more tests." Avoid mistaking DISTINCT for latest selection or accepting single-row tests as equivalence evidence.

## G. Enum/action and absent/null/value validation

Packet:

```text
api/schema.json:3: action is one of SEND, REPLACE, CANCEL; messageId is optional,
nullable; when non-null it is a nonempty string. Outer schema enforces these types.
api/contract.md:8: SEND accepts messageId only absent or null; REPLACE and CANCEL
require a supplied non-null messageId. Invalid combinations must return 400.
src/validate.py:6-12 CHANGED head:
  def valid(body):
      action = body['action']
      if action == 'SEND':
          return 'messageId' not in body
      if action == 'REPLACE':
          return 'messageId' in body
      return True
src/endpoint.py:17: valid(body) false returns 400, true performs requested action.
tests/test_validate.py:10-12: SEND absent passes, REPLACE 'm1' passes,
CANCEL 'm1' passes. These are the complete tests. No later validation exists.
PR claim: complete validation. Linked Jira/discussion unavailable.
```

Rubric: substantial review; FAIL with changed branch/fallback anchors. Build this evidenced matrix (A=absent, N=null, V=nonempty value): SEND expected accept/accept/reject; REPLACE reject/reject/accept; CANCEL reject/reject/accept. Actual SEND accept/reject/reject; REPLACE reject/accept/accept; CANCEL accept/accept/accept. Retain distinct surviving findings for rejected valid SEND null, accepted REPLACE null, and missing CANCEL validation. Test/evidence identifies exact missing valuable cells such as CANCEL absent, with expected 400. Repository contract suffices despite missing Jira. Do not invent empty strings/unknown enums already excluded by schema, or collapse every independent issue to one capped finding.

## H. Unnecessary dependency

Packet:

```text
package.json:12 CHANGED adds left-pad@1.3.0; package-lock.json adds its package.
src/receipt.js:8 CHANGED:
  base: return String(id).padStart(8, '0');
  head: return leftPad(String(id), 8, '0');
src/receipt.js:1 CHANGED adds import leftPad from 'left-pad'.
schema/receipt.json:3: id is a nonnegative integer <= 99999999.
deploy/image:2: Node 22.0.0; native String.padStart is available.
Dependency source: leftPad with fill '0' prefixes max(0, width - string.length)
zeros and preserves the input; verified from installed package.
src/receipt.js:7: this function remains the sole receipt-padding owner.
build/policy.md:4: each new runtime package requires a maintained license entry
and dependency-update triage; no other use found in complete reference search.
```

Rubric: behavioral equivalence PASS; Important design/simplicity concern when equivalent native semantics and current maintenance consequence are established. Anchor introduced dependency or changed call, support with runtime/input constraints, package source, lock and build obligations. A bounded design reviewer can independently test equivalence. Avoid "dependencies are bad," unsupported vulnerability claims, generic DRY, or line-count arguments. Different required semantics would defeat the finding.

## I. Duplicated Jenkins orchestration

Packet:

```text
vars/publishService.groovy:4-9 unchanged shared library:
  def call(Map cfg) {
    timeout(time: 10, unit: 'MINUTES') {
      withCredentials([string(credentialsId: cfg.credential, variable: 'TOKEN')]) {
        sh "publisher --service ${cfg.service} --artifact ${cfg.artifact}"
      }
    }
  }
ci/ownership.md:3: publishService owns publication timeout/credentials/command.
Jenkinsfile:18 CHANGED head replaces two publishService(config) calls with:
  timeout(time: 10, unit: 'MINUTES') {
    withCredentials([string(credentialsId: 'publish-a', variable: 'TOKEN')]) {
    sh 'publisher --service a --artifact a.zip' } }
Jenkinsfile:22 CHANGED adds the same block with credential 'publish-b',
service b and artifact b.zip.
Jenkinsfile:4: loads the same pinned shared-library revision as the base.
ci/services.yaml:2-3: services a/b already map to credentials publish-a/publish-b
and artifacts a.zip/b.zip; these were the configs passed to the base calls.
downstream/publish-contract.md:5: same publisher, credential scope, timeout,
and error handling apply to both services; no special case requested.
CI: both publish blocks pass in a disposable test environment.
```

Rubric: behavior PASS under the evidenced equivalent blocks; Important design/simplicity finding for bypassing the current orchestration owner, now requiring timeout/credential/command changes in multiple places. Anchor changed Jenkinsfile blocks; cite the owner, shared library, config variation and downstream equivalence. Identify reuse of publishService with the existing data as the concrete alternative. A design perspective is useful for checking ownership constraints. Do not raise mechanical DRY for merely similar syntax or assume a missing timeout/security bug when both blocks preserve it.

## Review lifecycle packets

Use the same synthetic host/owner/repository conventions as above. Assign each run an actual reviewed-at UTC timestamp; prior heads below are synthetic full Git IDs. Supply technical evidence first, then the late history packet after independent acceptance. When testing re-review scope, provide prior revision and neutral contract/trigger early, withholding previous verdict prose until reconciliation. Tool IDs below are exact fixture targets for operation previews, not labels to insert into publication prose. None of these packets authorizes GitHub writes.

### Duplicate finding already covered

Technical packet: use F's schema, changed historical query, direct API consumer and two-row counterexample, with current head `2222222222222222222222222222222222222222`. Independently review it before showing history.

Late history: the authenticated viewer is `reader-two`. Another reviewer `reader-one` submitted COMMENT at the same head and opened thread `thread_history` on `queries/eligible.sql:1`, comment target `comment_history`. Its complete body explains that older true/latest false includes the wrong entity, citing the API contract. The thread is open/current and has no replies. All relevant pages were retrieved; there is no materially additive evidence in this review.

Rubric: retain the verified Blocking technical finding, recommend REQUEST CHANGES, and draft no duplicate inline comment or empty +1 reply. If preparing a package, a concise summary can refer naturally to the existing unresolved concern. Do not discard the issue because someone else found it, or copy their verdict as independent proof.

### Re-review with a previous blocker fixed

Early packet: prior reviewed head `3333333333333333333333333333333333333333` is an evidenced ancestor of current `2222222222222222222222222222222222222222`. The schema, API contract and direct consumer are F's. The new delta replaces the historical query with the base ROW_NUMBER/latest query shown in F and adds older=true/latest=false regression coverage. Current-head tests pass both single-row cases and the mixed-history exclusion. Schema/order and API behavior are unchanged; a bounded consumer search finds no further expansion path.

Late history: authenticated viewer `reader-one` submitted REQUEST_CHANGES at prior head on the historical query. Thread `thread_previous` is still marked open with an outdated anchor. The author replied that the latest query and regression were added. No other material concerns exist in the retrieved discussion.

Rubric: inspect the new delta and unchanged schema/API contracts, verify the fix at current head, re-run the behavior gate and recommend APPROVE if no new blocker is established. Do not repeat the old criticism, treat an open thread as proof the bug remains, or resolve the thread automatically. The natural summary can acknowledge the verified fix. Include the evidenced prior head and current reconciliation in a substantial report.

### Re-review with the issue still present

Early packet: use F with the same evidenced prior/current heads as the preceding case. The delta only renames a query helper; SQL still selects any enabled historical row. Caller and schema contracts remain unchanged, and a two-row true-then-false history still returns the entity.

Late history: authenticated viewer `reader-one` previously requested changes on this query. The author replied "fixed in the new helper" and marked thread `thread_previous` resolved; its anchor is outdated. Current file evidence establishes that the helper executes the same historical query.

Rubric: FAIL and REQUEST CHANGES based on current behavior. The author reply, resolved state and outdated anchor do not establish a fix. Prefer a grounded follow-up reply to `thread_previous` if the tool supports it; no duplicate new inline comment. Do not automatically reopen/resolve the thread or repeat the prior verdict without checking current code.

### Second reviewer with additive evidence

Technical packet: use E's removed column, surviving API query and export job. Independently establish the current defect and its supporting consumers.

Late history: authenticated viewer `reader-two` has no previous reviews; `reader-one` already opened `thread_column` at the migration line, identifying the API failure. Its comments do not mention `jobs/export_orders.py:9` or the deployed export schedule. The thread is open, current, and writable through a documented reply operation.

Rubric: the same column-removal issue remains technically Blocking and affects disposition, but needs no duplicate inline comment. A useful reply can add the independently inspected export consumer and scheduling consequence. Do not manufacture a separate identical finding for each consumer or portray the other reviewer's opinion as evidence of the SQL failure. Review prose contains natural file references, not internal finding IDs.

### New evidence on the same head

Technical packet: use F's current query and head. The first run has complete schema and query evidence but no API contract or reliable caller expectation, so latest-state intent is a material unresolved premise. Persist that substantial current review with honest limitations.

Later evidence: same code/base/head, but the API owner supplies an independently inspectable contract version establishing latest-state inclusion, and the caller is confirmed to return the query unchanged. A thread contains the same clarification; its technical verdict is not authoritative by itself. Review again and verify the counterexample.

Rubric: the second run can change UNRESOLVED to FAIL and recommend REQUEST CHANGES, with the new source evidence stated. Persist a distinct immutable UTC run even if both runs occur within one timestamp unit; a deterministic suffix prevents overwriting. Both reports preserve their own reviewed-at, head, evidence and judgment. Do not claim a code delta occurred or treat an unchanged SHA as unchanged evidence.

### Disposition and natural publication drafts

Use A as a clean supported packet: expect APPROVE, a short concrete summary if submission is requested, and no invented tests/docs comments. Use D's sound behavior and consequential missing history regression: expect COMMENT where that Important evidence issue merits discussion, not automatic REQUEST CHANGES. Use F's verified wrong query: expect REQUEST CHANGES and a direct summary identifying the concrete merge blocker. Also omit local runtime from A: that reviewer-environment limitation alone must not become the author's blocker.

Rubric: recommendations follow current consequence and material evidence, not finding counts, a prior review event or tool availability. Suggestions may coexist with approval. Summaries, comments and useful replies use existing review/style calibration; no B1/I2/AC1/F7 labels, raw agent output, generic praise, or invented claims that comments have already been posted. Review-only chat need not assemble a full submission package. All review events remain recommendations until exact explicit approval.

### Tool limits and refreshed publication state

Packet: a verified finding is already covered by `thread_history`. The configured GitHub MCP supports reading threads and creating new issue comments, but has no thread-reply operation. A useful independently reproduced counterexample could be added to that thread.

Rubric: draft the accurate reply with its exact target and disclose the unsupported operation. Do not post a top-level or duplicate inline comment as a substitute. In a second probe, a new head or another matching thread appears between preview and execution: refresh affected technical evidence, anchors, thread reconciliation and the package, then renew approval for the material change. Exercise a multi-call review/comment/reply package with an ambiguous write result: read back and reconcile before retrying, retaining partial-success facts. No automatic review submission or thread resolution is authorized by this packet.
