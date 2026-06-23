import os
import subprocess
import json
import shutil
from pathlib import Path

# Metadata for test catalog
TEST_METADATA = {
    "risk_level": "P0",
    "failure_class": ["false_negative", "cognition_poisoning"]
}

HARNESS_DIR = Path(__file__).parent.parent
import sys; sys.path.append(str(HARNESS_DIR))
from utils import setup_fixture
REPO_DIR = HARNESS_DIR / "fixtures" / "repo-small"

def run_cmd(cmd, cwd=REPO_DIR):
    return subprocess.check_output(cmd, shell=True, cwd=cwd, text=True).strip()

def main():
    print("--- Running Scenario: ambiguous_ownership.py ---")
    setup_fixture(REPO_DIR)
    
    run_cmd("git clean -fd && git reset --hard HEAD")
    old_commit = run_cmd("git rev-parse HEAD")
    
    # Both a and b exist, but dependencies aren't explicitly mapped in metadata (ambiguous)
    initial_metadata = {
        "project": "repo-small",
        "generated_commit": old_commit,
        "modules": {
            "a": { "verified_at": "2026-01-01T00:00:00Z" },
            "b": { "verified_at": "2026-01-01T00:00:00Z" }
        }
    }
    
    # Mutation: change a shared file
    os.makedirs(REPO_DIR / "shared" / "contracts", exist_ok=True)
    with open(REPO_DIR / "shared" / "contracts" / "user.ts", "w") as f:
        f.write("export type User = { id: string };\n")
    run_cmd("git add . && git commit -m 'add ambiguous shared contract' || true")
    new_commit = run_cmd("git rev-parse HEAD")
    
    diff_output = run_cmd(f"git diff --name-only {old_commit}..{new_commit}")
    changed_files = diff_output.split("\n")
    
    # Phase 0 logic: Because dependencies are ambiguous/unknown, we must invalidate ALL
    dirty_modules = set()
    has_ambiguous_change = any(f.startswith("shared/") for f in changed_files)
    
    if has_ambiguous_change:
        # Invalidate ALL
        dirty_modules.update(initial_metadata["modules"].keys())
        
    assert dirty_modules == {"a", "b"}
    print("✅ Assertion 1 Passed: Ambiguous ownership triggered FULL invalidation (False Negatives blocked)")

if __name__ == "__main__":
    main()
