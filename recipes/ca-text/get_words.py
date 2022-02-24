import argparse
import os
from tqdm import tqdm

def transform(word, cat_tokens):
    word = word.replace('.', '')
    word = word.replace('!', '')
    word = word.replace(',', '')
    word = word.replace('?', '')
    word = word.replace(':', '')
    word = word.replace(';', '')
    word = word.replace('»', '')
    word = word.replace('«', '')
    word = word.replace('–', '')
    word = word.replace('…', '')
    word = word.replace('"', '')
    word = word.replace('$', '')
    word = word.replace('%', '')
    word = word.replace('*', '')
    word = word.replace('>', '')
    word = word.replace('<', '')
    word = word.replace('~', '')
    word = word.replace('“', '')
    word = word.replace('”', '')
    word = word.lower()

    trailing_tokens = "'-·"
    word = word.strip(trailing_tokens)

    if cat_tokens:
        for token in word:
            if token not in cat_tokens:
                word = ''

    return word

parser = argparse.ArgumentParser(description="Reads corpus txt files and generates a file with each unique word per line.") 
parser.add_argument("--src", default="", help="path to each corpus txt file, separated by commas. Otherwise, especify the directory, and all sub txt files will be taken", required=True)
parser.add_argument("--dst", default="", help="destination location to store words file, including the name of the file itself", required=True)
parser.add_argument("--cat_tokens", default="./tokens_cat.txt", help="file that contains predefined catalan tokens. After preprocessing, if a word contains a token that is not included here, it will be discarded", required=False)
parser.add_argument("--tokens", default="", help="destination directory to store tokens file", required=False)
parser.add_argument("--tokens_format", default="other", help="format of the tokens file: wav2letter | other", required=False)
args = parser.parse_args()
print("Arguments")
print(args)

lexicon = {}
tokens = {}

if args.cat_tokens != "":
    with open(args.cat_tokens, 'r') as f:
        cat_tokens = f.read().splitlines() 
else:
    cat_tokens = None

if os.path.isdir(args.src):
    txt_files = []
    for root, dirs, files in os.walk(args.src):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
else:
    txt_files = args.src.split(',')

for txt_file in tqdm(txt_files):
    print(f"Reading words in {txt_file}...")
    with open(txt_file, 'r') as f:
        lines = f.readlines()
        for line in tqdm(lines):
            words = line.strip().split(' ')
            for word in words:
                if word == " ":
                    continue
                elif word == "":
                    continue
                else:
                    word = transform(word, cat_tokens=cat_tokens)
                    if word == "":
                        continue
                    else:
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
