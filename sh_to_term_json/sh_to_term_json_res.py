import os
import sys

import json

from tqdm import tqdm

import shToTJN as s2t

def call_sh_to_term(input_, json_str, text_type):
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

