# Agent Reliability Lab — Phase 1 (staging)

A reproducible, provider-neutral **evaluation harness prototype** for coding agents. This folder is staged in a draft branch of the profile repository because a dedicated repository has not yet been provisioned. It is **not** an existing standalone product or a completed comparison of Hermes, Codex, and Claude Code.

## Scope

Phase 1 validates result schemas and computes comparable metrics from synthetic fixtures. It does **not** invoke models, execute arbitrary agent-generated code, or assert any real agent's quality.

## Proposed protocol

- Pin the task revision, test suite, environment, time budget (2 hours), and monetary cap ($5).
- Give each agent identical input and tool access where feasible; disclose differences.
- Run submitted patches in an isolated sandbox with network restrictions and resource limits.
- Score task success using independent tests and human review, not the agent's self-report.
- Record elapsed time, cost, token usage where available, failed tool calls, and policy violations.
- Preserve raw evidence and report missing metrics as `null`, never zero.

## Quick check

```bash
cd labs/agent-reliability-lab
python3 -m unittest discover -s tests -v
python3 report.py fixtures/sample_runs.json
```

Requires Python 3.11+ and no external packages. All fixture values are synthetic.

## Phase 1 acceptance

1. Reject unknown agents, duplicate task/agent runs, negative costs, and inconsistent success evidence.
2. Compute success rate and cost per verified success without division-by-zero.
3. Distinguish missing cost from zero cost.
4. Run offline in CI without provider keys, network, or executable model outputs.

## Next phase

Move into a dedicated repository after review; add task manifests, containerized execution, immutable result artifacts, and adapters for Hermes/Codex/Claude Code. Do not claim real-world benchmark results before independent runs.
