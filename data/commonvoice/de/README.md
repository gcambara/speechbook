# Common Voice German data processing
First, normalize the text in the tsv files to remove punctuation, foreign characters, etc.
By default, this will also generate corpus txt files.

```
python normalize_text.py --src train.tsv,dev.tsv,test.tsv --dst ./proc
```

Then, extract the corpus with the utility script:
```
python ../../utils/text/tsv_to_txt.py --src ./proc/train.tsv,./proc/dev.tsv,./proc/test.tsv --dst ./proc --column sentence
```

Now, generate lexicon and tokens file:
```
python ../../utils/text/generate_lexicon.py --src ./proc/train.txt --dst ./proc/train_lexicon.txt --tokens ./proc/tokens.txt
```

And, finally, get the lst files from the tsv files:
```
python ../../utils/text/tsv_to_lst.py --src ./proc/test.tsv --dst ./proc --from_type mp3 --to_type wav --base_path /datasets/TALN/speech/ger/commonvoice/cv-corpus-7.0-2021-07-21/de/clips_16k
```