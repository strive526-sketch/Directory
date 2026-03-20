"""
Shared configuration for CJDT analysis scripts.
All paths are relative to the project root (one level up from scripts/).
"""
import os

# Project root = parent of scripts/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input data
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
ZIP_PATH = os.path.join(DATA_DIR, "CjdtClerkCase.zip")
SAO_ZIP_PATH = os.path.join(DATA_DIR, "CjdtSAOCase.zip")

# Output
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Common constants
MISSING_VALS = {"Not Available", "N/A", "NA", "", "nan", "None", "NULL", "null"}
CHUNK_SIZE = 200000
