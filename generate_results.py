#!/usr/bin/env python3

import os
import sys

import json

from tqdm import tqdm

script, sh_res, scl_res, dcs_res, final_res = sys.argv


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
#dcs_dict_lst = get_contents(dcs_res)

final_dict_lst = []

print("Generating Results...")
for i in tqdm(range(len(sh_dict_lst))):
    sh_item = sh_dict_lst[i]
    scl_item = scl_dict_lst[i]
#    dcs_item = dcs_dict_lst[i]
    
    if sh_item.get("status", "") == "success":
        final_dict_lst.append(sh_item)
    elif scl_item.get("status", "") == "success":
        final_dict_lst.append(scl_item)
#    elif dcs_item.get("status", "") == "success":
#        final_dict_lst.append(dcs_item)
    else:
        final_dict_lst.append(sh_item)
    
final_dict_str_lst = [ json.dumps(item, ensure_ascii=False) for item in final_dict_lst ]

final_file = open(final_res, "w", encoding="utf-8")
final_file.write("\n".join(final_dict_str_lst))
final_file.close()
