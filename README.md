# transliteration

 A seq2seq model for converting Romanized text into its original orthography. This model was built and tested with Armenian in mind, but should be adaptable to any alphabet-based orthography. This model can be used with or without labelled Romanized text, as long as a corpus in the original orthography is available.
 
 This work was inspired by a similar project by [translit-rnn, created by YerevaNN](https://github.com/YerevaNN/translit-rnn).
 
## Current status

This model is in its initial stages. Two completed components are availabe in this repository at the moment.

* __preprocessing.py__ is a script for further preparing the output of a wikidump processed using [WikiExtractor](https://github.com/attardi/wikiextractor). The output of preprocessing.py is a directory with the same substructure as the input directory (ie, extracted the wikidump), and each document within is free of all Wikipedia Document ID tags and has one sentence (or text segment) per line. For instance, to separate text by periods, you would use the following command:

`python3 preprocessing.py --in_dir [path to input directory] --out_dir [path to output directory] --seps '.' --encoding [encoding]`

And to separate by periods and commas, you would use `--seps '.,'`. The encoding argument is optional; utf8 is the default value.

* __romanization.py__ is a script for generating artificial Romanized text when no labelled data is available. It requires a handwritten Romanization key; see __hye_translit_key.txt__ for a formatted example. A character may have any number of ways it can be Romanized, and the Romanization candidates can be separated into more likely and less likely options.

`python3 romanization.py --key [Romanization key] --in_dir [path to input directory] --out_dir [path to output directory] --prop_typical [probability weight assigned to more likely Romanization option] --encoding [encoding]` 

