import gzip
import shutil
from pathlib import Path

# BUG FIX: Original used hardcoded relative paths "../data/..." which only work
# when the script is executed from inside the src/ directory. If run from the
# project root or any other location it raises FileNotFoundError. Now resolved
# relative to this file's own location so it is CWD-independent.
base_dir = Path(__file__).resolve().parents[1]
input_file = base_dir / "data" / "USA-road-d.NY.gr.gz"
output_file = base_dir / "data" / "USA-road-d.NY.gr"

with gzip.open(input_file, "rb") as f_in:
    with open(output_file, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

print("Extraction complete!")
