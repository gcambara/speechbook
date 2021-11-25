""" 
Validates that all audio files in a dataset are readable. 
"""

import argparse
import os
import pandas as pd
import sox
from tqdm import tqdm

def check_dataset(df, dst, column, base_path=None, type=None, channels=None, sampling_rate=None):
    with open(dst, 'w+') as f:
        for _, row in tqdm(df.iterrows()):
            if base_path:
                audio_path = os.path.join(base_path, row.iloc[column])
            else:
                audio_path = row.iloc[column]

            if type:
                file_type = sox.file_info.file_type(audio_path)
                if file_type != type:
                    f.write(f"Error! File type is {file_type}, but expected {type}. File = {audio_path}")

            if sampling_rate:
                sample_rate = int(sox.file_info.sample_rate(audio_path))
                if sample_rate != sampling_rate:
                    f.write(f"Error! Sampling rate is {sample_rate} Hz, but expected {sampling_rate} Hz. File = {audio_path}")

            if channels:
                n_channels = int(sox.file_info.channels(audio_path))
                if n_channels != channels:
                    f.write(f"Error! There are {n_channels} channels, but expected {channels} channels. File = {audio_path}")

parser = argparse.ArgumentParser(description="Validate audio samples in a dataset") 
parser.add_argument("--src", default="", help="path to the src manifest with the paths to the samples", required=True)
parser.add_argument("--dst", default="", help="path to the dst report file", required=True)
parser.add_argument("--base_path", default=None, help="path to pre-append to sample paths")
parser.add_argument("--column", type=int, default=None, help="column number where the paths are stored at", required=True)
parser.add_argument("--sep", default="\t", help="expected separator between columns")
parser.add_argument("--type", default=None, help="expected type for all audio files")
parser.add_argument("--channels", default=None, help="expected channels for all audio files")
parser.add_argument("--sampling_rate", default=None, help="expected sampling rate for all audio files")
parser.add_argument("--skip_header", type=bool, default=False, help="""if set to True, it will
                                                                       skip the first row, since
                                                                       it will consider it
                                                                       as header""")
args = parser.parse_args()
print("Arguments")
print(args)

if args.skip_header:
    header = None
else:
    header = 0

df = pd.read_csv(args.src, sep=args.sep, header=header)

check_dataset(df, args.dst, args.column, args.base_path, args.type, args.channels, args.sampling_rate)