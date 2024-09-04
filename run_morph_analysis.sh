#!/bin/bash

# Input
INPUT_FILE=$1

# Extract Input
python3 preprocess.py $INPUT_FILE tmp_input_orig.tsv

# Clean Input
# Generate three sets of input: cleaned, sandhied, split
# to be used successively until the word is recognized
# temporarily using the same input file for analyses

python3 process_special_chars.py tmp_input_orig.tsv tmp_input_modified.tsv tmp_input_segmented.tsv tmp_input_sandhied.tsv tmp_input_hyphenated.tsv
# cut -d'	' -f3 tmp_input_modified.tsv > tmp_input_sandhied.tsv
# cut -d'	' -f4 tmp_input_modified.tsv > tmp_input_hyphenated.tsv

# Run SH
echo "Extracting Sanskrit Heritage Analysis..."
cd vedic_morph_analyser_sh/
echo "Sandhied..."
python3 pada_vishleshika.py DN deva word best -i ../tmp_input_sandhied.tsv -o ../tmp_res_sh_sa.tsv
echo "Hyphenated..."
python3 pada_vishleshika.py DN deva word best -i ../tmp_input_hyphenated.tsv -o ../tmp_res_sh_hy.tsv
cd ..

# Run SCL
echo "Extracting Samsaadhanii Analysis..."
cd scl_morph_interface/
echo "Sandhied..."
python3 samsaadhanii_morph_analysis.py DN deva -i ../tmp_input_sandhied.tsv -o ../tmp_res_scl_sa.tsv
echo "Hyphenated..."
python3 samsaadhanii_morph_analysis.py DN deva -i ../tmp_input_hyphenated.tsv -o ../tmp_res_scl_hy.tsv
cd ..

# Run DCS
cd dcs_morph_analysis/
echo "Extracting DCS Analysis (Rigveda)..."
echo "Sandhied..."
python3 get_dcs_sh_morph.py rv_analysis_map.tsv ../tmp_input_sandhied.tsv ../tmp_res_dcs_rv_sa.tsv
echo "Hyphenated..."
python3 get_dcs_sh_morph.py rv_analysis_map.tsv ../tmp_input_hyphenated.tsv ../tmp_res_dcs_rv_hy.tsv
echo "Extracting DCS Analysis (Atharvaveda)..."
echo "Sandhied..."
python3 get_dcs_sh_morph.py av_analysis_map.tsv ../tmp_input_sandhied.tsv ../tmp_res_dcs_av_sa.tsv
echo "Hyphenated..."
python3 get_dcs_sh_morph.py av_analysis_map.tsv ../tmp_input_hyphenated.tsv ../tmp_res_dcs_av_hy.tsv
cd ..

# Generate final results
# python3 generate_results_new.py $INPUT_FILE tmp_res_sh_sa.tsv tmp_res_sh_hy.tsv tmp_res_scl_sa.tsv tmp_res_scl_hy.tsv tmp_res_dcs_rv_sa.tsv tmp_res_dcs_rv_hy.tsv tmp_res_dcs_av_sa.tsv tmp_res_dcs_av_hy.tsv tmp_final_res.tsv final_result_all.tsv cache.json tmp_overall_analysis.tsv

# Generate SH final results
[ ! -f cache_sh.json ] && echo "{}" > cache_sh.json
python3 generate_results_new_sh_scl.py $INPUT_FILE tmp_res_sh_sa.tsv tmp_res_sh_hy.tsv tmp_res_sh_final.tsv tmp_res_sh_final_all.tsv cache_sh.json tmp_res_sh_overall_analysis.tsv "sh"
# Generate SCL final results
[ ! -f cache_scl.json ] && echo "{}" > cache_scl.json
python3 generate_results_new_sh_scl.py $INPUT_FILE tmp_res_scl_sa.tsv tmp_res_scl_hy.tsv tmp_res_scl_final.tsv tmp_res_scl_final_all.tsv cache_scl.json tmp_res_scl_overall_analysis.tsv "scl"
# Generate DCS final results
python3 generate_results_new_dcs.py $INPUT_FILE tmp_res_dcs_rv_sa.tsv tmp_res_dcs_rv_hy.tsv tmp_res_dcs_av_sa.tsv tmp_res_dcs_av_hy.tsv tmp_res_dcs_final.tsv tmp_res_dcs_final_all.tsv tmp_res_dcs_overall_analysis.tsv
paste tmp_input_orig.tsv tmp_input_segmented.tsv tmp_input_sandhied.tsv tmp_input_hyphenated.tsv tmp_res_dcs_rv_sa.tsv tmp_res_dcs_av_sa.tsv tmp_res_dcs_rv_hy.tsv tmp_res_dcs_av_hy.tsv tmp_res_dcs_final.tsv > tmp_res_dcs_for_sheet.tsv

echo "Generating term_json for SH analyses..."
cd sh_to_term_json/
python3 sh_to_term_json_run.py ../tmp_res_sh_overall_analysis.tsv ../sh_term_res.json ../sh_term_res.tsv ../sh_term_res.xlsx word
echo "Generating term_json for SCL analyses..."
python3 sh_to_term_json_run.py ../tmp_res_scl_overall_analysis.tsv ../scl_term_res.json ../scl_term_res.tsv ../scl_term_res.xlsx word
echo "Generating term_json for DCS analyses..."
python3 sh_to_term_json_run.py ../tmp_res_dcs_overall_analysis.tsv ../dcs_term_res.json ../dcs_term_res.tsv ../dcs_term_res.xlsx word
cd ..

rm tmp*

echo "Done."
