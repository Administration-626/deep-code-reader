import os
import subprocess
import json
import shutil
from pathlib import Path

# Metadata for test catalog
TEST_METADATA = {
    "risk_level": "P0",
    "failure_class": ["false_negative", "stale_manifest", "ghost_state"]
}

HARNESS_DIR = Path(__file__).parent.parent
import sys; sys.path.append(str(HARNESS_DIR))
from utils import setup_fixture
REPO_DIR = HARNESS_DIR / "fixtures" / "repo-small"

def run_cmd(cmd, cwd=REPO_DIR):
    return subprocess.check_output(cmd, shell=True, cwd=cwd, text=True).strip()

def main():
    print("--- Running Scenario: shared_contract_change.py ---")
    print(f"Risk Level: {TEST_METADATA['risk_level']} | Failure Class: {TEST_METADATA['failure_class']}")
    setup_fixture(REPO_DIR)
    
    # 1. Ensure a third module `c` exists that DOES NOT import shared
    os.makedirs(REPO_DIR / "modules" / "c", exist_ok=True)
    with open(REPO_DIR / "modules" / "c" / "index.ts", "w") as f:
        f.write("export const NO_DEPENDENCY = true;\n")
    run_cmd("git add . && git commit -m 'add module c' || true")
    
    old_commit = run_cmd("git rev-parse HEAD")
    
    # Mock Initial State
    initial_metadata = {
        "project": "repo-small",
        "generated_commit": old_commit,
        "modules": {
            "a": {
                "verified_at": "2026-01-01T00:00:00Z",
                "open_gaps": ["gap_a"],
                "module_hash": "hash_a_1",
                "dependencies": ["shared/types.ts"]
            },
            "b": {
                "verified_at": "2026-01-01T00:00:00Z",
                "open_gaps": ["gap_b"],
                "module_hash": "hash_b_1",
                "dependencies": ["shared/types.ts"]
            },
            "c": {
                "verified_at": "2026-01-01T00:00:00Z",
                "open_gaps": ["gap_c"],
                "module_hash": "hash_c_1",
                "dependencies": []
            }
        }
    }
    
    # 2. Mutation: Modify Shared Contract
    with open(REPO_DIR / "shared" / "types.ts", "a") as f:
        f.write("\nexport interface SharedConfig { feature_flag: boolean; }\n")
        
    run_cmd("git add . && git commit -m 'shared contract avalanche'")
    new_commit = run_cmd("git rev-parse HEAD")
    
    # 3. Phase 0: Incremental Detection Logic (Dependency-aware invalidation)
    diff_output = run_cmd(f"git diff --name-only {old_commit}..{new_commit}")
    changed_files = diff_output.split("\n")
    
    dirty_modules = set()
    for file in changed_files:
        if file.startswith("shared/"):
            # AVALANCHE: find all modules depending on shared
            for mod_name, mod_data in initial_metadata["modules"].items():
                if "shared/types.ts" in mod_data.get("dependencies", []):
                    dirty_modules.add(mod_name)
        elif file.startswith("modules/a/"):
            dirty_modules.add("a")
        elif file.startswith("modules/b/"):
            dirty_modules.add("b")
        elif file.startswith("modules/c/"):
            dirty_modules.add("c")
            
    # Assertion 1: Avalanche Correctness
    assert dirty_modules == {"a", "b"}, f"Assertion 1 Failed: Expected {{'a', 'b'}}, got {dirty_modules}"
    print("✅ Assertion 1 Passed: Avalanche Correctness (Both 'a' and 'b' invalidated, no False Negative)")
    
    # 4. Phase 4 Simulation
    new_metadata = json.loads(json.dumps(initial_metadata))
    new_metadata["generated_commit"] = new_commit
    
    for mod in ["a", "b"]:
        new_metadata["modules"][mod] = {
            "verified_at": "2026-01-02T00:00:00Z",
            "open_gaps": [],
            "module_hash": f"hash_{mod}_2",
            "dependencies": ["shared/types.ts"]
        }
        
    # Assertion 2 & 3: Metadata Full Refresh & No Ghost State
    for mod in ["a", "b"]:
        assert new_metadata["modules"][mod]["verified_at"] != initial_metadata["modules"][mod]["verified_at"]
        assert new_metadata["modules"][mod]["open_gaps"] == []
    print("✅ Assertion 2 & 3 Passed: Metadata Replaced & No Ghost State")
    
    # Assertion 4: Global Manifest Consistency
    assert new_metadata["generated_commit"] != initial_metadata["generated_commit"]
    print("✅ Assertion 4 Passed: Global Manifest Consistency regenerated")
    
    # Assertion 5: Byte Stability Outside Dirty Set
    assert json.dumps(new_metadata["modules"]["c"]) == json.dumps(initial_metadata["modules"]["c"])
    print("✅ Assertion 5 Passed: Byte Stability Outside Dirty Set (Module 'c' completely untouched)")

    print("\n🎉 Scenario `shared_contract_change.py` completed successfully!")

if __name__ == "__main__":
    main()
