import argparse
from einops import rearrange
import os
import pandas as pd
import torch
import torchaudio
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from speechbrain.lobes.augment import EnvCorrupt

class AudioDataset(Dataset):
    def __init__(self, df, root, audio_column, sampling_rate):
        super().__init__()
        self.df = df
        self.root = root
        self.audio_column = audio_column
        self.sampling_rate = sampling_rate

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        sample_info = self.df.loc[index]
        audio_path = sample_info[self.audio_column]
        if self.root != '':
            audio_path = os.path.join(self.root, audio_path)
        wav, src_sr = torchaudio.load(audio_path)
        wav = torchaudio.transforms.Resample(src_sr, self.sampling_rate)(wav)
        wav = rearrange(wav, '1 t -> t')
        return wav, sample_info.to_dict()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Script that contaminates a dataset and stores it to hard disk')
    parser.add_argument('--clean_csv', default='/homedtic/gcambara/projects/ingenious/git/sb_es/recipes/CommonVoice/ASR/CTC/results/wav2vec2_ctc_es/2/save/dev.csv', help='path to the clean data manifest')
    parser.add_argument('--clean_sep', default=',', help='separator for the clean manifest')
    parser.add_argument('--clean_root', default='', help='root path to append to path files in clean data manifest, not to be applied if empty')
    parser.add_argument('--clean_audio_column', default='wav', help='name of the audio column in the clean manifest')
    parser.add_argument('--noise_csv', default='./dev.csv', help='path to the noisy data manifest')
    parser.add_argument('--noise_sep', default='\t', help='separator for the noisy manifest')
    parser.add_argument('--dst_wav', default='/datasets/TALN/speech/esp/commonvoice/cv-corpus-5.1-2020-06-22/es/noise_clips/20220322_1142', help='destination folder to output wav files')
    parser.add_argument('--dst_manifest', default='./dev_noisy.csv', help='destination folder to output manifest files')
    parser.add_argument('--sampling_rate', type=int, default=16000, help='batch size')
    parser.add_argument('--batch_size', type=int, default=1, help='batch size')
    parser.add_argument('--num_workers', type=int, default=2, help='num workers')
    args = parser.parse_args()
    return args

args = parse_arguments()

# ARGUMENTS
df = pd.read_csv(args.clean_csv, args.clean_sep)

dataset = AudioDataset(df, root=args.clean_root,
                       audio_column=args.clean_audio_column,
                       sampling_rate=args.sampling_rate)
dataloader = DataLoader(dataset, batch_size=args.batch_size,
                        shuffle=False, num_workers=args.num_workers)

corrupter = EnvCorrupt(noise_csv=args.noise_csv,
                       noise_prob=1.0,
                       noise_snr_low=0.0,
                       noise_snr_high=15.0,
                       reverb_prob=0.0,
                       babble_prob=0.0)

os.makedirs(args.dst_wav, exist_ok=True)

index = 0
for wav, sample_info in tqdm(dataloader):
    wav = corrupter(wav, torch.ones(args.batch_size))
    original_path = sample_info[args.clean_audio_column][0]
    file_path = os.path.join(args.dst_wav, os.path.basename(original_path))

    torchaudio.save(file_path, src=wav, sample_rate=args.sampling_rate)

    df.at[index, args.clean_audio_column] = file_path
    index += 1

df.to_csv(args.dst_manifest, sep=',', index=None)