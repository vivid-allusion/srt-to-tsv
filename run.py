#!/usr/bin/env python3
"""Run the SRT to TSV converter with virtual environment activation."""

import subprocess
import sys
from pathlib import Path

def ensure_venv(project_root: Path) -> Path:
    """Create virtual environment if missing and return path to venv Python."""
    venv_python = project_root / "venv" / "bin" / "python"
    if venv_python.exists():
        return venv_python

    print("Creating virtual environment...")
    result = subprocess.run(
        [sys.executable, "-m", "venv", str(project_root / "venv")],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error creating virtual environment:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    print("Installing dependencies...")
    pip = project_root / "venv" / "bin" / "pip"
    result = subprocess.run(
        [str(pip), "install", "-r", str(project_root / "requirements.txt")],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error installing dependencies:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    return venv_python

def main():
    """Activate venv and run the main script."""
    project_root = Path(__file__).parent
    venv_python = ensure_venv(project_root)

    result = subprocess.run(
        [str(venv_python), "-m", "src.main"],
        cwd=project_root
    )

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()