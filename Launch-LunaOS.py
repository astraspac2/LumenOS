import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

subprocess.run(
    [sys.executable, "main.py"],
    cwd=ROOT
)