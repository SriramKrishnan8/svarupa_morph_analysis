import os
import sys

import json

from tqdm import tqdm

import shToTJN as s2t

script, inp, out, out2, text_type = sys.argv

def call_sh_to_term(input_, json_str):
    """ """

    term_json_obj = []
    if "final_json" in json_str:
        status = "skip"
    elif ("unrecognized" in json_str and text_type == "word") or "error" in json_str:
        status = "unrecognized"
        term_json_obj = [
            {"name": input_, "morphList": [], "selected": "false", "source" : ""}
        ]
    else:
        status = "success"
        term_json_str, segmentation = s2t.shToTerm(json_str)
        term_json_obj = json.loads(term_json_str)
    
    return term_json_obj, status


inp_f = open(inp, "r", encoding="utf-8")
inp_contents = inp_f.read()
inp_f.close()

inp_list = list(filter(None, inp_contents.split("\n")))

term_json_dict = {}
term_json_lst = []

for i in tqdm(range(len(inp_list))):
# for i in range(len(inp_list)):
    item = inp_list[i].split("\t")
    
    input_ = item[0]
    json_str = item[-1]
    
    term_json_obj, status = call_sh_to_term(input_, json_str)
    
    if status == "skip":
        continue
    
    term_json_dict[input_] = term_json_obj
    term_json_lst.append((input_ + "\t" + json.dumps(term_json_obj, ensure_ascii=False)))

with open(out, "w", encoding="utf-8") as f:
    json.dump(term_json_dict, f, ensure_ascii=False)
    
with open(out2, "w", encoding="utf-8") as f:
    f.write("\n".join(term_json_lst))
