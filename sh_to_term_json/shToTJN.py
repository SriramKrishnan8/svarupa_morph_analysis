import json

pronoun_stems = [
    "त्वद्", "मद्", "अस्मद्", "युष्मद्", "तद्", "यद्", "एतद्", "किम्", "त्यद्", "इदम्", "अदस्", "एक", "द्वि", "भवतु",
    "सर्व", "विश्व", "उभ", "उभय", "डतर", "डतम", "अन्य", "अन्यतर", "इतर", "त्वत्", "त्व", "नेम", "सम","सिम",
    "पूर्व", "पर", "अवर", "दक्षिण", "उत्तर", "अपर", "अधर", "स्व", "अन्तर",
]

cardinal_stems = [
    "एक", "द्वि", "त्रि", "चतुर्", "पञ्चन्", "षष्", "सप्तन्", "अष्टन्", "नवन्", "दशन्",
    "एकादशन्", "द्वादशन्", "त्रयोदशन्", "चतुर्दशन्", "पञ्चदशन्", "षोडशन्", "सप्तदशन्", "अष्टदशन्", "नवदशन्",
    "विंशति", "त्रिंशत्", "चत्वारिंशत्", "पञ्चाशत्", "षष्टि", "सप्तति", "अशीति", "नवति", "शतम्",
]

def is_noun(inflectional_morph):
    """ Checks whether the given morph analysis corresponds to a noun or not """
    
    cases = [
        "nom.", "acc.", "i.", "dat.", "abl.", "gen.", "loc.", "voc.",
        "iic.", 
    ]
    
    return any([c in inflectional_morph for c in cases])    
    

class SHMorph:
    def __init__(self):
        self.input = ''
        self.status = ''
        self.segmentation = []
        self.morph = []
        self.source = ''

    def to_dict(self):
        return {
            "input": self.input,
            "status": self.status,
            "segmentation": [segment for segment in self.segmentation],
            "morph": [morph.to_dict() for morph in self.morph],
            "source": self.source
        }


class Segment:
    def __init__(self):
        self.name = ''
        self.morphList = []
        self.selected = False
        self.source = ''

    def to_dict(self):
        return {
            "name": self.name,
            "morphList": [morph.to_dict() for morph in self.morphList],
            "selected": self.selected,
            "source": self.source,
        }


class BaseWord:
    def __init__(self, morph):
        self.baseElement = morph.word
        self.stem = morph.stem
        self.grammar = ''
        self.dcsMeaningsStem = None
        self.ambudaMenaingsStem = None
        self.dcsMeaningsRoot = None
        self.ambudaMenaingsRoot = None
        self.grammarMap = None
        self.grammarMapEn = None
        self.grammarMapSa = None
        self.rootTermLink = None
        self.root = morph.root
        self.selected = False

    def to_dict(self):
        return {
            "baseElement": self.baseElement,
            "stem": self.stem,
            "grammar": self.grammar,
            "dcsMeaningsStem": self.dcsMeaningsStem,
            "ambudaMenaingsStem": self.ambudaMenaingsStem,
            "dcsMeaningsRoot": self.dcsMeaningsRoot,
            "ambudaMenaingsRoot": self.ambudaMenaingsRoot,
            "grammarMap": self.grammarMap,
            "grammarMapEn": self.grammarMapEn,
            "grammarMapSa": self.grammarMapSa,
            "rootTermLink": self.rootTermLink,
            "root": self.root,
            "selected": self.selected,
        }


class MorphDetail:
    def __init__(self):
        self.name = ''
        self.grammarList = []

    def to_dict(self):
        return {
            "name": self.name,
            "grammarList": [grammar.to_dict() for grammar in self.grammarList],
        }


class Morph:
    def __init__(self, word, stem, root, derivational_morph, inflectional_morphs):
        self.word = word
        self.stem = stem
        self.root = root
        self.derivational_morph = derivational_morph
        self.inflectional_morphs = inflectional_morphs

    def to_dict(self):
        return {
            "word": self.word,
            "stem": self.stem,
            "root": self.root,
            "derivational_morph": self.derivational_morph,
            "inflectional_morphs": self.inflectional_morphs,
        }


def convertToBaseList(morphList):
    baseList = []
    for morph in morphList:
        stem = morph.stem
        inflectionalMorphs = morph.inflectional_morphs
        derivationalMorph = morph.derivational_morph
        
        noun_type = ""
        if stem in pronoun_stems:
            noun_type = "dei."
        elif stem in cardinal_stems:
            noun_type = "car."
        else:
            pass

        for inflectionalMorph in inflectionalMorphs:
            base = BaseWord(morph)
            if not noun_type and is_noun(inflectionalMorph):
                noun_type = "nam."
            else:
                pass
            
            if noun_type:
                if "*" in inflectionalMorph:
                    inflectionalMorph = inflectionalMorph.replace("*", noun_type)
                else:
                    inflectionalMorph += " " + noun_type
            
            grmr_lst = [
                derivationalMorph, inflectionalMorph
            ]
            grmr = " ".join(list(filter(None,grmr_lst)))
#            inflectionalMorph = inflectionalMorph + " " + noun_type if noun_type else inflectionalMorph
#            grmr = (derivationalMorph + " " + inflectionalMorph) if derivationalMorph else inflectionalMorph
            base.grammar = grmr
            baseList.append(base)

#        if derivationalMorph:
#            derivationalBase = BaseWord(morph)
#            derivationalBase.grammar = derivationalMorph
#            baseList.append(derivationalBase)

    return baseList


def processWords(baseList, splitted, part):
    resultMap = MorphDetail()
    resultMap.name = splitted
    resultMap.grammarList = []

    # print(splitted, part)
    # print(resultMap.to_dict())

    for base in baseList:
        # print(base.to_dict())
        if base.grammar == "?" or base.grammar == "":
            continue
        if part == base.baseElement or (part + "-" == base.baseElement):
            resultMap.grammarList.append(base)

    return resultMap


def shToTerm(shJsonStr):
    if shJsonStr[0] == '[':
        shJsonStr_updated = shJsonStr[1:-1]
    shJsonStr_updated = shJsonStr
    shJsonDict = json.loads(shJsonStr_updated)
    
#    print(shJsonStr)
    
    # print(shJsonDict)
    shJson = SHMorph()
    shJson.input = shJsonDict.get('input', '')
    shJson.status = shJsonDict.get('status', '')
    shJson.segmentation = shJsonDict.get('segmentation', [])
    shJson.morph = []
    shJson.source = shJsonDict.get('source', '')

    # print(shJsonDict['morph'])
    
    for morph_data in shJsonDict.get('morph', []):
        morph = Morph(
            word=morph_data.get('word', ''),
            stem=morph_data.get('stem', ''),
            root=morph_data.get('root', ''),
            derivational_morph=morph_data.get('derivational_morph', ''),
            inflectional_morphs=morph_data.get('inflectional_morphs', [])
        )
        shJson.morph.append(morph)

    # print(shJson.to_dict())
    
    shJsonString = str(shJson.__dict__)
    shJsonString = shJsonString.replace("'", '"')

    # print("\nBefore: " + shJsonString)
    
    if '"segmentation":' in shJsonString:
        shJsonString = shJsonString.replace('"segmentation": "', '"segmentation": ["')
        shJsonString = shJsonString.replace('", "morph', '"], "morph')

    # print("After 1: " + shJsonString)
    
    if shJsonString.startswith("[") and shJsonString.endswith("]"):
        shJsonString = shJsonString[1:-1]
    
    # print("After 2: " + shJsonString)

    # print([x.to_dict() for x in shJson.morph])
    # print([x for x in shJson.segmentation])

    baseWordList = convertToBaseList(shJson.morph)

    # print([x.to_dict() for x in baseWordList])

    outerMap = []
    for s in shJson.segmentation:
        # print("\n" + s)
        s = s.replace("#", "")
        insideList = []
        spaceSeparated = s.split(" ")
        for splitted in spaceSeparated:
            if "-" in splitted:
                hyphenSeparated = []
                parts = splitted.split("-")
                for i in range(len(parts) - 1):
                    hyphenSeparated.append(parts[i] + "-")
                hyphenSeparated.append(parts[-1])
                for part in hyphenSeparated:
                    morphDetail = processWords(baseWordList, splitted, part)
                    insideList.append(morphDetail)
            else:
                morphDetail = processWords(baseWordList, splitted, splitted)
                # print(morphDetail.to_dict())
                insideList.append(morphDetail)

        segment = Segment()
        segment.morphList = insideList
        segment.name = s
        segment.source = shJson.source
        outerMap.append(segment)
    outer_map_dicts = [segment.to_dict() for segment in outerMap]
    termJsonNew = str(outer_map_dicts)
    termJsonNew = termJsonNew.replace("'", '"')
    termJsonNew = termJsonNew.replace('False', 'false')
    termJsonNew = termJsonNew.replace("None", "null")
    return termJsonNew, shJson.segmentation

#sh_json_string = """{"input": "ये", "status": "success", "segmentation": ["ये"], "source": "DCS", "morph": [{"word": "ये", "stem": "यद्", "root": "", "derivational_morph": "", "inflectional_morphs": ["m. pl. nom."]}, {"word": "ये", "stem": "यद्", "root": "", "derivational_morph": "", "inflectional_morphs": ["f. du. nom."]}, {"word": "ये", "stem": "यद्", "root": "", "derivational_morph": "", "inflectional_morphs": ["n. du. acc."]}, {"word": "ये", "stem": "यद्", "root": "", "derivational_morph": "", "inflectional_morphs": ["n. du. nom."]}]}"""
#term_json_new = shToTerm(sh_json_string)
#print(term_json_new)
