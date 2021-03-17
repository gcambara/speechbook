# Log utils

Utilities for handling log files are provided within this directory.

## Usage

### Computing WER scores for utterance from a fairseq log
Currently, fairseq log files only provide the WER score for the whole test set evaluated. With the [fairseq_scores_to_tsv.py](https://github.com/gcambara/speechbook/blob/master/data/utils/audio/fairseq_scores_to_tsv.py) script, it is possible to retrieve WER scores for each utterance, and store the result in a new .tsv file. Optionally, the .tsv file containing the test dataset can be provided via --src_tsv argument, and the WER scores shall be appended to such .tsv, and output in a new one.
```
python fairseq_scores_to_tsv.py --src_log <path_to_fairseq_log> --src_tsv <path_to_test_data_tsv> --dst <path_to_dst_tsv>
```
