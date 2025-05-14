import os
import sys

import json

import pandas as pd

from tqdm import tqdm

if __name__ == "__main__":
    from sh_to_term_json_res import call_sh_to_term
else:
    from sh_to_term_json.sh_to_term_json_res import call_sh_to_term

script, inp, out, out2, out_excel, text_type = sys.argv

inp_f = open(inp, "r", encoding="utf-8")
inp_contents = inp_f.read()
inp_f.close()

inp_list = list(filter(None, inp_contents.split("\n")))

term_json_dict = {}
term_json_lst = []
headers = []

for i in tqdm(range(len(inp_list))):
# for i in range(len(inp_list)):
    item = inp_list[i].split("\t")
    if "term_text" in item:
        continue
    
    input_ = item[0]
    all_det = item[:-1]
    json_str = item[-1]
    
    term_json_obj, status = call_sh_to_term(input_, json_str, text_type)
    
    if status == "skip":
        headers = all_det
        continue
    
    term_json_dict[input_] = term_json_obj
    term_json_lst.append((all_det + [ json.dumps(term_json_obj, ensure_ascii=False) ]))

with open(out, "w", encoding="utf-8") as f:
    json.dump(term_json_dict, f, ensure_ascii=False)
    
term_json_lst_str = [ "\t".join(x) for x in term_json_lst ]

with open(out2, "w", encoding="utf-8") as f:
    f.write("\n".join(term_json_lst_str))

df = pd.DataFrame(term_json_lst, columns=headers[:-1] + ['term_json_new'])
df.to_excel(out_excel, index=False)
