import argparse
import os
from tqdm import tqdm

def transform(word):
    word = word.replace('.', '')
    word = word.replace('!', '')
    word = word.replace(',', '')
    word = word.replace('?', '')
    word = word.replace(':', '')
    word = word.replace('»', '')
    word = word.replace('«', '')
    word = word.replace('–', '')
    word = word.replace('…', '')
    word = word.lower()
    return word

parser = argparse.ArgumentParser(description="Reads corpus txt files and generates a file with each unique word per line.") 
parser.add_argument("--src", default="", help="path to each corpus txt file, separated by commas", required=True)
parser.add_argument("--dst", default="", help="destination location to store words file, including the name of the file itself", required=True)
parser.add_argument("--tokens", default="", help="destination directory to store tokens file", required=False)
parser.add_argument("--tokens_format", default="other", help="format of the tokens file: wav2letter | other", required=False)
args = parser.parse_args()
print("Arguments")
print(args)

lexicon = {}
tokens = {}

txt_files = args.src.split(',')

for txt_file in tqdm(txt_files):
    print(f"Reading words in {txt_file}...")
    with open(txt_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            words = line.strip().split(' ')
            for word in words:
                if word == " ":
                    continue
                elif word == "":
                    continue
                else:
                    word = transform(word)
                    lexicon[word] = " ".join(word)

                for char in word:
                    tokens[char] = 0
    print("Done!\n")

os.makedirs(os.path.split(args.dst)[0], exist_ok=True)
with open(args.dst, 'w+') as f:
    print(f"Saving words in lexicon file at {args.dst}")
    for word in tqdm(sorted(lexicon.keys())):
        f.write(f"{word}\n")

if tokens != "":
    os.makedirs(os.path.split(args.tokens)[0], exist_ok=True)
    with open(args.tokens, 'w+') as f:
        print(f"Saving tokens in tokens file at {args.tokens}")
        if args.tokens_format == 'wav2letter':
            f.write(f"|\n")
        for token in tqdm(sorted(tokens.keys())):
            f.write(f"{token}\n")

