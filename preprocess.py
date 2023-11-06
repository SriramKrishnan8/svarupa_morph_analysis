#!/usr/bin/env python3

import sys

import pandas as pd

script, inp, out_w = sys.argv

input_df = pd.read_csv(inp, sep='\t')
input_df.to_csv(out_w, sep='\t', index=False, columns=["term"], header=False)
