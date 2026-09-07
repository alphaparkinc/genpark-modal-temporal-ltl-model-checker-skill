"""
MCP Server for Modal Temporal LTL Model Checker Skill
"""

import json
import sys
from client import KripkeStructure, LTLModelChecker

def handle_call(name: str, args: dict) -> dict:
    if name == "check_ltl_safety":
        states = args.get("states", ["S0"])
        init = args.get("initial_state", "S0")
        k = KripkeStructure(states, init)
        for t in args.get("transitions", []):
            k.add_transition(t[0], t[1])
        for s, p in args.get("labels", {}).items():
            for prop in p:
                k.add_label(s, prop)
        c = LTLModelChecker(k)
        safe, ce = c.check_globally(args.get("property", "safe"))
        return {"satisfied": safe, "counterexample": ce}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_call(req.get("method"), req.get("params", {}))
        sys.stdout.write(json.dumps(res) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
