import argparse
import os
import pandas as pd
from tqdm import tqdm
from data.commonvoice.utils.normalizer import CommonVoiceNormalizer

def normalize_tsv(tsv_path, dst_folder, generate_txt_file):
    normalizer = CommonVoiceNormalizer()
    normalizer.keep_trans_characters(['ß'])

    drop_indices = []

    df = pd.read_csv(tsv_path, sep='\t')
    for i, row in tqdm(df.iterrows()):
        discard_sentence = False
        sentence = row['sentence']
        if type(sentence) != str:
            continue
        sentence = normalizer.normalize(sentence)

        for character in sentence:
            if character in normalizer.get_discard_chars():
                discard_sentence = True
                drop_indices.append(i)
                break

        if not discard_sentence:
            df.at[df.index[i], 'sentence'] = sentence

    dropped_df = df.iloc[drop_indices]
    df = df.drop(drop_indices)

    filename = os.path.basename(tsv_path)
    df.to_csv(os.path.join(dst_folder, filename), sep='\t', index=None)
    dropped_df.to_csv(os.path.join(dst_folder, filename).replace('.tsv', '_dropped.tsv'), sep='\t', index=None)

    if generate_txt_file:
        sentences = df['sentence'].tolist()
        with open(os.path.join(dst_folder, filename.replace('.tsv', '.txt')), 'w+') as f:
            for sentence in sentences:
                f.write(f"{sentence}\n")

parser = argparse.ArgumentParser(description="Normalize Common Voice German text") 
parser.add_argument("--src", default="", help="path to each TSV file, separated by commas", required=True)
parser.add_argument("--dst", default="", help="destination directory to store normalized TSV files", required=True)
parser.add_argument("--generate_txt_files", type=bool, default=True, help="store corpus txt files in destination folder")
args = parser.parse_args()
print("Arguments")
print(args)

tsv_paths = args.src.split(',')
os.makedirs(args.dst, exist_ok=True)

for tsv_path in tsv_paths:
    normalize_tsv(tsv_path, args.dst, args.generate_txt_files)