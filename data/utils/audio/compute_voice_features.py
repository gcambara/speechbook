""" 
Batch computing of voice features for all the audios in a 
tsv file. It is expected that sample ID is found at the first column,
and the path to the audio file is found at the second one.
This is the typical format in wav2letter/Flashlight and fairseq
pipelines.
"""

import os
import argparse
import librosa
import numpy as np
import pandas as pd
import parselmouth
from tqdm import tqdm
from parselmouth.praat import call

def get_delta_F0(pitch, order=1, width=9, unvoiced_mode='drop_all'):
    pitch_values = pitch.selected_array['frequency']
    pitch_values = np.array(pitch_values)
    
    if unvoiced_mode == 'drop_all':
        pitch_values = pitch_values[pitch_values != 0.0]
    else:
        raise NotImplementedError
    
    delta_pitch = librosa.feature.delta(pitch_values, order=order, width=width)
    return delta_pitch
  
def measure_voice_features(sound, f0min, f0max, unit):
    sound = parselmouth.Sound(sound) # read the sound
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    delta_F0 = get_delta_F0(pitch)
    mean_delta_F0 = delta_F0.mean()
    stdev_delta_F0 = delta_F0.std()
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return [meanF0, stdevF0, mean_delta_F0, stdev_delta_F0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer]

parser = argparse.ArgumentParser(description="Compute voice quality features") 
parser.add_argument("--src", default="", help="source tsv file with speech samples per row", required=True)
parser.add_argument("--dst", default="", help="destination tsv file with the appended voice quality measurements", required=True)
parser.add_argument("--min_f0", type=int, default=50, help="lower bound for F0 computation")
parser.add_argument("--max_f0", type=int, default=400, help="lower bound for F0 computation")
args = parser.parse_args()
print("Arguments")
print(args)

df = pd.read_csv(args.src, sep='\t')

voice_features_list = []
for index, row in tqdm(df.iterrows()):
    path = row[1]
    assert os.path.isfile(path), f"The path \"{path}\" does not lead to a file! Check that the second column in your tsv file contains paths to audio files."

    sound = parselmouth.Sound(path)
    voice_features = measure_voice_features(sound, args.min_f0, args.max_f0, "Hertz")

    current_information = row.tolist()
    current_information += voice_features

    voice_features_list.append(current_information)

columns = df.columns.tolist()
columns += ['mean_f0', 'stdev_f0', 'mean_delta_f0', 'stdev_delta_f0', 'hnr', 'local_jitter', 'local_absolute_jitter', 'rap_jitter', 'ppq5_jitter', 'ddp_jitter', 'local_shimmer', 'localdb_shimmer', 'apq3_shimmer', 'aqpq5_shimmer', 'apq11_shimmer', 'dda_shimmer']
features_df = pd.DataFrame(voice_features_list, columns=columns)

features_df.to_csv(args.dst, sep='\t', index=None)
