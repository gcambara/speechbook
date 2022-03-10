import argparse
import os
import pandas as pd
import torchaudio
from tqdm import tqdm

PARTITIONS_LIST = ['train', 'test']
SAMPLING_RATE = 44100

def parse_arguments():
    parser = argparse.ArgumentParser(description='UrbanSound 8k data preparation script')
    parser.add_argument('--root', default='/datasets/TALN/speech/audio/urbansound8k/UrbanSound8K', help='path to the directory where the dataset is to be found')
    parser.add_argument('--dev_folds', default='9', help='the folds to use for dev')
    parser.add_argument('--test_folds', default='10', help='the folds to use for test')
    parser.add_argument('--dst', default='', help='destination folder to output tsv files')
    parser.add_argument('--manifest_format', default='speechbrain', help='format of the output tsv manifest')
    args = parser.parse_args()
    return args

def folds_to_list(folds):
    out_folds = []
    for fold in folds.split(','):
        out_folds.append(int(fold))
    return out_folds

def generate_manifests(src, dst, dev_folds, test_folds, manifest_format):
    meta_path = os.path.join(src, 'metadata', 'UrbanSound8K.csv')
    audio_dir = os.path.join(src, 'audio')
    assert os.path.isfile(meta_path), f"UrbanSound8K metadata file has not been found! Metadata path: {meta_path}"
    assert os.path.isdir(audio_dir), f"UrbanSound8K audio directory has not been found! Partition path: {audio_dir}"

    meta_df = pd.read_csv(meta_path)

    if manifest_format == 'speechbrain':
        meta_df = meta_df.rename(columns={"slice_file_name": "ID"})
        meta_df['wav'] = meta_df['ID']

        meta_df['ID'] = meta_df['ID'].str.replace('.wav', '')

        wavs = []
        durations = []
        print(f"Reading durations...")
        for index, row in tqdm(meta_df.iterrows()):
            audio_path = os.path.join(audio_dir, f"fold{row['fold']}", f"{row['ID']}.wav")
            wavs.append(audio_path)
            audio, sr = torchaudio.load(audio_path)
            duration = audio.size(-1) / sr
            durations.append(duration)

        meta_df['duration'] = durations
        meta_df['wav'] = wavs
        meta_df = meta_df[['ID', 'duration', 'wav', 'fsID', 'start', 'end', 'salience', 'fold', 'classID', 'class']]
    else:
        raise NotImplementedError

    dev_df = meta_df[meta_df['fold'].isin(dev_folds)]
    test_df = meta_df[meta_df['fold'].isin(test_folds)]
    train_df = meta_df[~meta_df['fold'].isin(dev_folds + test_folds)]

    dev_df.to_csv(os.path.join(dst, 'dev.csv'), sep=',', index=None)
    test_df.to_csv(os.path.join(dst, 'test.csv'), sep=',', index=None)
    train_df.to_csv(os.path.join(dst, 'train.csv'), sep=',', index=None)

def main():
    args = parse_arguments()

    assert args.dst != '', "Please specify a path for saving output tsv files."

    os.makedirs(args.dst, exist_ok=True)

    dev_folds = folds_to_list(args.dev_folds)
    test_folds = folds_to_list(args.test_folds)

    generate_manifests(args.root, args.dst, dev_folds, test_folds, args.manifest_format)

if __name__ == '__main__':
    main()
