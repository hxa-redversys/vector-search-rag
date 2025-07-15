import sys
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

# Indicate testing mode so the backend uses the dummy model
import os
os.environ["TESTING"] = "1"
