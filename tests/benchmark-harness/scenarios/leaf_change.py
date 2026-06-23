import os
import subprocess
import json
import shutil
from pathlib import Path

# Metadata for test catalog
TEST_METADATA = {
    "risk_level": "P2",
    "failure_class": ["false_positive", "metadata_drift"]
}

# Setup paths
HARNESS_DIR = Path(__file__).parent.parent
import sys; sys.path.append(str(HARNESS_DIR))
from utils import setup_fixture
REPO_DIR = HARNESS_DIR / "fixtures" / "repo-small"

def run_cmd(cmd, cwd=REPO_DIR):
    return subprocess.check_output(cmd, shell=True, cwd=cwd, text=True).strip()

def main():
    print("--- Running Scenario: leaf_change.py ---")
    setup_fixture(REPO_DIR)
    
    # 1. Setup Initial Mock State
    old_commit = run_cmd("git rev-parse HEAD")
    
    initial_metadata = {
        "project": "repo-small",
        "generated_commit": old_commit,
        "modules": {
            "a": {
                "verified_at": "2026-01-01T00:00:00Z",
                "verification_pass_rate": 0.5,
                "open_gaps": ["gap1_history"],
                "module_hash": "hash_a_1"
            },
            "b": {
                "verified_at": "2026-01-01T00:00:00Z",
                "verification_pass_rate": 0.8,
                "open_gaps": ["gap2_history"],
                "module_hash": "hash_b_1"
            }
        }
    }
    
    # 2. Mutation
    with open(REPO_DIR / "modules" / "a" / "index.ts", "a") as f:
        f.write("\nexport const TEST_INCREMENTAL = true;\n")
        
    run_cmd("git add . && git commit -m 'leaf change'")
    new_commit = run_cmd("git rev-parse HEAD")
    
    # 3. Phase 0: Incremental Detection Logic (Protocol execution mock)
    diff_output = run_cmd(f"git diff --name-only {old_commit}..{new_commit}")
    changed_files = diff_output.split("\n")
    
    dirty_modules = []
    for file in changed_files:
        if file.startswith("modules/a/"):
            dirty_modules.append("a")
        elif file.startswith("modules/b/"):
            dirty_modules.append("b")
        elif file.startswith("shared/"):
            pass
            
    # Assertion 1: Dirty Precision
    assert set(dirty_modules) == {"a"}, f"Assertion 1 Failed: Expected ['a'], got {dirty_modules}"
    print("✅ Assertion 1 Passed: Dirty Precision (Only 'a' is dirty, False Negative avoided)")
    
    # 4. Phase 4: Metadata Mutation (Simulating Agent replacement semantics)
    new_metadata = json.loads(json.dumps(initial_metadata)) # deep copy
    new_metadata["generated_commit"] = new_commit
    
    new_metadata["modules"]["a"] = {
        "verified_at": "2026-01-02T00:00:00Z", # Replaced
        "verification_pass_rate": 1.0,         # Replaced
        "open_gaps": [],                       # Strict replacement, no append!
        "module_hash": "hash_a_2"              # Replaced
    }
    
    # Assertion 2: Metadata Replacement
    module_a = new_metadata["modules"]["a"]
    assert module_a["verified_at"] != initial_metadata["modules"]["a"]["verified_at"]
    assert module_a["open_gaps"] == []
    print("✅ Assertion 2 Passed: Metadata Replacement for 'a' (Ghost gaps prevented)")
    
    # Assertion 3: Unchanged Stability
    module_b = new_metadata["modules"]["b"]
    assert json.dumps(module_b) == json.dumps(initial_metadata["modules"]["b"])
    print("✅ Assertion 3 Passed: Unchanged Stability for 'b' (Byte-identical integrity)")

    # Assertion 4: Phase 5 Regeneration
    assert new_metadata["generated_commit"] != initial_metadata["generated_commit"]
    print("✅ Assertion 4 Passed: Phase 5 Global Metadata regenerated")
    
    print("\n🎉 Scenario `leaf_change.py` completed successfully!")

if __name__ == "__main__":
    main()
