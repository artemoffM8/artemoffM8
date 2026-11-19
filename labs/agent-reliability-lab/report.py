"""Strict offline metrics for synthetic agent evaluation records."""
import json
import sys
from collections import defaultdict
from pathlib import Path

AGENTS = {"hermes", "codex", "claude-code"}

def summarize(records):
    if not isinstance(records, list):
        raise ValueError("Expected list of runs")
    seen = set()
    groups = defaultdict(list)
    for row in records:
        if not isinstance(row, dict):
            raise ValueError("Run must be an object")
        task = row.get("task_id")
        agent = row.get("agent")
        success = row.get("verified_success")
        cost = row.get("cost_usd")
        if not isinstance(task, str) or not task.strip() or agent not in AGENTS:
            raise ValueError("Invalid task or agent")
        if type(success) is not bool:
            raise ValueError("verified_success must be boolean")
        if cost is not None and (type(cost) not in (int, float) or
                                 not 0 <= cost < float("inf")):
            raise ValueError("Invalid cost")
        key = (task, agent)
        if key in seen:
            raise ValueError("Duplicate task/agent run")
        seen.add(key)
        groups[agent].append(row)
    output = {}
    for agent, rows in sorted(groups.items()):
        successes = sum(row["verified_success"] for row in rows)
        known_costs = [row["cost_usd"] for row in rows if row["cost_usd"] is not None]
        total_cost = round(sum(known_costs), 6) if len(known_costs) == len(rows) else None
        output[agent] = {
            "runs": len(rows),
            "verified_successes": successes,
            "success_rate": round(successes / len(rows), 4),
            "total_cost_usd": total_cost,
            "cost_per_verified_success_usd": (
                round(total_cost / successes, 6)
                if total_cost is not None and successes else None
            ),
        }
    return output

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 report.py runs.json")
    print(json.dumps(summarize(json.loads(Path(sys.argv[1]).read_text())), indent=2))
