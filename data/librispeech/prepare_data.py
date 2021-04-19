import argparse
import os
import pandas as pd
import sox

TSV_COLUMNS = ['id', 'audio', 'n_frames', 'tgt_text', 'speaker', 'duration']
PARTITIONS_LIST = ['train-clean-100', 'train-clean-360', 'train-other-500', 'dev-clean', 'dev-other', 'test-clean', 'test-other']

def parse_arguments():
    parser = argparse.ArgumentParser(description='LibriSpeech data preparation script')
    parser.add_argument('--root', default='', help='path to the directory where the dataset is to be found')
    parser.add_argument('--splits', default='all', help='the split names to preprocess, type all to download all partitions, or use commas to indicate a subset: all, train-clean-100, train-clean-360, train-other-500, dev-clean, dev-other, test-clean, test-other')
    parser.add_argument('--dst', default='', help='destination folder to output tsv files')
    parser.add_argument('--audio_format', default='wav', help='audio file format to look for')

    args = parser.parse_args()
    return args

def splits_to_list(splits):
    if splits == 'all':
        splits_list = PARTITIONS_LIST
    else:
        splits_list = splits.split(',')
    return splits_list

def generate_manifest(src, dst, split, audio_format):
    manifest = {c: [] for c in TSV_COLUMNS}
    for dirpath, dirnames, filenames in os.walk(src):
        for filename in filenames:
            if filename.endswith('.txt') and not filename.startswith('.'):
                transcripts_path = os.path.join(dirpath, filename)
                with open(transcripts_path, 'r') as f:
                    for line in f.readlines():
                        sample_id, transcript = line.split(' ', 1)
                        sample_id = sample_id.strip()
                        speaker_id = sample_id.split('-')[0]
                        transcript = transcript.strip().lower()
                        sample_path = os.path.join(dirpath, f"{sample_id}.{audio_format}")
                        duration = sox.file_info.duration(sample_path) * 1000  # miliseconds
                        sampling_rate = sox.file_info.sample_rate(sample_path)
                        n_frames = int(sampling_rate*(duration/1000))

                        assert os.path.isfile(sample_path), f"Audio sample path not found! Path: {sample_path}"

                        manifest['id'].append(sample_id)
                        manifest['audio'].append(sample_path)
                        manifest['n_frames'].append(n_frames)
                        manifest['tgt_text'].append(transcript)
                        manifest['speaker'].append(speaker_id)
                        manifest['duration'].append(duration)

    tsv_path = f'{os.path.join(dst, split)}.tsv'
    df = pd.DataFrame.from_dict(manifest)
    df.to_csv(tsv_path, sep='\t', index=None)

def main():
    args = parse_arguments()

    assert args.splits != '', "Please specify the split names in the --splits argument."
    assert args.dst != '', "Please specify a path for saving output tsv files."

    os.makedirs(args.dst, exist_ok=True)

    splits_list = splits_to_list(args.splits)

    for split in splits_list:
        split_path = os.path.join(args.root, split)
        assert os.path.isdir(split_path), f"LibriSpeech partition directory has not been found! Partition path: {split_path}"

        generate_manifest(split_path, args.dst, split, args.audio_format)

if __name__ == '__main__':
    main()
