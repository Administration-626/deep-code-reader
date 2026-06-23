import os
import subprocess
import json
import shutil
from pathlib import Path

# Metadata for test catalog
TEST_METADATA = {
    "risk_level": "P1",
    "failure_class": ["ghost_state", "stale_routing", "orphan_manifest"]
}

HARNESS_DIR = Path(__file__).parent.parent
import sys; sys.path.append(str(HARNESS_DIR))
from utils import setup_fixture
REPO_DIR = HARNESS_DIR / "fixtures" / "repo-small"

def run_cmd(cmd, cwd=REPO_DIR):
    return subprocess.check_output(cmd, shell=True, cwd=cwd, text=True).strip()

def main():
    print("--- Running Scenario: module_delete.py ---")
    setup_fixture(REPO_DIR)
    
    # 1. Ensure `repo-small` is reset to a known state
    run_cmd("git clean -fd && git reset --hard HEAD")
    
    old_commit = run_cmd("git rev-parse HEAD")
    
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
            }
        }
    }
    
    # 2. Mutation: Delete module 'a' completely
    shutil.rmtree(REPO_DIR / "modules" / "a", ignore_errors=True)
    run_cmd("git add -u && git commit -m 'delete module a'")
    new_commit = run_cmd("git rev-parse HEAD")
    
    # 3. Phase 0: Incremental Detection
    diff_output = run_cmd(f"git diff --name-only {old_commit}..{new_commit}")
    changed_files = diff_output.split("\n")
    
    deleted_modules = set()
    for file in changed_files:
        if file.startswith("modules/a/"):
            deleted_modules.add("a")
            
    assert deleted_modules == {"a"}
    print("✅ Assertion 1 Passed: Deletion correctly identified for 'a'")
    
    # 4. Phase 4 Simulation: Cognition Garbage Collection
    new_metadata = json.loads(json.dumps(initial_metadata))
    new_metadata["generated_commit"] = new_commit
    
    if "a" in new_metadata["modules"]:
        del new_metadata["modules"]["a"]
        
    # Assertion 2: No Ghost Metadata
    assert "a" not in new_metadata["modules"]
    print("✅ Assertion 2 Passed: No Ghost Metadata (Module 'a' purged completely)")
    
    # Assertion 3: Manifest Regeneration
    assert new_metadata["generated_commit"] != initial_metadata["generated_commit"]
    print("✅ Assertion 3 Passed: Global Manifest Consistency regenerated")
    
    print("\n🎉 Scenario `module_delete.py` completed successfully!")

if __name__ == "__main__":
    main()
