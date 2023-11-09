#!/usr/bin/env python3

import sys

import pandas as pd

script, inp_, out_ = sys.argv

input_df = pd.read_csv(inp_, sep='\t')
input_df.to_csv(out_, sep='\t', index=False, columns=["term"], header=False)
