# Svarupa-morph-analysis

This package is a collection of modules from Sanskrit Heritage (SH) Platform, Samsaadhanii tools and Digital Corpus of Sanskrit (DCS) for extracting morphological analyses for given word(s). Given a set of words in (.tsv) format, with the other details being indices and ids of each of the words, extract the morphological analyses from SH, Samsaadhanii and DCS. There are 3 modules:

1. Extracting SH analyses
2. Extracting SCL analyses
3. Generating Results
(more modules to follow)

SH and SCL analysers have dedicated packages, [Sanskrit Heritage Morph Interface](https://github.com/SriramKrishnan8/vedic_morph_analyser_sh.git) and [Samsaadhanii Morph Interface](https://github.com/SriramKrishnan8/scl_morph_interface.git), respectively. These are included as submodules in this project.

The following are the constituents:
1. vedic\_morph\_analyser\_sh &rarr; Morphological Analysis powered by Sanskrit Heritage Platform, produces analyses in JSON format
2. scl\_morph\_interface &rarr; Morphological Analysis powered by Samsaadhanii, includes analysis as well as conversion of the analysis to the format identical to SH
3. generate\_results.py &rarr; compares results from SH and SCL and generates the final list of analyses
4. run\_morph\_analysis.sh &rarr; runs all the above processes, requires an input file and an output file
5. input_words.tsv &rarr; sample input words, could be a list of input words or a list of words with their details in a tab-delimited file

## Pre-requisites

The pre-requisites of Sanskrit Heritage Platform Interface are available here: [Sanskrit Heritage Platform Interface](https://github.com/SriramKrishnan8/vedic_morph_analyser_sh.git).
The pre-requisites of Samsaadhanii Morphological Analysis are available here: [Samsaadhanii Morph Analysis Interface](https://github.com/SriramKrishnan8/scl_morph_interface.git).

In addition to these, pandas and tqdm are used in this setup:

```
pip3 install pandas tqdm
```

## Installation

1. Clone this project at a location of choice:

To clone only the main project and not the submodules:
```
git clone https://github.com/SriramKrishnan8/svarupa_morph_analysis.git
```
To clone the main project along with the submodules:
```
git clone --recursive https://github.com/SriramKrishnan8/svarupa_morph_analysis.git
```

2. If only the main project is cloned, the submodules can be loaded as follows:
```
git submodule update --init
```

3. To pull the recent changes in the submodules:
```
git submodule update --remote
```

To pull all the changes in the main repository as well as the submodules:
```
git pull --recurse-submodules
```

4. Refer pre-requisites and install ocaml, camlp4, ocamlbuild, python3, lttoolbox, devtrans

5. Test the setup by running:
```
sh run_morph_analysis.sh input_words.tsv results.tsv
```

