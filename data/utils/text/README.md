# Text utils
Utilities for handling text files are provided within this directory.

## Usage

### Extracting sentences in TSV files to plain txt files
Just call the following script, indicating the source TSV files, the output destination folder, and the name of the column containing the sentences:
```
python tsv_to_txt.py --src ../../commonvoice/de/train.tsv,../../commonvoice/de/dev.tsv,../../commonvoice/de/test.tsv --dst ./proc --column sentence
```