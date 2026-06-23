import os
import shutil
import subprocess
from pathlib import Path

def setup_fixture(repo_dir: Path):
    shutil.rmtree(repo_dir, ignore_errors=True)
    os.makedirs(repo_dir / "modules" / "a")
    os.makedirs(repo_dir / "modules" / "b")
    os.makedirs(repo_dir / "shared")
    with open(repo_dir / "shared" / "types.ts", "w") as f:
        f.write("export type ID = string;\n")
    with open(repo_dir / "modules" / "a" / "index.ts", "w") as f:
        f.write("import { ID } from '../../shared/types';\n")
    with open(repo_dir / "modules" / "b" / "index.ts", "w") as f:
        f.write("import { ID } from '../../shared/types';\n")
    subprocess.check_output("git init", shell=True, cwd=repo_dir)
    subprocess.check_output("git add . && git commit -m 'initial'", shell=True, cwd=repo_dir)
