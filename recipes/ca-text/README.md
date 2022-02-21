# Catalan Text Corpus
Find here some script utilities for processing the text in the [Catalan Text Corpus](https://github.com/Softcatala/ca-text-corpus).

## Downloading the corpus
Simply git clone the repo:
```
git clone https://github.com/Softcatala/ca-text-corpus.git
```
## Generating a words file
To generate a file containing each unique word from a text corpus, in a single line, run the following command:
```
SRC=/path/to/ca-text-corpus/data/common-short-sentences.txt
python get_words.py --src $SRC --dst ./words.txt --tokens ./tokens.txt --tokens_format other
```
