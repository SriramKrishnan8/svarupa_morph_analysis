#!/bin/bash

# Input
INPUT_FILE=$1
OUTPUT_FILE=$2

# Extract Input
python3 preprocess.py $INPUT_FILE tmp_input.tsv

# Clean Input
# Generate three sets of input: cleaned, sandhied, split
# to be used successively until the word is recognized
# temporarily using the same input file for analyses

# Run SH
echo "Extracting Sanskrit Heritage Analysis..."
cd vedic_morph_analyser_sh/
python3 pada_vishleshika.py DN deva best -i ../tmp_input.tsv -o ../tmp_res_sh.tsv
cd ..

# Run SCL
echo "Extracting Samsaadhanii Analysis..."
cd scl_morph_interface/
python3 samsaadhanii_morph_analysis.py DN deva -i ../tmp_input.tsv -o ../tmp_res_scl.tsv
cd ..

# Run DCS
echo "Extracting DCS Analysis (Rigveda)..."
cd dcs_morph_analysis/
python3 get_dcs_sh_morph.py rv_analysis_map.tsv ../tmp_input.tsv ../tmp_res_dcs_rv.tsv
echo "Extracting DCS Analysis (Atharvaveda)..."
python3 get_dcs_sh_morph.py av_analysis_map.tsv ../tmp_input.tsv ../tmp_res_dcs_av.tsv
cd ..

# Generate final results
python3 generate_results.py $INPUT_FILE tmp_res_sh.tsv tmp_res_scl.tsv tmp_res_dcs_rv.tsv tmp_res_dcs_av.tsv tmp_final_res.tsv $OUTPUT_FILE

rm tmp*

echo "Done."
