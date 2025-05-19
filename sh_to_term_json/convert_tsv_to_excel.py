#!/usr/bin/env python3

import sys

import pandas as pd

script, in_, out_ = sys.argv

def main():
    """ """

    # Input and output file paths
    tsv_file = in_
    excel_file = out_
    
    # Read the TSV file into a DataFrame
    df = pd.read_csv(in_, sep='\t')
    
    # Write the DataFrame to an Excel file
    df.to_excel(out_, index=False)
    
    print(f"TSV file '{tsv_file}' has been converted to Excel file '{excel_file}'.")
    

if __name__ == '__main__':
    main()
