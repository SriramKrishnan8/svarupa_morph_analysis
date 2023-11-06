#!/usr/bin/env python3

import os
import sys

import json
import ast

import pandas as pd
from tqdm import tqdm

script, inp, sh_res, scl_res, dcs_rv_res, dcs_av_res, final_res, all_res = sys.argv


def get_contents(f_name):
    """ """
    
    file_ = open(f_name, "r", encoding="utf-8")
    file_contents = file_.read()
    file_.close()
    
    file_list = list(filter(None, file_contents.split("\n")))
    
    dict_list = [ json.loads(item) for item in file_list ]
    
    return dict_list
    

sh_dict_lst = get_contents(sh_res)
scl_dict_lst = get_contents(scl_res)
dcs_rv_dict_lst = get_contents(dcs_rv_res)
dcs_av_dict_lst = get_contents(dcs_av_res)

final_dict_lst = []

print("Generating Results...")
for i in tqdm(range(len(sh_dict_lst))):
    sh_item = sh_dict_lst[i]
    scl_item = scl_dict_lst[i]
    dcs_rv_item = dcs_rv_dict_lst[i]
    dcs_av_item = dcs_av_dict_lst[i]
    
    if sh_item.get("status", "") == "success":
        final_dict_lst.append(sh_item)
    elif scl_item.get("status", "") == "success":
        final_dict_lst.append(scl_item)
    elif dcs_rv_item.get("status", "") == "success":
        final_dict_lst.append(dcs_rv_item)
    elif dcs_av_item.get("status", "") == "success":
        final_dict_lst.append(dcs_av_item)
    else:
        final_dict_lst.append(sh_item)

final_dict_str_lst = [ json.dumps(item, ensure_ascii=False) for item in final_dict_lst ]

final_file = open(final_res, "w", encoding="utf-8")
final_file.write("\n".join(final_dict_str_lst))
final_file.close()

# For converting the results into a dataframe and  
# uploading it into the output file
# The following is required because the default loading of 
# a json as a value in the dataframe results into incorrect
# JSON formatting. Hence, an iterative approach is used here.  
input_df = pd.read_csv(inp, sep='\t')
second_df = pd.DataFrame({"final_json": final_dict_lst})
merged_df = pd.concat([input_df, second_df], axis=1)
merged_df.to_csv('tmp_all.tsv', sep='\t', index=False)

# Here since we know that we have added the final json as 
# last column, we can iteratively operate on them and change
# the JSON formatting
all_det_f = open('tmp_all.tsv', 'r', encoding="utf-8")
all_det_contents = all_det_f.read()
all_det_f.close()

all_det_list = list(filter(None, all_det_contents.split("\n")))
new_list = []
for i in range(len(all_det_list)):
    item = all_det_list[i]
    if i == 0:
        new_list.append(item)
        continue
    
    split_item = item.split("\t")
    old_json = ast.literal_eval(split_item[-1])
    new_json = json.dumps(old_json, ensure_ascii=False)
    
    new_item = split_item[:-1] +  [ new_json ]
    new_joined_item = "\t".join(new_item)
    new_list.append(new_joined_item)

with open(all_res, 'w', encoding="utf-8") as out_f:
    out_f.write("\n".join(new_list))
