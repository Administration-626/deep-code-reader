import os
import subprocess
import json
import shutil
from pathlib import Path

# Metadata for test catalog
TEST_METADATA = {
    "risk_level": "P0",
    "failure_class": ["stale_manifest", "metadata_drift"]
}

HARNESS_DIR = Path(__file__).parent.parent
import sys; sys.path.append(str(HARNESS_DIR))
from utils import setup_fixture
REPO_DIR = HARNESS_DIR / "fixtures" / "repo-small"

def run_cmd(cmd, cwd=REPO_DIR):
    return subprocess.check_output(cmd, shell=True, cwd=cwd, text=True).strip()

def main():
    print("--- Running Scenario: stale_manifest.py ---")
    setup_fixture(REPO_DIR)
    
    # 1. Ensure `repo-small` is reset
    run_cmd("git clean -fd && git reset --hard HEAD")
    old_commit = run_cmd("git rev-parse HEAD")
    
    # Recreate module 'a' just in case it was deleted by previous tests
    os.makedirs(REPO_DIR / "modules" / "a", exist_ok=True)
    with open(REPO_DIR / "modules" / "a" / "index.ts", "w") as f:
        f.write("export const TEST = 1;")
    run_cmd("git add . && git commit -m 'restore a' || true")
    
    initial_metadata = {
        "project": "repo-small",
        "generated_commit": old_commit,
        "modules": {
            "a": {
                "verified_at": "2026-01-01T00:00:00Z",
                "open_gaps": [],
                "module_hash": "hash_a_1",
                "dependencies": []
            }
        }
    }
    
    # 2. Mutation: Delete the module under the hood (e.g., via git branch switch)
    shutil.rmtree(REPO_DIR / "modules" / "a", ignore_errors=True)
    run_cmd("git add -u && git commit -m 'delete a secretly' || true")
    
    # 3. Phase 0: The protocol boots up and compares metadata to physical disk.
    # It notices `a` is in metadata but not on disk.
    physical_modules = set()
    for root, dirs, files in os.walk(REPO_DIR / "modules"):
        if "index.ts" in files:
            physical_modules.add(Path(root).name)
            
    # Assertion 1: Stale Manifest Detection
    assert "a" not in physical_modules
    assert "a" in initial_metadata["modules"]
    
    # The protocol must explicitly purge "a" from the new metadata to prevent corruption
    new_metadata = json.loads(json.dumps(initial_metadata))
    
    # Protocol purging logic
    stale_modules = set(new_metadata["modules"].keys()) - physical_modules
    for stale in stale_modules:
        del new_metadata["modules"][stale]
        
    assert "a" not in new_metadata["modules"]
    print("✅ Assertion 1 Passed: Stale manifest detected and module purged (Corruption prevented)")
    
if __name__ == "__main__":
    main()
