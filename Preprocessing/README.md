# Pre-processing

 The scripts in this folder are used for a variety of preprocessing tasks, described below.
 
##  __preprocess_wikidump.py__ 

This is a script for further preparing the output of a wikidump processed using [WikiExtractor](https://github.com/attardi/wikiextractor). The output of is a directory with the same substructure as the input directory (ie, the same structure as an extracted wikidump), and each document within is free of all Wikipedia Document ID tags and has one sentence (or text segment) per line. For instance, to separate text by periods, you would use the following command:

`python3 preprocess_wikidump.py --in_dir [path to input directory] --out_dir [path to output directory] --seps '.' --encoding [encoding]`

And to separate by periods and commas, you would use `--seps '.,'`. The encoding argument is optional; utf8 is the default value.

## __generate_romanization.py__ 

This is a script for generating artificial Romanized text when no labelled data is available. It requires a handwritten Romanization key; see __transliteration/RomanizationKeys__ for formatted examples. A character may have any number of ways it can be Romanized, and the Romanization candidates can be separated into more likely and less likely options.

`python3 generate_romanization.py --key [Romanization key] --in_dir [path to input directory] --out_dir [path to output directory] --prop_typical [probability weight assigned to more likely Romanization option] --encoding [encoding]` 

## __clean_and_split_data.py__

This script generates the train/dev/test splits for the data after removing lines that contain characters with fewer than a specified number of occurences. Because wikidumps often contain some text that is not in the language of interest, removing rare characters can greatly reduce the input and output vocabulary.

`python3 clean_and_split_data.py [spource directory] [target directory] [output directory] [inimum frequency]`

