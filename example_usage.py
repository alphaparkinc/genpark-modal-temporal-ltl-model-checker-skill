"""
Demonstration of Modal Temporal LTL Model Checker Skill
"""

from client import KripkeStructure, LTLModelChecker

def main():
    print("=== Linear Temporal Logic (LTL) Symbolic Model Checking ===")
    kripke = KripkeStructure(states=["IDLE", "WORKING", "COMPLETED", "CRASHED"], initial_state="IDLE")

    # Transitions
    kripke.add_transition("IDLE", "WORKING")
    kripke.add_transition("WORKING", "COMPLETED")
    kripke.add_transition("COMPLETED", "IDLE")

    # Labels
    kripke.add_label("IDLE", "safe")
    kripke.add_label("WORKING", "safe")
    kripke.add_label("WORKING", "request")
    kripke.add_label("COMPLETED", "safe")
    kripke.add_label("COMPLETED", "response")

    checker = LTLModelChecker(kripke)

    print("Checking Safety Property G(safe)...")
    is_safe, counterexample = checker.check_globally("safe")
    print(f"Safety G(safe): {is_safe} (Counterexample: {counterexample})")
    assert is_safe is True

    print("\nChecking Liveness Property F(response)...")
    is_live, reachable_state = checker.check_finally("response")
    print(f"Liveness F(response): {is_live} (State: {reachable_state})")
    assert is_live is True

    print("\nChecking Response Property G(request -> F response)...")
    response_ok, violation_state = checker.check_response("request", "response")
    print(f"Response G(req -> F resp): {response_ok}")
    assert response_ok is True

    print("\nLTL Model Checker Verification PASS!")

if __name__ == "__main__":
    main()
