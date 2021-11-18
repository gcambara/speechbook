import argparse
import os
import pandas as pd
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Gets sentences in a TSV file and stores them in a txt file.") 
parser.add_argument("--src", default="", help="path to each TSV file, separated by commas", required=True)
parser.add_argument("--dst", default="", help="destination directory to store normalized TSV files", required=True)
parser.add_argument("--column", default="", help="name of the column containing the sentences", required=True)
args = parser.parse_args()
print("Arguments")
print(args)

tsv_paths = args.src.split(',')
os.makedirs(args.dst, exist_ok=True)

for tsv_path in tsv_paths:
    print(f"Processing {tsv_path}...")
    filename = os.path.basename(tsv_path)

    df = pd.read_csv(tsv_path, sep='\t')
    sentences = df[args.column].tolist()
    with open(os.path.join(args.dst, filename.replace('.tsv', '.txt')), 'w+') as f:
        for sentence in tqdm(sentences):
            f.write(f"{sentence}\n")
    print("Done!")