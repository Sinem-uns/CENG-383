import gzip
import shutil

input_file = "../data/USA-road-d.NY.gr.gz"
output_file = "../data/USA-road-d.NY.gr"

with gzip.open(input_file, 'rb') as f_in:
    with open(output_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print("Extraction complete!")