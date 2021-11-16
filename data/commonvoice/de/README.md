# Common Voice German data processing
First, normalize the text in the tsv files to remove punctuation, foreign characters, etc.

python normalize_text.py --src train.tsv,dev.tsv,test.tsv --dst ./proc

