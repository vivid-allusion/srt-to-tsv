#!/usr/bin/env python3
"""Run the SRT to TSV converter with virtual environment activation."""

import subprocess
import sys
from pathlib import Path

def main():
    """Activate venv and run the main script."""
    project_root = Path(__file__).parent
    venv_python = project_root / "venv" / "bin" / "python"

    if not venv_python.exists():
        print(f"Error: Virtual environment not found at {venv_python}")
        print("Please create it with: python3 -m venv venv")
        sys.exit(1)

    # Run the main script using the venv Python
    result = subprocess.run(
        [str(venv_python), "-m", "src.main"],
        cwd=project_root
    )

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()