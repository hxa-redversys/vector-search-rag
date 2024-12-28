import os
import sys
from pathlib import Path

# Get the absolute path to the project root
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

print(f"Project root configured at: {ROOT_DIR}")