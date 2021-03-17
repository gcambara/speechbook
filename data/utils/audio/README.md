# Audio utils

Utilities for handling audio files are provided within this directory.

## Usage

### Converting audio files in batches
Batch conversion of audio files can be done with [convert_audio.py](https://github.com/gcambara/speechbook/blob/master/data/utils/audio/convert_audio.py) Python script.
Such script finds all audio files with a specified type within a source folder, and outputs converted files to a destination folder. Source and destination paths plus file type to search for are mandatory arguments.
```
python convert_audio.py --src <path_to_src_folder> --dst <path_to_dst_folder> --from_type <mp3/wav/...>
```
Supported format modifications imply changes in file type, sampling rate, bit depth and number of channels. If not specified, the output files will have the same format as the input ones.
Parallelization is enabled, so the number of workers can be set as an argument, which is set to one by default.
For example, for converting mp3 audio files to wav files with 16kHz sampling rate, 16-bits and one channel, using 8 workers, the following command is used:
```
python convert_audio.py --src <path_to_src_folder> --dst <path_to_dst_folder> --from_type mp3 --to_type wav --sampling_rate 16000 --bit_depth 16 --channels 1 --workers 8
```

### Computing voice features using Praat
It is possible to compute several voice features like F0 mean, HNR, jitter or shimmer measurements, using [compute_voice_features.py](https://github.com/gcambara/speechbook/blob/master/data/utils/audio/compute_voice_features.py) script based on Praat-Parselmouth, a Praat wrapper for Python. This is convenient for batch processing of files, where we have a .tsv file with an audio sample per row. The script computes several voice features and appends them with new columns in a new generated .tsv file, that also contains all the information from the original .tsv.
```
python compute_voice_features.py --src <path_to_input_tsv> --dst <path_to_output_tsv> --min_f0 50 --max_f0 400
```

Currently, the mandatory format for the .tsv files is to have the sample ID in the first column, and the path to the audio file in the second one. This is the typical format of .tsv and .lst files adapted for wav2letter/Flashlight and fairseq framework pipelines.