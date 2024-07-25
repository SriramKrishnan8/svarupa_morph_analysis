import os
import sys

import re

from tqdm import tqdm

import cleaning as cln
import handle_iti as iti

script, in_, out_mo, out_se, out_sa, out_hy = sys.argv


file_ = open(in_, 'r', encoding="utf-8")
all_text = file_.read()
file_.close()

all_lines = list(filter(None, all_text.split("\n")))
# new_list = []

iti_entries_dict = iti.get_iti_strings()

modified_list = []
segmented_list = []
sandhied_list = []
hyphenated_list = []

print("Cleaning terms...")
for i in tqdm(range(len(all_lines))):
    line = all_lines[i]
    new_text = cln.remove_svara(line)
    new_text = cln.remove_non_unicode(new_text)
    new_text = cln.check_chandrabindu(new_text)
    new_text = cln.replace_others(new_text)
    new_text = cln.replace_avagraha(new_text)

    # Insert sandhi module
    
    cleaned_term = new_text
    segmented_term, sandhied_term, hyphenated_term = iti.replace_iti(
        new_text, iti_entries_dict
    )
    
    # Instead of saving all forms, only the sandhied and hyphenated are stored
    # new_list.append((line, cleaned_term, sandhied_term, hyphenated_term))
    modified_list.append(cleaned_term)
    segmented_list.append(segmented_term)
    sandhied_list.append(sandhied_term)
    hyphenated_list.append(hyphenated_term)

# updated_list = ["\t".join(item) for item in new_list]

file_ = open(out_mo, 'w', encoding="utf-8")
file_.write("\n".join(modified_list))
file_.close()

file_ = open(out_se, 'w', encoding="utf-8")
file_.write("\n".join(segmented_list))
file_.close()

file_ = open(out_sa, 'w', encoding="utf-8")
file_.write("\n".join(sandhied_list))
file_.close()

file_ = open(out_hy, 'w', encoding="utf-8")
file_.write("\n".join(hyphenated_list))
file_.close()
