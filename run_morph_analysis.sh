#!/bin/bash

# Input
INPUT_FILE=$1
OUTPUT_FILE=$2

# Extract Input
cut -f 1 $INPUT_FILE > tmp_input.tsv

# Clean Input
# Generate three sets of input: cleaned, sandhied, split
# to be used successively until the word is recognized
# temporarily using the same input file for analyses

# Run SH
echo "Extracting Sanskrit Heritage Analysis..."
cd vedic_morph_analyser_sh/
python3 pada_vishleshika.py DN deva best -i ../tmp_input.tsv -o ../tmp_res_sh.tsv

# Run SCL
echo "Extracting Samsaadhanii Analysis..."
cd ../scl_morph_interface/
python3 samsaadhanii_morph_analysis.py DN deva -i ../tmp_input.tsv -o ../tmp_res_scl.tsv

# Run DCS
#cd ../dcs_morph_analysis/
#python3 

# Generate final results
cd ..
python3 generate_results.py tmp_res_sh.tsv tmp_res_scl.tsv tmp_res_dcs.tsv tmp_final_res.tsv

# Generate Output
num_columns=$(awk -F'\t' '{print NF; exit}' $INPUT_FILE)
if [ "$num_columns" -gt 1 ]; then
    # If there are more than one column 
    cut -f 2-"$num_columns" "$1" > tmp_details.tsv
    paste tmp_input.tsv tmp_details.tsv tmp_final_res.tsv > $OUTPUT_FILE
else
    # If there's only one column
    cut -f 1 "$1" > tmp_input.tsv
    paste tmp_input.tsv tmp_final_res.tsv > $OUTPUT_FILE
fi

rm tmp*

echo "Done."
