import os
import sys

import json

from tqdm import tqdm


if __name__ == "__main__":
    from generate_wsmp_results import generate_results as gwr
else:
    from sh_to_term_json.generate_wsmp_results import generate_result as gwr


def main():
    """ """
    
    script, inp, res, out, out2 = sys.argv
    
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
        
        sent_json_obj, status = gwr(input_id, input_sent, json_str, "sent")
        
        if status == "skip":
            continue
        
        sent_json_dict[input_sent] = sent_json_obj
        sent_json_lst.append((input_id + "\t" + input_sent + "\t" + json.dumps(sent_json_obj, ensure_ascii=False)))
    
    with open(out, "w", encoding="utf-8") as f:
        json.dump(sent_json_dict, f, ensure_ascii=False)
        
    with open(out2, "w", encoding="utf-8") as f:
        f.write("\n".join(sent_json_lst))


if __name__ == "__main__":
    main()
