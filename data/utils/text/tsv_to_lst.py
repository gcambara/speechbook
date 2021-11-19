import argparse
import os
import pandas as pd
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Translates a TSV file into a lst file ready for wav2letter/Flashlight pipeline.") 
parser.add_argument("--src", default="", help="path to each TSV file, separated by commas", required=True)
parser.add_argument("--dst", default="", help="destination directory to store lst files", required=True)
parser.add_argument("--txt_column", default="sentence", help="name of the column containing the sentences")
parser.add_argument("--path_column", default="path", help="name of the column containing the paths")
parser.add_argument("--id_method", default="from_path", help="method to extract the sample ID: from_path")
parser.add_argument("--get_length", type=bool, default=True, help="read the length in milliseconds")
parser.add_argument("--from_type", default="", help="change the file extension in the path from the one indicated here")
parser.add_argument("--to_type", default="", help="change the file extension in the path to the one indicated here")
parser.add_argument("--base_path", default="", help="base path to append before the parsed path in the TSV")
args = parser.parse_args()
print("Arguments")
print(args)

tsv_paths = args.src.split(',')
os.makedirs(args.dst, exist_ok=True)

for tsv_path in tsv_paths:
    print(f"Processing {tsv_path}...")
    filename = os.path.basename(tsv_path)

    df = pd.read_csv(tsv_path, sep='\t')
    with open(os.path.join(args.dst, filename.replace('.tsv', '.lst')), 'w+') as f:
        for i, row in tqdm(df.iterrows()):
            transcript = row[args.txt_column]
            path = row[args.path_column]

            if args.id_method == 'from_path':
                sample_id = path.split('.')[:-1]
                sample_id = ''.join(sample_id)
            else:
                raise NotImplementedError

            if args.from_type != "" and args.to_type != "":
                path = path.replace(f".{args.from_type}", f".{args.to_type}")

            if args.base_path != "":
                path = os.path.join(args.base_path, path)

            if args.get_length:
                length = 5000.0
            else:
                length = 5000.0

            f.write(f"{sample_id}\t{path}\t{length}\t{transcript}\n")
    print("Done!")