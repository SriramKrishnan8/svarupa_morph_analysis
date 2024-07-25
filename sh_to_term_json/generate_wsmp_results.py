import os
import sys

import json

from tqdm import tqdm

import shToTJN as s2t

script, inp, res, out, out2, text_type = sys.argv

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


def get_morphs(morph_list, segment):
    """ """
    
    morphs = []
    for morph in morph_list:
        word = morph.get("word", "")
        if segment == word:
            morphs.append(morph)
    
    return morphs
    

def generate_results(input_id, input_sent, json_str):
    """ """
    
    sh_json = json.loads(json_str)
    sent_json = {}
    
    segmentation = sh_json.get("segmentation", [])
    morphs = sh_json.get("morph", [])
    segment_id = 0
    status = ""
    
    segs = segmentation[0] if segmentation else ""
    for seg in segs.split(" "):
        segment_id += 1
        seg_input = seg
        
        if "।" in seg or "." in seg:
            continue
        
        seg_status = "unrecognized" if ("#" in seg or "?" in seg) else "success"
        seg_segmentation = [ seg ]
        seg_morph = []
        
        if "-" in seg:
            components = seg.split("-")
            for cpnt in components[:-1]:
                seg_morph += get_morphs(morphs, cpnt + "-")
            seg_morph += get_morphs(morphs, components[-1])
        else:
            seg_morph += get_morphs(morphs, seg)
        
        seg_json = {
            "input": seg_input,
            "status": seg_status,
            "segmentation": seg_segmentation,
            "morph": seg_morph,
            "source": "SH",
        }
        
        seg_json_str = json.dumps(seg_json, ensure_ascii=False)
        
        term_json_obj, status = call_sh_to_term(seg, seg_json_str)
        term_id = input_id + "." + str(segment_id)
        sent_json[term_id] = {
#            "term_index" : term_id,
            "term_text" : seg_input,
            "term_json_new" : term_json_obj
        }
    
    return sent_json, status


inp_f = open(inp, "r", encoding="utf-8")
inp_contents = inp_f.read()
inp_f.close()

res_f = open(res, "r", encoding="utf-8")
res_contents = res_f.read()
res_f.close()

inp_list = list(filter(None, inp_contents.split("\n")))
res_list = list(filter(None, res_contents.split("\n")))

sent_json_dict = {}
sent_json_lst = []

for i in tqdm(range(len(inp_list))):
# for i in range(len(inp_list)):
    item = inp_list[i].split("\t")
    
    input_id = item[0]
    input_sent = item[-1]
    
    json_str = res_list[i]
    
    sent_json_obj, status = generate_results(input_id, input_sent, json_str)
    
    if status == "skip":
        continue
    
    sent_json_dict[input_sent] = sent_json_obj
    sent_json_lst.append((input_id + "\t" + input_sent + "\t" + json.dumps(sent_json_obj, ensure_ascii=False)))

with open(out, "w", encoding="utf-8") as f:
    json.dump(sent_json_dict, f, ensure_ascii=False)
    
with open(out2, "w", encoding="utf-8") as f:
    f.write("\n".join(sent_json_lst))
