from .runner import run_python_code
import html
from typing import List, Dict

def run_tests_on_submission(code: str, tests: List[Dict]) -> Dict:
    """
    tests: list of {"input": "input text", "expected": "expected output text"}
    returns dict with score, per_test details, feedback string
    """
    total = len(tests)
    passed = 0
    test_details = []
    for idx, t in enumerate(tests, start=1):
        tc_input = t.get("input", "")
        expected = t.get("expected", "").strip()
        rc, stdout, stderr = run_python_code(code, stdin_data=tc_input)
        out = stdout.strip()
        ok = False
        reason = ""
        if rc == -1:
            reason = stderr
        elif stderr:
            # There was runtime error
            reason = stderr.strip()
        if rc == 0 and stderr.strip() == "":
            # compare outputs, normalize whitespace
            def norm(s): return "\n".join([ln.rstrip() for ln in s.strip().splitlines()]).strip()
            if norm(out) == norm(expected):
                ok = True
                passed += 1
            else:
                reason = f"Wrong output. Expected: {html.escape(expected)} Got: {html.escape(out)}"
        test_details.append({
            "test_number": idx,
            "input": tc_input,
            "expected": expected,
            "output": out,
            "stderr": stderr,
            "passed": ok,
            "reason": reason
        })
    score = int((passed / total) * 100) if total else 0
    # Generate AI-like feedback heuristics
    feedback_lines = []
    if score == 100:
        feedback_lines.append("Excellent — all test cases passed.")
    else:
        feedback_lines.append(f"{passed}/{total} tests passed. Score: {score}%")
        # common hints
        if any(d["stderr"] for d in test_details):
            feedback_lines.append("There were runtime errors. Check for exceptions, incorrect indexing, or input parsing.")
        # If outputs mismatch but program ran, suggest printing debug values
        if any((not d["passed"]) and (d["stderr"] == "") for d in test_details):
            feedback_lines.append("Output mismatch on some tests. Check formatting, whitespace, and correct use of loops/conditions.")
    feedback = "\n".join(feedback_lines)
    return {"score": score, "passed": passed, "total": total, "test_details": test_details, "feedback": feedback}
