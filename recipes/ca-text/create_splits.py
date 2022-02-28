import argparse
import os
import random
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Reads words files and generates train-test splits, also doing some filtering.") 
parser.add_argument("--src", default="./cat_central/transdic_out.txt,./cat_occidental/transdic_out.txt,./cat_tortosa/transdic_out.txt,./cat_valencia_central/transdic_out.txt", help="path to each words txt file, separated by commas.")
parser.add_argument("--dst", default="./", help="destination location to store split file")
parser.add_argument("--test_percentage", default=0.05, type=float, help="percentage of the total data set to be used as test set")
parser.add_argument("--len_filter", default=15, type=int, help="words that have more tokens than this parameter are filtered out")
args = parser.parse_args()
print("Arguments")
print(args)

words_files = args.src.split(',')
test_words = []
filtered_words = set()

first_run = True
word_file_id = 0
for word_file in tqdm(words_files):
    train_file_path = os.path.basename(word_file).replace('.txt', '_train_{word_file_id}.lex')
    test_file_path = os.path.basename(word_file).replace('.txt', '_test_{word_file_id}.lex')
    with open(os.path.join(args.dst, train_file_path), 'w+') as train_file:
        with open(os.path.join(args.dst, test_file_path), 'w+') as test_file:
            with open(word_file, 'r') as f:
                lines = f.readlines()
                for line in tqdm(lines):
                    line_info = line.strip().split('\t')
                    if len(line_info) == 1 and line_info == ['h']:
                        line_info = ['h', 'ˈa g']
                    assert len(line_info) == 2, f"Error! Line info len is not 2: {len(line_info)}. Line info = {line_info}"
                    graphemes = line_info[0]
                    if graphemes in filtered_words:
                        continue

                    phonemes = line_info[1]
                    phonemes = phonemes.replace(' ', '')
                    spaced_phonemes = ""
                    for phn in phonemes:
                        spaced_phonemes += phn + " "
                    spaced_phonemes = spaced_phonemes.strip()
                    line_out = f"{graphemes} {spaced_phonemes}\n"

                    if len(graphemes) > args.len_filter:
                        filtered_words.add(graphemes)
                        continue

                    if first_run:
                        random_number = random.uniform(0, 1)
                        if random_number < args.test_percentage:
                            test_words.append(graphemes)
                            test_file.write(line_out)
                        else:
                            train_file.write(line_out)
                    else:
                        if graphemes in test_words:
                            test_file.write(line_out)
                        else:
                            train_file.write(line_out)
    first_run = False
    word_file_id += 1

with open(os.path.join(args.dst, 'filtered_words.txt'), 'w+') as f:
    for word in filtered_words:
        f.write(f"{word}\n")
