import os
import sys
import subprocess
import importlib.util
from pathlib import Path

HARNESS_DIR = Path(__file__).parent
SCENARIOS_DIR = HARNESS_DIR / "scenarios"

def run_scenario(script_path):
    try:
        # Load TEST_METADATA by importing the module
        spec = importlib.util.spec_from_file_location("scenario", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        metadata = getattr(module, "TEST_METADATA", {
            "risk_level": "UNKNOWN",
            "failure_class": ["unknown"]
        })
        
        # Execute the script as a subprocess
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        return {
            "name": script_path.stem,
            "passed": result.returncode == 0,
            "metadata": metadata,
            "output": result.stdout + result.stderr
        }
    except Exception as e:
        return {
            "name": script_path.stem,
            "passed": False,
            "metadata": {"risk_level": "UNKNOWN", "failure_class": ["execution_error"]},
            "output": str(e)
        }

def main():
    print("=== Cognition Failure Observatory: Runner v0 ===\n")
    
    scenarios = list(SCENARIOS_DIR.glob("*.py"))
    results = []
    
    for script in sorted(scenarios):
        if script.name.startswith("__"): continue
        res = run_scenario(script)
        results.append(res)
        status = "PASS" if res["passed"] else "FAIL"
        print(f"[{status}] {res['name']}")
        
    # Aggregate
    total_runs = len(results)
    passed_runs = sum(1 for r in results if r["passed"])
    failed_runs = total_runs - passed_runs
    
    # Risk Dashboard
    risk_counts = {"P0": 0, "P1": 0, "P2": 0, "UNKNOWN": 0}
    failure_classes = {}
    
    for res in results:
        if not res["passed"]:
            risk = res["metadata"].get("risk_level", "UNKNOWN")
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
            for fc in res["metadata"].get("failure_class", []):
                failure_classes[fc] = failure_classes.get(fc, 0) + 1

    print("\n=== Risk Dashboard ===")
    for risk in ["P0", "P1", "P2", "UNKNOWN"]:
        print(f"{risk} failures: {risk_counts.get(risk, 0)}")
            
    print("\n=== Failure Summary ===")
    if not failure_classes:
        print("All scenarios passed! No failures detected.")
    else:
        for fc, count in failure_classes.items():
            print(f"  {fc}: {count}")
            
    if risk_counts.get("P0", 0) > 0 or "false_negative" in failure_classes:
        print("\n❌ CRITICAL PROTOCOL FAILURE DETECTED. Exiting with error.")
        sys.exit(1)
    elif failed_runs > 0:
        print("\n⚠️ SCENARIOS FAILED. Check logs.")
        sys.exit(1)
    else:
        print("\n✅ ALL COGNITION INTEGRITY CHECKS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
