# Execution isolation — design gate (not implemented)

**Do not execute arbitrary agent-produced patches on the host or in this repository's GitHub Actions workflow.** Phase 1 only parses synthetic JSON and runs local unit tests.

## Requirements for a future runner

- Per-run ephemeral VM or equivalently isolated executor; a plain Python subprocess is not a security boundary.
- Read-only task snapshot and separate writable workspace.
- No provider keys, GitHub tokens, SSH agent, or production mounts inside task execution.
- Default-deny outbound network with an explicit task-specific allowlist, including DNS and metadata endpoint protection.
- CPU, memory, disk, wall-time, output, process-count, and network limits; terminate the entire process tree on timeout.
- Immutable task revision, container image digest, test command, and hash of submitted patch.
- Independent evaluator with withheld tests, immutable logs, and human review for security-sensitive tasks.
- Scrub secrets from logs and artifacts; never publish raw private repositories or real user data.
- Re-run identical tasks under equivalent resources and report confounders.

## First end-to-end gate

Before any real agent run, demonstrate with a disposable fixture that attempted file escape, network access, excessive output, process spawning, and timeout are all denied. Publish negative-test evidence, not just a configuration file.

## Measurement contract

For each task/agent pair record task revision, environment digest, verified result, elapsed seconds, provider cost (nullable), test evidence, failure category, and review outcome. Distinguish an unavailable metric from zero.

This document does not claim that a sandbox or agent adapters currently exist.
