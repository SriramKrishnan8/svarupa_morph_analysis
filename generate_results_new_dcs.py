#!/usr/bin/env python3

import os
import sys

import json
import ast

import pandas as pd
from tqdm import tqdm

script, inp, dcs_rv_res_sa, dcs_rv_res_hy, dcs_av_res_sa, dcs_av_res_hy, final_res, final_res_all, all_res = sys.argv


def get_contents(f_name):
    """ """
    
    file_ = open(f_name, "r", encoding="utf-8")
    file_contents = file_.read()
    file_.close()
    
    file_list = list(filter(None, file_contents.split("\n")))
    
    dict_list = [ json.loads(item) for item in file_list ]
    
    return dict_list


def get_confirmation(analysis_dict):
    """ """

    status = False
    if analysis_dict.get("status", "") == "success":
        status = True

    return analysis_dict, status

def merge_sa_hy(sa_dict, hy_dict, source):
    """ """

    sa_status = (sa_dict.get("status", "") == "success")
    hy_status = (hy_dict.get("status", "") == "success")
    
    new_dict = {}
    if not sa_status and not hy_status:
        new_dict = sa_dict.copy()
    elif sa_status and not hy_status:
        new_dict = sa_dict.copy()
    elif not sa_status and hy_status:
        new_dict = hy_dict.copy()
    elif sa_dict == hy_dict:
        new_dict = sa_dict.copy()
    else:
        new_dict["input"] = sa_dict["input"]
        new_dict["status"] = "success"
        new_dict["source"] = sa_dict.get("source", source)
        segmentation_set = set(sa_dict["segmentation"] + hy_dict["segmentation"])
        new_dict["segmentation"] = list(segmentation_set)
        sa_morph_list = [ dict(item) for item in sa_dict["morph"] ]
        hy_morph_list = [ dict(item) for item in hy_dict["morph"] ]
        
        morph_lst = []
        for itm in sa_morph_list:
            morph_lst.append(itm)
        for itm in hy_morph_list:
            if itm not in morph_lst:
                morph_lst.append(itm)
        new_dict["morph"] = list(morph_lst)
    
    return new_dict


def generate_unrecognized_json(word):
    """ """
    
    new_dict = {}
    new_dict["input"] = word
    new_dict["status"] = "unrecognized"
    
    return new_dict


dcs_rv_dict_lst_sa = get_contents(dcs_rv_res_sa)
dcs_rv_dict_lst_hy = get_contents(dcs_rv_res_hy)

dcs_av_dict_lst_sa = get_contents(dcs_av_res_sa)
dcs_av_dict_lst_hy = get_contents(dcs_av_res_hy)

final_dict_lst = []
final_dict_lst_all = []

inp_file = open(inp, "r", encoding="utf-8")
inp_contents = inp_file.read()
inp_file.close()

inp_list = list(filter(None, inp_contents.split("\n")))

print("Generating DCS Results...")
for i in tqdm(range(len(dcs_rv_dict_lst_sa))):
    dcs_rv_item_sa, dcs_rv_sa = get_confirmation(dcs_rv_dict_lst_sa[i])
    dcs_rv_item_hy, dcs_rv_hy = get_confirmation(dcs_rv_dict_lst_hy[i])
    
    dcs_av_item_sa, dcs_av_sa = get_confirmation(dcs_av_dict_lst_sa[i])
    dcs_av_item_hy, dcs_av_hy = get_confirmation(dcs_av_dict_lst_hy[i])
    
    success = True
    if dcs_rv_sa:
        final_dict_lst.append(dcs_rv_item_sa)
    elif dcs_av_sa:
        final_dict_lst.append(dcs_av_item_sa)
    elif dcs_rv_hy:
        final_dict_lst.append(dcs_rv_item_hy)
    elif dcs_av_hy:
        final_dict_lst.append(dcs_av_item_hy)
    else:
        success = False
        final_dict_lst.append(generate_unrecognized_json(inp_list[i + 1]))
    
    if success:
        new_dict = {}
        
        temp_dict_1 = merge_sa_hy(dcs_rv_item_sa, dcs_rv_item_hy, "dcs")
        
        temp_dict_2 = merge_sa_hy(dcs_av_item_sa, dcs_av_item_hy, "dcs")
        
        new_dict["dcs"] = merge_sa_hy(temp_dict_1, temp_dict_2, "dcs")
        
        final_dict_lst_all.append(new_dict)
    else:
        final_dict_lst_all.append(generate_unrecognized_json(inp_list[i + 1]))

final_dict_str_lst = [ json.dumps(item, ensure_ascii=False) for item in final_dict_lst ]
final_dict_str_lst_all = [ json.dumps(item, ensure_ascii=False) for item in final_dict_lst_all ]

final_file = open(final_res, "w", encoding="utf-8")
final_file.write("\n".join(final_dict_str_lst))
final_file.close()

final_file = open(final_res_all, "w", encoding="utf-8")
final_file.write("\n".join(final_dict_str_lst_all))
final_file.close()

# For converting the results into a dataframe and  
# uploading it into the output file
# The following is required because the default loading of 
# a json as a value in the dataframe results into incorrect
# JSON formatting. Hence, an iterative approach is used here.  
input_df = pd.read_csv(inp, sep='\t')
second_df = pd.DataFrame({"final_json": final_dict_lst})
merged_df = pd.concat([input_df, second_df], axis=1)
merged_df.to_csv('tmp_all_dcs.tsv', sep='\t', index=False)

# Here since we know that we have added the final json as 
# last column, we can iteratively operate on them and change
# the JSON formatting
all_det_f = open('tmp_all_dcs.tsv', 'r', encoding="utf-8")
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
