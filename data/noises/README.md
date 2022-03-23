# Noise audio utils

## Generate a noisy dataset
You can generate a noisy dataset with the following command (currently it only supports SpeechBrain pipeline):
```
python generate_noisy_dataset.py --clean_csv /path/to/speechbrain/test.csv --noise_csv ./test.csv --dst_manifest ./test_noisy.csv
```
