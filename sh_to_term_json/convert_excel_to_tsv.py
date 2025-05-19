#!/usr/bin/env python3

import sys

script, in_, out_ = sys.argv

def main():
    """ """
        
    # Validate if the file is a valid TSV or Excel file
    if in_.endswith('.xls') in_.endswith('.xlsx')):
        # Handle Excel to TSV conversion
        try:
            excel_data = pd.read_excel(in_, engine='openpyxl')
            # tsv_path = os.path.join(process_folder, file.filename.replace('.xlsx', '.tsv'))
            excel_data.to_csv(out_, sep='\t', index=False)
        except Exception as e:
            return "error"
    else:
        return "error"

if __name__ == '__main__':
    main()
