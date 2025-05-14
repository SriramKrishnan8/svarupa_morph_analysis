import re

import devtrans as dt

from scl_sandhi_interface import sandhi_words as sw

patterns_dict = {
    #" iwi$"
    r'^(.*?) iwi$': r'\1',
    
    #" iwi " -> 1106
    r'^(.*?)a iwi (.*?)e$': r'\1e iwi \2e', # (219)
    r'^(.*?)A iwi (.*?)E$': r'\1E iwi \2E', # (42)
    r'^(.*?)a iwi (.*?)aH$': r'\1aH iwi \2aH', # (602)
    r'^(.*?)A iwi (.*?)AH$': r'\1AH iwi \2AH', # (187)
    r'^(.*?)I iwi (.*?)I$': r'\1I iwi \2I', # (33)
    r'^(.*?)U iwi (.*?)U$': r'\1U iwi \2U', # (10)
    r'^(.*?)e iwi (.*?)e$': r'\1e iwi \2e', # (39)
    r'^(.*?)o iwi (.*?)o$': r'\1o iwi \2o', # (7)

    #[-grmndxvbf]iwi -> 1221
    r'^(.*?)-iwi (.*?)$': r'\1-iwi \2', # (26)
    r'^(.*?)xiwi (.*?)w$': r'\1w iwi \2w', # (128)
    r'^(.*?)diwi (.*?)t$': r'\1t iwi \2t', # (9)
    r'^(.*?)miwi (.*?)m$': r'\1m iwi \2m', # (540)
    r'^(.*?)riwi (.*?)H$': r'\1H iwi \2H', # (336)
    r'^(.*?)aviwi (.*?)o$': r'\1o iwi \2o', # (3)
    r'^(.*?)Aviwi (.*?)O$': r'\1O iwi \2O', # (38)
    r'^(.*?)Bviwi (.*?)u$': r'\1Bu iwi \2u', # (2)
    r'^(.*?)rviwi (.*?)u$': r'\1ru iwi \2u', # (2)
    r'^(.*?)Rviwi (.*?)u$': r'\1Ru iwi \2u', # (12)
    r'^(.*?)sviwi (.*?)u$': r'\1su iwi \2u', # (16)
    r'^(.*?)nniwi (.*?)n$': r'\1n iwi \2n', # (60)
    r'^(.*?)niwi (.*?)n$': r'\1n iwi \2n', # (49)
    r'^(.*?)giwi (.*?)k$': r'\1k iwi \2k', # (10)

    # iwy -> 397
    r'^(.*?)a iwy(.*)aH$': r'\1aH iwi \2aH', # (223)
    r'^(.*?)a iwy(.*)e$': r'\1e iwi \2e', # (73)
    r'^(.*?)A iwy(.*)AH$': r'\1AH iwi \2AH', # (56)
    r'^(.*?)e iwy(.*)e$': r'\1e iwi \2e', # (12)
    r'^(.*?)I iwy(.*)I$': r'\1I iwi \2I', # (8)
    r'^(.*?)A iwy(.*)E$': r'\1E iwi \2E', # (22)
    r'^(.*?)o iwy(.*)o$': r'\1o iwi \2o', #
    r'^(.*?)o iwy(.*)U$': r'\1U iwi \2U', #

    #iwI
    r'^(i.*?[^-])riwI(.*?H)$': r'\1H iwi i\2',
    r'^(I.*?[^-])riwI(.*?H)$': r'\1H iwi I\2',
    
    #[m]iwI
    r'^([^-]+)miwI(.*?m)$': r'\1m iwi I\2',
    
    #[mrnxv]iwy -> 474
    r'^(.*?[^-])miwy(.*?)m$': r'\1m iwi \2m', # (226)
    r'^(.*?[^-])riwy(.*?[aAiIuUeEoO])H$': r'\1H iwi \2H', # (84)
    r'^(.*?[^-])nniwy(.*?)nn$': r'\1n iwi \2n', # (35)
    r'^(.*?[^-])niwy(.*?)n$': r'\1n iwi \2n', # (11)
    r'^(.*?[^-])xiwy(.*?)w$': r'\1w iwi \2w', # (57)
    r'^(.*?[^-])viwy(.*?)u$': r'\1u iwi \2u', # (11)
    r'^(.*?[^-])Aviwy(.*?)O$': r'\1O iwi \2O', # (15)
    r'^(.*?[^-])biwy(.*?)p$': r'\1p iwi \2p', # (2)
    r'^(.*?[^-])giwy(.*?)k$': r'\1k iwi \2k', # (2)
    r'^(.*?[^-])diwy(.*?)t$': r'\1t iwi \2t', # (1)

    #ewi -> 536
    r'^(.*?)ewi (.*?)A$': r'\1A iwi \2A', # (160)
    r'^(.*?)ewi (.*?)a$': r'\1a iwi \2a', # (376)
    
    #ewy
    r'^([^-]+)ewy([^-]+-[^-]+)A$': r'\1A iwi \2A',
    r'^([^-]+)ewy([^-]+-[^-]+)a$': r'\1a iwi \2a',

    #Iwy -> 137
    r'^([^ ]*?)Iwy([^ ]*?)i$': r'\1i iwi \2i', # (124)
    r'^([^ ]*?)Iwy([^ ]*?)I$': r'\1I iwi \2I', # (13)

    #Iwi -> 236
    r'^(.*?)Iwi (.*?)i$': r'\1i iwi \2i', # (150)
    r'^(.*?)Iwi (.*?)I$': r'\1I iwi \2I', # (54)


    #iwI (to be done before all)
#    r'(.)(.*?)iwI(.*?[^;])$': r'\1\2iwi \1\3', # (20) Handled individually
    
    #ewI
    r'^(i[^-]+)ewI([^-]+-[^-]+)A$': r'\1A iwi i\2A',
    r'^(i[^-]+)ewI([^-]+-[^-]+)a$': r'\1a iwi i\2a',
    r'^(I[^-]+)ewI([^-]+-[^-]+)A$': r'\1A iwi I\2A',
    r'^(I[^-]+)ewI([^-]+-[^-]+)a$': r'\1a iwi I\2a',
    
    #-iwy
    r'^(.*?)a-iwy(.*?H)$': r'\1aH iwi \2', # 
    r'^(.*?)e-iwy(.*?e)$': r'\1e iwi \2', # 
}

def get_iti_strings():
    """ """

    iti_entries_file = open("itikarana_entries.tsv", "r", encoding="utf-8")
    iti_entries_contents = iti_entries_file.read()

    iti_entries_list = list(filter(None, iti_entries_contents.split("\n")))

    iti_entries_dict = {}
    
    for i_entry in iti_entries_list:
        split_ = i_entry.split("\t")
        key = split_[0]
        value = split_[1]
        iti_entries_dict[key] = value

    return iti_entries_dict


def check_iti_entries(input_string, iti_entries_dict):
    """ """

    found = False
    segmented_term = ""
    sandhied_term = ""
    hyphenated_term = ""
    if input_string in iti_entries_dict:
        found = True
        split_value = iti_entries_dict[input_string].split(",")
        if len(split_value) == 3:
            segmented_term = split_value[0]
            sandhied_term = split_value[1]
            hyphenated_term = split_value[2]
        else:
            segmented_term = split_value[0]
            sandhied_term = split_value[1]
    else:
        found = False
    
    return found, segmented_term, sandhied_term, hyphenated_term


def sandhi_items(term):
    """ """

    sub_terms = term.split("-")
    sandhied_term = ""
    for sb_trm in sub_terms:
        sandhied_term = sw.sandhi_join(sandhied_term, sb_trm, True)
    
    return sandhied_term


def replace_patterns(input_string, patterns_dict):
    """ """

    segmented_term = str(input_string)
    for pattern, replacement in patterns_dict.items():
        segmented_term = re.sub(pattern, replacement, segmented_term)

    segmented_term = dt.wx2dev(segmented_term)
    
    iwi_exception_condition = "इतिः" in segmented_term or "इतिम्" in segmented_term or "इतीम्" in segmented_term
    
    if "इति" in segmented_term and not iwi_exception_condition:
        split_terms = segmented_term.split("इति")
        sandhied_term = split_terms[0].strip()
        hyphenated_term = split_terms[1].strip()
    elif "iwi" in segmented_term:
        split_terms = segmented_term.split("iwi")
        sandhied_term = split_terms[0].strip()
        hyphenated_term = split_terms[1].strip()
    else:
        if "-" in segmented_term:
            sandhied_term = segmented_term.replace("-", "")
            # Temporarily not doing the sandhi, only concatenating it
            # Implement Sandhi module and then uncomment the below
            sandhied_term = sandhi_items(segmented_term)
            hyphenated_term = segmented_term
        else:
            sandhied_term = segmented_term
            hyphenated_term = segmented_term
    
    return segmented_term, sandhied_term, hyphenated_term


def replace_iti(input_string, iti_entries_dict):
    """ """

    found, segmented_term, sandhied_term, hyphenated_term = check_iti_entries(
        input_string, iti_entries_dict
    )
    
    if not found:
        wx_string = dt.dev2wx(input_string)
        segmented_term, sandhied_term, hyphenated_term = replace_patterns(
            wx_string, patterns_dict
        )
    
    # The following conditions are temporarily added to make sure that 
    # none of these are terms are returned empty
#    if sandhied_term == "" and "-" in segmented_term:
#        sandhied_term = segmented_term.replace("-", "")
#    elif "-" in sandhied_term:
#        sandhied_term.replace("-", "")
    if sandhied_term == "":
        if hyphenated_term == "":
            hyphenated_term = segmented_term
        sandhied_term = segmented_term.replace("-", "")
    elif hyphenated_term == "":
        hyphenated_term = sandhied_term
            
    return segmented_term, sandhied_term, hyphenated_term
