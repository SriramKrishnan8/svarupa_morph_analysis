# Run SH
echo "Extracting Sanskrit Heritage Analysis..."
cd vedic_morph_analyser_sh/
python3 pada_vishleshika.py DN deva best -i ../sample_input_pada_dev.tsv -o ../sample_res_sh.tsv

# Run SCL
echo "Extracting Samsaadhanii Analysis..."
cd ../scl_morph_interface/
python3 samsaadhanii_morph_analysis.py DN deva -i ../sample_input_pada_dev.tsv -o ../sample_res_scl.tsv

echo "Done."
