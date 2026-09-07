"""
Modal Temporal LTL Model Checker Skill Client
Pure Python Standard Library implementation of Linear Temporal Logic (LTL) Model Checking (Pnueli).
Verifies Safety invariants (Globally G), Liveness invariants (Finally F), and Request-Response (G(p -> Fq))
across agent Kripke state transition structures.
"""

from typing import List, Dict, Any, Tuple, Optional, Set


class KripkeStructure:
    def __init__(self, states: List[str], initial_state: str):
        self.states = states
        self.initial_state = initial_state
        self.transitions: Dict[str, List[str]] = {s: [] for s in states}
        self.labels: Dict[str, Set[str]] = {s: set() for s in states}

    def add_transition(self, src: str, dst: str):
        if src in self.transitions and dst in self.states:
            self.transitions[src].append(dst)

    def add_label(self, state: str, prop: str):
        if state in self.labels:
            self.labels[state].add(prop)


class LTLModelChecker:
    def __init__(self, kripke: KripkeStructure):
        self.kripke = kripke

    def check_globally(self, prop: str) -> Tuple[bool, Optional[List[str]]]:
        """Verify safety invariant G(prop): prop holds in all reachable states."""
        visited = set()
        queue = [[self.kripke.initial_state]]

        while queue:
            path = queue.pop(0)
            curr = path[-1]
            if prop not in self.kripke.labels[curr]:
                return False, path  # Counterexample trace

            visited.add(curr)
            for nxt in self.kripke.transitions.get(curr, []):
                if nxt not in visited:
                    queue.append(path + [nxt])

        return True, None

    def check_finally(self, prop: str) -> Tuple[bool, Optional[str]]:
        """Verify liveness F(prop): prop is reachable from initial state."""
        visited = set()
        queue = [self.kripke.initial_state]

        while queue:
            curr = queue.pop(0)
            if prop in self.kripke.labels[curr]:
                return True, curr  # Found reachable state satisfying prop
            visited.add(curr)
            for nxt in self.kripke.transitions.get(curr, []):
                if nxt not in visited:
                    queue.append(nxt)

        return False, None

    def check_response(self, request_prop: str, response_prop: str) -> Tuple[bool, Optional[str]]:
        """Verify G(request -> F response): whenever request occurs, response eventually reachable."""
        # Find all states where request holds
        for s in self.kripke.states:
            if request_prop in self.kripke.labels[s]:
                # Check if response reachable from s
                visited = set()
                queue = [s]
                found = False
                while queue:
                    curr = queue.pop(0)
                    if response_prop in self.kripke.labels[curr]:
                        found = True
                        break
                    visited.add(curr)
                    for nxt in self.kripke.transitions.get(curr, []):
                        if nxt not in visited:
                            queue.append(nxt)
                if not found:
                    return False, s  # Request state that cannot reach response
        return True, None
