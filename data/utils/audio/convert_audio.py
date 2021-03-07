""" 
Converts audio files within a folder to the specified format. 
"""

import os
import argparse
from joblib import Parallel, delayed
import multiprocessing
import sox

parser = argparse.ArgumentParser(description="Convert MP3 to WAV") 
parser.add_argument("--src", default="", help="source directory with MP3 files", required=True)
parser.add_argument("--dst", default="", help="destination directory with WAV files", required=True)
parser.add_argument("--from_type", default=None, help="source file type to convert from: wav | mp3 | ...", required=True)
parser.add_argument("--to_type", default=None, help="destination file type to convert to: wav | mp3 | ...")
parser.add_argument("--channels", default=None, help="destination file channels")
parser.add_argument("--sampling_rate", default=None, help="destination file sampling rate")
parser.add_argument("--bit_depth", default=None, help="destination file bit depth")
parser.add_argument("--remove_mp3", type=bool, default=False, help="remove the original MP3 files after conversion")
parser.add_argument("--workers", type=int, default=1, help="number of workers for code parallelization")
args = parser.parse_args()
print("Arguments")
print(args)

def convert_sample(src, dst, file_name, from_type, to_type, sampling_rate, channels, bit_depth):
    """Converts a single file to the desired format."""
    src_file_path = os.path.join(src, file_name)
    if to_type:
        dst_file_path = os.path.join(dst, file_name.replace(f'.{from_type}', f'.{to_type}'))
    else:
        dst_file_path = os.path.join(dst, file_name)

    tfm = sox.Transformer()
    tfm.set_output_format(file_type=to_type, rate=int(sampling_rate), bits=int(bit_depth), channels=int(channels))
    tfm.build(src_file_path, dst_file_path)

    if args.remove_mp3:
        os.system(f"rm {src_file_path}")

file_names = []
for root, directories, files in os.walk(args.src):
    for file in files:
        if file.endswith(f'.{args.from_type}') and not file.startswith('.'):
            file_names.append(file)

os.makedirs(args.dst, exist_ok=True)
print(f"Converting {args.from_type} files under directory {args.src}")
results = Parallel(n_jobs=args.workers)(delayed(convert_sample)(args.src, args.dst, i, args.from_type, args.to_type, args.sampling_rate, args.channels, args.bit_depth) for i in file_names)