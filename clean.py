import os
import sys

import re

from tqdm import tqdm

import cleaning as cln

script, in_, out_ = sys.argv


file_ = open(in_, 'r', encoding="utf-8")
all_text = file_.read()
file_.close()

all_lines = list(filter(None, all_text.split("\n")))
new_list = []

#print("Cleaning terms...")
for i in tqdm(range(len(all_lines))):
    line = all_lines[i]
    
    items = line.split("\t")
    
    id_ = items[0]
    sent_ = items[1]
    new_text = cln.remove_svara(line)
    new_text = cln.remove_non_unicode(new_text)
    new_text = cln.check_chandrabindu(new_text)
    new_text = cln.replace_others(new_text)
    
    new_list.append(new_text)


file_ = open(out_, 'w', encoding="utf-8")
file_.write("\n".join(new_list))
file_.close()

