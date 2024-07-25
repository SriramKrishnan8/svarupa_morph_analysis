#!/bin/bash

# Input
INPUT_FILE=$1
OUTPUT_FILE=$2

echo "Cleaning sentences..."
python3 clean.py $INPUT_FILE tmp_wsmp_cleaned_sentences.tsv

# Run SH
echo "Extracting Sanskrit Heritage Analysis..."
cd vedic_morph_analyser_sh/
python3 wsmp_sh.py DN deva sent first -i ../tmp_wsmp_cleaned_sentences.tsv -o ../tmp_wsmp_res_sh.tsv
cd ..

# SH to term_json
cd sh_to_term_json/
python3 generate_wsmp_results.py ../$INPUT_FILE ../tmp_wsmp_res_sh.tsv ../tmp_term_wsmp_res.json ../$OUTPUT_FILE "sent"

# rm tmp*

echo "Done."
