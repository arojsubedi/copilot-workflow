# Planning

The [eng-planning skill](../skills/eng-planning/SKILL.md) turns a requested outcome into a repository-grounded implementation proposal. It owns research, design validation, sequencing, and convergence in one current plan. A coherent first draft is provisional: validation must be able to discover a better existing owner even when the draft never mentioned it.

Copilot may select this skill from the request and its description. Explicit `/eng-planning` invocation makes the workflow choice unambiguous; [source inspection](setup.md#verify-skill-selection) is optional. The sequence below describes the workflow once loaded.

```text
Requested outcome + target/evidence snapshot
        |
Inspect owners / callers / contracts / tests
        |
Provisional direction in parent context
        |
Validation gate, driven by consequential questions
        +-- repository falsification
        +-- when warranted: unanchored independent approach
        |                     -> compare/reconcile
        +-- when useful: adversarial critique
        |
Resolve challenges against evidence
        |
Coverage closure + affected evidence refresh
        |
Persist/update ONE active plan + final coherence
        |
Handoff (implementation needs explicit direction)
```

## Evidence and validation depth

Inspection establishes requested behavior, scope, owners, callers, contracts, tests, and verification commands before decomposition. Dependencies are followed while they can change the design. User-proposed means are candidates unless explicitly constrained; precedent is evidence rather than automatic authority. External research supplies current version-specific facts only when the decision depends on them.

A tiny, obvious change needs an internal evidence sanity check and a concise plan, with no required worker. Normal meaningful work challenges material assumptions against the repository. Meaningful/consequential planning requires repository falsification. Independent discovery is selected for consequential design commitments or framing risk; adversarial critique is selected when it can change an important conclusion. A large mechanically determined migration needs no invented alternatives, while a small new ownership boundary may warrant both perspectives. Depth follows ownership, contracts, new state or machinery, transitions, risk, and uncertainty rather than line count.

Validation establishes why behavior is required and what would defeat each major commitment. It searches mechanisms by responsibility, then compares actual semantics and consumers. Reuse is justified by ownership, not file count. New machinery needs a present responsibility; implied contracts remain binding, while imagined persistence, consumers, compatibility, and configurability do not become requirements. Existing variability can justify generality, but hypothetical future variants cannot.

Behavioral partitions, affected consumers, data/deployment transitions, and functional-first dependency order receive attention where they can alter the approach. Verification names evidence that distinguishes intended behavior from a plausible defect, such as mixed history for a latest-state rule, rather than merely promising tests.

## Independent perspectives and parent judgment

Maintained `explore` handles selective, bounded repository questions that can falsify assumptions: find existing interfaces for a responsibility, trace consumers, or locate an existing configuration or retry owner. Available semantic navigation is complemented by textual search for dynamic relationships. Bounded negative results do not prove whole-repository absence. [GitHub's built-in agents](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents)

For a consequential ownership/design question, the parent keeps its provisional direction private until a fresh `general-purpose` context derives an approach from the outcome, evidenced constraints, neutral repository facts, and unresolved questions. The worker receives no draft, chosen implementation, proposed names, parent verdict, or other worker conclusions. No accessible repository/session draft is persisted first. Only after the result returns does the parent compare directions. [Subagent contexts](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents#running-agents-as-subagents)

Safe dispatch requires both effective mutation restrictions and draft exclusion. Native Plan mode provides inherited project-edit protection; outside it, a fresh context needs effective read-only tools/permissions. Instructions alone provide neither a permission boundary nor filesystem isolation. An existing or automatically persisted draft must be excluded by the actual context/read scope, including session history. If that cannot be established, the parent retains repository falsification, discloses missing independent discovery, and does not claim equivalent validation. A worker that saw the draft supplied anchored critique.

After evidence work and any independent comparison, `rubber-duck` may see the provisional proposal and a discovered alternative to challenge framing, ownership, scope, scenarios, and verification. It supplies complementary-model critique when useful, subject to supported Claude/GPT sessions and critic availability. It is never the sole validator. [Rubber-duck support](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/rubber-duck)

The parent reconciles a relevant critique already in context, including one initiated by Copilot, instead of requesting an equivalent pass. Another challenge needs a materially different question/state, a proposal change that makes the critique stale, or a plausible ability to change the conclusion. No persistent critique state is needed.

The parent resolves disputed assumptions against requirements and repository contracts. Agreement counts and numeric confidence cannot defeat evidence; proposed reuse is rejected when its semantics violate a contract. Routine decisions remain autonomous. Only consequential questions that inspection cannot resolve go to the user.

## Coverage and freshness

Before a substantial/consequential plan is ready, every material requested behavior, evidenced requirement, and explicit constraint has an implementation owner/path and meaningful verification, or remains unresolved. Closure includes preserved contracts, consumers, behavior partitions, data/side-effect/rollout transitions, earned machinery, dependency order, and verification counterexamples. Individually sound decisions do not compensate for a forgotten requirement. Tiny work keeps this accounting implicit; the output needs no traceability matrix.

The parent retains repository identity/revision and relevant staged, unstaged and untracked evidence internally. Before persistence and handoff it checks whether affected content or material issue/remote facts changed, refreshing only invalidated assumptions, validation and coverage. Unchanged HEAD alone does not prove unchanged local evidence. Material gaps limit readiness; detected stale evidence cannot be presented as current.

## Artifact, resources, and authorization

Supported native Plan mode uses the actual current session's managed plan as its sole active artifact. Other surfaces use the explicit destination or default `<repository-root>/plan.md`. The parent identifies the active surface/location; it does not silently create both plans. Copilot's session facilities expose the current plan, and its best-practice flow separates planning from implementation. [Session plan](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices#plan-mode)

Native Plan mode restricts project changes and passes restrictions to delegated subtasks. Some uncertain shell and external/MCP operations remain possible, so normal authorization and tool restrictions still apply. It is not draft-read isolation or a complete sandbox. The skill does not automatically switch modes or enable plan-then-autopilot. [Plan-mode enforcement and limits](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#plan-mode)

An explicit repository-local destination may be blocked in native Plan mode. The workflow preserves the request, discloses pending persistence, and uses chat or an already managed session plan without a competing copy. A supported artifact-only transfer can establish the requested file as the sole active source and retire the former session plan from use. It never selects an implementation action merely to copy a plan.

After validation, closure and evidence refresh, the active plan contains only the chosen proposal, useful implementation rationale, dependency-oriented steps/phases, meaningful verification, and unresolved material questions. Revisions replace defeated assumptions in place. Worker transcripts, discarded designs and validation history create no extra artifact. The [plan examples](../writing/examples/plan.md) calibrate final prose rather than internal procedure.

The core skill owns lifecycle, depth, closure, evidence refresh, convergence, and handoff. Its single [validation reference](../skills/eng-planning/references/validation.md), read for meaningful and substantial validation, owns detailed challenges, neutral delegation, capability fallback, and evidence reconciliation. Supplementary Markdown is a supported Agent Skill resource; discovery does not establish that its instructions were read. The existing recursive installer manages it through ordinary ownership checks. [GitHub's skill resources](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)

Validation completion and plan acceptance do not authorize implementation. Planning stops at the proposal unless explicit implementation direction already covers the work. [Implementation](../skills/eng-implementation/SKILL.md) consumes the actual active plan alongside current code, without requiring a repository copy, and reconciles consequential invalidation in the same artifact before dependent changes.

[Planning quality cases](../tests/planning-quality-cases.md) evaluate semantic behavior in disposable contexts. Automated tests check resource ownership, installation, links, and bounded content contracts; they do not prove model behavior or actual Copilot context isolation.
