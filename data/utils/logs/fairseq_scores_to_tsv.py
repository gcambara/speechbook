""" 
Reads a fairseq log file and computes the WER score for each utterance,
given that target and hypothesis transcripts are provided at such log.
A .tsv file is returned with the WER per utterance, along with the ID.
If the .tsv file originally used for fairseq testing is provided, the
WER scores shall be appended at such file, and output in a new one.
"""

import os
import argparse
import numpy as np
import pandas as pd
from fairseq import scoring
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Compute WER scores from fairseq log.") 
parser.add_argument("--src_log", default="", help="source fairseq log file", required=True)
parser.add_argument("--src_tsv", default="", help="source fairseq dataset tsv file")
parser.add_argument("--dst", default="", help="destination tsv file with the fairseq WER scores per utterance", required=True)
args = parser.parse_args()
print("Arguments")
print(args)

print("Building fairseq WER scorer...")
scorer = scoring.build_scorer('wer', None)

if args.src_tsv == "":
    print("No base .tsv file provided in --src_tsv argument, results shall be stored in a new .tsv file.")
else:
    df = pd.read_csv(args.src_tsv, sep='\t')
    print(f"Base .tsv read from --src_tsv = {args.src_tsv}")

print("Reading target and hypothesis transcripts from fairseq log...")
eval_dict = {}
with open(args.src_log, 'r') as f:
    curr_sample_id = ""
    for line in f.readlines():
        if line.startswith('T-'):
            curr_sample_id = line.split('\t')[0].replace('T-', '')
            ref = line.split('\t')[1].strip()
        elif line.startswith('D-'):
            assert (curr_sample_id == line.split('\t')[0].replace('D-', '')), "Reference transcript is not followed by a detokenized hypothesis!"
            hyp = line.split('\t')[2].strip()
            eval_dict[curr_sample_id] = (ref, hyp)

print("Scoring utterances with WER...")
if args.src_tsv == "":
    scores_list = []
    for sample_id, (ref, hyp) in eval_dict.items():
        scorer.add_string(ref, hyp)
        wer = scorer.result_string().split('WER: ')[1]
        scorer.reset()

        scores_list.append([sample_id, ref, hyp, wer])
    df = pd.DataFrame(scores_list, columns=['id', 'ref', 'hyp', 'wer'])
else:
    df['wer'] = np.nan
    for sample_id, (ref, hyp) in eval_dict.items():
        scorer.add_string(ref, hyp)
        wer = scorer.result_string().split('WER: ')[1]
        scorer.reset()

        assert (ref == df.loc[int(sample_id), 'tgt_text']), "The reference text indicated by the sample ID in the transcripts file does not match with the one stored in the dataset!"
        df.at[int(sample_id), 'wer'] = wer

df.to_csv(args.dst, sep='\t', index=None)