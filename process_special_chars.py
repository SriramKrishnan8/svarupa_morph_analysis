import os
import sys

import re

from tqdm import tqdm

import handle_iti as iti

script, in_, out_ = sys.argv


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
    

def remove_svara(text):
    """ Removes svaras
    """

    new_text = []
    for char in text:
        if '\u0951' <= char <= '\u0954':
            continue
        # To remove zero width joiner character
        elif char in ['\u200d', '\u200c', '\u1CD6', '\u1CD5', '\u1CE1']:
            continue
        new_text.append(char)
    
    modified_text = "".join(new_text)
    
    return modified_text


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
new_list = []

iti_entries_dict = iti.get_iti_strings()

print("Cleaning terms...")
for i in tqdm(range(len(all_lines))):
    line = all_lines[i]
    new_text = remove_svara(line)
    new_text = remove_non_unicode(new_text)
    new_text = check_chandrabindu(new_text)
    new_text = replace_others(new_text)
    
    cleaned_term = new_text
    segmented_term, sandhied_term, hyphenated_term = iti.replace_iti(
        new_text, iti_entries_dict
    )
    new_list.append((line, cleaned_term, sandhied_term, hyphenated_term))

updated_list = ["\t".join(item) for item in new_list]

file_ = open(out_, 'w', encoding="utf-8")
file_.write("\n".join(updated_list))
file_.close()
