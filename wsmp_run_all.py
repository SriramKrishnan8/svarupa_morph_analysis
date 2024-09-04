import requests

import json

import re

from tqdm import tqdm

url = "http://34.212.84.51:5000/sh-wsmp"
#url = "http://10.21.72.127:5000/sh-wsmp"

def call_wsmp_sh(mantra_id, mantra_text):
    """ """
    
    params = {
        'mantra_index': mantra_id,
        'mantra': mantra_text
    }
    
    response = requests.get(url, params=params)
#    print(mantra_id, mantra_text)
#    print(response.json(), response.status_code)
    
    try:
        data = json.dumps(response.json(), ensure_ascii=False)
        status = "success"
    except ValueError as e:
        data = ""
        status = "json-parse-error"
    
    return data


def call_wsmp_sh_all(in_file, out_file):
    """ """
    
    file_ = open(in_file, "r", encoding="utf-8")
    contents_ = file_.read()
    lines_ = list(filter(None, contents_.split("\n")))
    file_.close()
    
    results = []
    for i in range(len(lines_)):
#    for i in tqdm(range(len(lines_))):
        line = lines_[i]
        mantra_id, mantra_text = line.split("\t")
        res = call_wsmp_sh(mantra_id, mantra_text)
        results.append(res)
    
    file_ = open(out_file, "w", encoding="utf-8")
    lines_ = "\n".join(results)
    file_.write(lines_)
    file_.close()

#call_wsmp_sh_all("ab_1.tsv", "ab_1_res.tsv")
call_wsmp_sh_all("116.tsv", "116_res2.tsv")
