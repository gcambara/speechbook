import argparse
import os
import pandas as pd
from tqdm import tqdm
from data.commonvoice.utils.normalizer import CommonVoiceNormalizer

def normalize_tsv(tsv_path, dst_folder, generate_txt_file):
    normalizer = CommonVoiceNormalizer()

    unique_characters = set()
    char_sent = {}
    df = pd.read_csv(tsv_path, sep='\t')
    for i, row in tqdm(df.iterrows()):
        sentence = row['sentence']
        if type(sentence) != str:
            continue
        sentence = normalizer.normalize(sentence)

        for character in sentence:
            if character in normalizer.get_discard_chars():
                pass
            else:
                unique_characters.add(character)
                char_sent[character] = sentence

        df.at[df.index[i], 'sentence'] = sentence

    filename = os.path.basename(tsv_path)
    df.to_csv(os.path.join(dst_folder, filename), sep='\t', index=None)

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






# exit()

# tsv_path = './dev.tsv'

# df = pd.read_csv(tsv_path, sep='\t')
# sentences = df['sentence']

# normalizer = CommonVoiceNormalizer()
# #normalizer = normalizers.Sequence([BertNormalizer(clean_text=True, handle_chinese_chars=True,
# #                                                  strip_accents=False, lowercase=True), NFKC(), Strip()])

# unique_characters = set()
# char_sent = {}
# for sentence in tqdm(sentences):
#     if type(sentence) != str:
#         continue
#     #sentence = normalizer.normalize_str(sentence)
#     #sentence = sentence.translate(str.maketrans('', '', string.punctuation))
#     #sentence = ''.join(trans_map.get(ch, ch) for ch in sentence)
#     sentence = normalizer(sentence)

#     for character in sentence:
#         if character in normalizer.get_discard_chars():
#             pass
#         else:
#             unique_characters.add(character)
#             char_sent[character] = sentence

# print(len(unique_characters))
# print(unique_characters)
# print(char_sent)
