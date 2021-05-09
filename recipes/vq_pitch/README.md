# Voice Quality and Pitch Features in Transformer-Based Speech Recognition

Voice quality features like jitter and shimmer have proven to enhance the performance in several speech tasks like speaker diarization or speaker recognition, for instance. In our work presented to the InterSpeech 2021 conference, we show that using such features along with pitch helps a Transformer-based ASR model to reduce the word error rate, specially when less amount of training hours are available.

Find here the recipe to run ASR experiments using voice quality and pitch features, with the [fairseq toolkit](https://github.com/pytorch/fairseq). The provided scripts are set to train and test against LibriSpeech dataset, using the 100h and the 960h training sets.

## Setting up the repo

The implementation of voice quality and pitch features to a Transformer-based model has been done in a fairseq fork. First, you will need to clone such repo, move to the implementation branch and install fairseq:

```
git clone https://github.com/gcambara/fairseq.git fairseq_vq
cd fairseq_vq
git checkout pitch
pip install --editable ./
```

## Preparing the data

In order to prepare the LibriSpeech data for the fairseq pipeline, use the following script as told in the fairseq ASR recipe:
```
pip install pandas torchaudio sentencepiece
python examples/speech_to_text/prep_librispeech_data.py \
  --output-root ${LS_ROOT} --vocab-type unigram --vocab-size 10000
``` 
This script will download the LibriSpeech data and will generate the vocabulary files and a TSV manifest with the sample IDs, paths, transcripts, etc. Now, precompute pitch, jitter and shimmer features, so training and decoding is faster:
```
python examples/speech_to_text/prep_librispeech_feats.py \
  --output-root ${LS_ROOT} --folder_name vq_features --config-yaml ${SPEECHBOOK_ROOT}/recipes/vq_pitch/config/config_40fb_precomputation.yaml 
```
