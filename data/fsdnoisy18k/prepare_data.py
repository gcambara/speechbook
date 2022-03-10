import argparse
import os
import pandas as pd
import torchaudio
from tqdm import tqdm

PARTITIONS_LIST = ['train', 'test']
SAMPLING_RATE = 44100

def parse_arguments():
    parser = argparse.ArgumentParser(description='FSD noisy 18k data preparation script')
    parser.add_argument('--root', default='/datasets/TALN/speech/audio/fsdnoisy18k', help='path to the directory where the dataset is to be found')
    parser.add_argument('--splits', default='all', help='the split names to preprocess, type all to download all partitions, or use commas to indicate a subset: train, test')
    parser.add_argument('--dst', default='', help='destination folder to output tsv files')
    parser.add_argument('--manifest_format', default='speechbrain', help='format of the output tsv manifest')
    parser.add_argument('--dev_percentage', default=0.1, help='percentage of the train set to split into dev set')

    args = parser.parse_args()
    return args

def splits_to_list(splits):
    if splits == 'all':
        splits_list = PARTITIONS_LIST
    else:
        splits_list = splits.split(',')
    return splits_list

def generate_manifest(src, dst, audio_dir, split, manifest_format, dev_percentage):
    meta_df = pd.read_csv(src)

    if manifest_format == 'speechbrain':
        meta_df = meta_df.rename(columns={"fname": "ID"})
        meta_df['wav'] = meta_df['ID']

        meta_df['ID'] = meta_df['ID'].str.replace('.wav', '')
        meta_df['wav'] = audio_dir + '/' + meta_df['wav'].astype(str)

        durations = []
        print(f"Reading durations in {split} split...")
        for index, row in tqdm(meta_df.iterrows()):
            audio_path = row['wav']
            audio, sr = torchaudio.load(audio_path)
            duration = audio.size(-1) / sr
            durations.append(duration)

        meta_df['duration'] = durations
        if split == 'train':
            meta_df = meta_df[["ID", "duration", "wav", 'aso_id', 'manually_verified', 'noisy_small']]
        else:
            meta_df = meta_df[["ID", "duration", "wav", 'aso_id']]

    else:
        raise NotImplementedError

    if split == 'train' and dev_percentage > 0.0:
        dev_df = meta_df.sample(frac=dev_percentage)
        
        meta_df = meta_df.drop(dev_df.index)
        dev_df.to_csv(os.path.join(dst, 'dev.csv'), sep=',', index=None)

    meta_df.to_csv(os.path.join(dst, f'{split}.csv'), sep=',', index=None)

def main():
    args = parse_arguments()

    assert args.splits != '', "Please specify the split names in the --splits argument."
    assert args.dst != '', "Please specify a path for saving output tsv files."

    os.makedirs(args.dst, exist_ok=True)

    splits_list = splits_to_list(args.splits)

    for split in splits_list:
        meta_path = os.path.join(args.root, 'FSDnoisy18k.meta', f'{split}.csv')
        audio_dir = os.path.join(args.root, f'FSDnoisy18k.audio_{split}')
        assert os.path.isdir(args.root), f"FSD noisy 18k directory has not been found! Dataset path: {args.root}"
        assert os.path.isdir(audio_dir), f"FSD noisy 18k audio directory has not been found! Partition path: {audio_dir}"

        generate_manifest(meta_path, args.dst, audio_dir, split, args.manifest_format, args.dev_percentage)

if __name__ == '__main__':
    main()
