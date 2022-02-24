import argparse
import os
import random
from tqdm import tqdm

words_files = ['./cat_central/transdic_out.txt', 
               './cat_occidental/transdic_out.txt',
               './cat_tortosa/transdic_out.txt',
               './cat_valencia_central/transdic_out.txt']
test_percentage = 0.05

test_words = []

first_run = True
for word_file in tqdm(words_files):
    train_file_path = word_file.replace('.txt', '_train.lex')
    test_file_path = word_file.replace('.txt', '_test.lex')
    with open(train_file_path, 'w+') as train_file:
        with open(test_file_path, 'w+') as test_file:
            with open(word_file, 'r') as f:
                lines = f.readlines()
                for line in tqdm(lines):
                    line_info = line.strip().split('\t')
                    if len(line_info) == 1 and line_info == ['h']:
                        line_info = ['h', 'ˈa g']
                    assert len(line_info) == 2, f"Error! Line info len is not 2: {len(line_info)}. Line info = {line_info}"
                    graphemes = line_info[0]
                    phonemes = line_info[1]
                    phonemes = phonemes.replace(' ', '')
                    spaced_phonemes = ""
                    for phn in phonemes:
                        spaced_phonemes += phn + " "
                    spaced_phonemes = spaced_phonemes.strip()
                    line_out = f"{graphemes} {spaced_phonemes}\n"
                    if first_run:
                        random_number = random.uniform(0, 1)
                        if random_number < test_percentage:
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
