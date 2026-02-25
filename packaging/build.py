from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    spec_path = project_root / "packaging" / "stm_sts.spec"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        str(spec_path),
    ]
    subprocess.run(cmd, check=True, cwd=project_root)


if __name__ == "__main__":
    main()
