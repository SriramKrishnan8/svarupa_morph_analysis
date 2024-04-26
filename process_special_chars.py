import os
import sys

import re

from tqdm import tqdm

import handle_iti as iti

script, in_, out_mo, out_se, out_sa, out_hy = sys.argv


svaras = [ '\uA8E1', '\uA8E2', '\uA8E3', '\uA8E4', '\uA8E5', '\uA8E6', '\uA8E7', '\uA8E8', '\uA8E9', '\uA8E0', '\uA8EA', '\uA8EB', '\uA8EC', '\uA8EE', '\uA8EF', '\u030D', '\u0951', '\u0952', '\u0953', '\u0954', '\u0945' ]
special_characters = [ '\uf15c', '\uf193', '\uf130', '\uf1a3', '\uf1a2', '\uf195', '\uf185', '\u200d', '\u200c', '\u1CD6', '\u1CD5', '\u1CE1', '\u030E', '\u035B', '\u0324', '\u1CB5', '\u0331', '\u1CB6', '\u032B', '\u0308', '\u030D', '\u0942', '\uF512', '\uF693', '\uF576', '\uF11E', '\u1CD1', '\u093C', '\uF697', '\uF6AA', '\uF692' ]


def replace_chandrabindu(cb, input_string):
    """ Replaces chandrabindu
    """
    
    text = input_string
    if cb in input_string:
        if input_string[-1] == cb:
            text = text.replace(cb, "म्")
        else:
            text = text.replace(cb, "ं")
    
    return text


def check_chandrabindu(input_string):
    """ Checks and replaces chandrabindu
    """
    
    text = input_string
    
    # The following condition is added to replace chandrabindu
    # which comes adjacent to characters, with m or .m 
    # depending upon its position
    chandrabindus = ["ꣳ", "", "", ""]
    
    for item in chandrabindus:
        text = replace_chandrabindu(item, text)
    
    return text


def remove_non_unicode(text):
    """ Removes non-unicode characters
    """
    
    # [^a-zA-Z0-9,().ळळ्꣢꣡꣯꣬ॅ᳡꣫꣣: ॐ\u200d\u200c\u1CD6\u1CD5\u1CE1ꣳऱ्r़\]|-]
    pattern = re.compile(r'[꣡꣬᳡़꣯꣢꣣ॅ꣫]')
    
    cleaned_string = pattern.sub('', text)
    
    return cleaned_string
    
    
def replace_avagraha(input_string):
    """ Replaces avagraha with hyphen
    """
    
    text = input_string
    text = text.replace("ऽ", "-")
    
    return text


def remove_svara_iter(text):
    """ Removes svaras by iterating through the text
    """
    
    new_text = []
    
    for char in text:
        if char in (svaras + special_characters):
            continue
        new_text.append(char)
   
    modified_text = "".join(new_text)
    
    return modified_text
    

def remove_svara_regexp(with_svara):
    """ Removes svaras using regexp module
    """

    pattern = re.compile(r'[\uA8E1\uA8E2\uA8E3\uA8E4\uA8E5\uA8E6\uA8E7\uA8E8\uA8E9\uA8E0\uA8EA\uA8EB\uA8EC\uA8EE\uA8EF\u0945\u0951\u0952\u0953\u0954\uf15c\uf193\uf130\uf1a3\uf1a2\uf195\uf185\u200d\u200c\u1CD6\u1CD5\u1CE1\u030E\u035B\u0324\u1CB5\u0331\u1CB6\u032B\u0308\u030D\u0942\uF512\uF693\uF576\uF11E\u1CD1\u093C\uF697\uF6AA\uF692]')
#    pattern = re.compile(r'[꣡꣫\uf15c\uf193\uf1a3\uf1a3꣯꣣꣡\uf195\uf1a2\uf185꣬᳡़꣯꣢꣣ॅ꣫\u200d\u200c\uF512\u1CD6\u1CD5\u1CE1\uA8EB\u030E\u035B\u0324\uA8E2\u1CB5\uA8EC\u0331\u1CB6\uA8F1\u032B\uA8EF\uA8E3\uA8E1\u0308\u030D\u0942\u0951\u0952\u0953\u0954]')
    without_svara = pattern.sub('', with_svara)

    return without_svara


def remove_svara(text):
    """ Removes svaras
    """

    # Both remove_svara_iter and remove_svara_regexp functions work well
    # but we are using remove_svara_regexp
    
    return remove_svara_regexp(text)


def replace_others(input_string):
    """ Replaces special texts
    """
    
    text = input_string
    
    text = text.replace(":", "ः")
    text = text.replace("ळ्", "ड्")
    text = text.replace("ळ", "ड")
    text = text.replace("ॐ", "ओम्")
#    text = text.replace("़", "")
    
    patterns = [
        re.compile(r'[0-9,.०१२३४५६७८९]'),
        re.compile(r'[(\[]'),
        re.compile(r'[)\]]')
    ]
    
    for pt in patterns:
        text = pt.sub('', text)
        
    return text


file_ = open(in_, 'r', encoding="utf-8")
all_text = file_.read()
file_.close()

all_lines = list(filter(None, all_text.split("\n")))
# new_list = []

iti_entries_dict = iti.get_iti_strings()

modified_list = []
segmented_list = []
sandhied_list = []
hyphenated_list = []

print("Cleaning terms...")
for i in tqdm(range(len(all_lines))):
    line = all_lines[i]
    new_text = remove_svara(line)
    new_text = remove_non_unicode(new_text)
    new_text = check_chandrabindu(new_text)
    new_text = replace_others(new_text)
    new_text = replace_avagraha(new_text)

    # Insert sandhi module
    
    cleaned_term = new_text
    segmented_term, sandhied_term, hyphenated_term = iti.replace_iti(
        new_text, iti_entries_dict
    )
    
    # Instead of saving all forms, only the sandhied and hyphenated are stored
    # new_list.append((line, cleaned_term, sandhied_term, hyphenated_term))
    modified_list.append(cleaned_term)
    segmented_list.append(segmented_term)
    sandhied_list.append(sandhied_term)
    hyphenated_list.append(hyphenated_term)

# updated_list = ["\t".join(item) for item in new_list]

file_ = open(out_mo, 'w', encoding="utf-8")
file_.write("\n".join(modified_list))
file_.close()

file_ = open(out_se, 'w', encoding="utf-8")
file_.write("\n".join(segmented_list))
file_.close()

file_ = open(out_sa, 'w', encoding="utf-8")
file_.write("\n".join(sandhied_list))
file_.close()

file_ = open(out_hy, 'w', encoding="utf-8")
file_.write("\n".join(hyphenated_list))
file_.close()
