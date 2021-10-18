# transliteration

 A seq2seq model for converting Romanized text into its original orthography. This model was built and tested with Armenian in mind, but should be adaptable to any alphabet-based orthography. This model can be used with or without labelled Romanized text, as long as a corpus in the original orthography is available.
 
 This work was inspired by a similar project by [translit-rnn, created by YerevaNN](https://github.com/YerevaNN/translit-rnn).
 
## Current status

This model is in its initial stages. The preprocessing components are completed and available for use, while the model itself is currently under construction.

## Setting up

This project uses a conda environment, `translit-env.yml`. Once you have Anaconda installed, create the environment and activate it using the following commands:

`conda env create -f translit-env.yml`
`conda activate translit-env`

## Preprocessing

See the `/Preprocessing/` readme for sample commands.

