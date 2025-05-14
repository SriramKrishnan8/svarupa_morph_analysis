import os
import sys

import json

from tqdm import tqdm

try:
    from sh_to_term_json import shToTJN as s2t
except Exception as e:
    import shToTJN as s2t

def call_sh_to_term(input_, json_str, text_type):
    """ """

    term_json_obj = []
    if "final_json" in json_str:
        status = "skip"
    elif ("unrecognized" in json_str and text_type == "word") or "Error" in json_str:
    # Handle the error properly. Currently all the sub sentence ids are provided 
    # followed by a colon and the hyphen if there is no error, otherwise the error
    # is considered
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
    

def generate_word_results(input_id, input_word, json_str, text_type):
    """ """
    
    morph_analysis, _ = call_sh_to_term(input_word, json_str, text_type)
    
    return morph_analysis
    
    
def generate_results(input_id, input_sent, json_str, text_type):
    """ """
    
    sh_json = json.loads(json_str)
    sent_json = {}
    
    segmentation = sh_json.get("segmentation", [])
    morphs = sh_json.get("morph", [])
    segment_id = 0
    status = ""
    
    # Choosing the first segmentation and getting its terms and analysis
    segs = segmentation[0] if segmentation else ""
    for seg in segs.split(" "):
        if "।" in seg or "." in seg or "॥" in seg:
            continue
        
        segment_id += 1
        seg_input = seg
        
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
        
        term_json_obj, status = call_sh_to_term(seg, seg_json_str, text_type)
        term_id = input_id + "." + str(segment_id)
        sent_json[term_id] = {
#            "term_index" : term_id,
            "term_text" : seg_input,
            "term_json_new" : term_json_obj
        }
    
    return sent_json, status
    
