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
python get_words.py --src $SRC --dst ./words.txt --tokens ./tokens.txt --tokens_format other --cat_tokens ./tokens_cat.txt
```

With ```tokens_cat.txt``` it is ensured that no strange characters are kept in the words file.

Also, you can submit more than one text file, separating the paths with commas:
```
SRC1=/path/to/ca-text-corpus/data/common-short-sentences.txt
SRC2=/path/to/ca-text-corpus/data/common-voice-sentences.txt
python get_words.py --src $SRC1,$SRC2 --dst ./words.txt --tokens ./tokens.txt --tokens_format other --cat_tokens ./tokens_cat.txt
```

If you want to get the words from all the txt files, simply input the path to the directory containing those, and all will be taken:
```
SRC_DIR=/path/to/ca-text-corpus/data
python get_words.py --src $SRC_DIR --dst ./words.txt --tokens ./tokens.txt --tokens_format other --cat_tokens ./tokens_cat.txt
```

## Creating a train-test split for sequitur-g2p
If you have a lexicon file with the format "word\tphonemes", it is possible to create a train-test split with ```create_split.py``` script. For now, paths and test split percentage must be modified within the file. The script also adapts to the format necessary for training a g2p model in [sequitur-g2p](https://github.com/sequitur-g2p/sequitur-g2p).
