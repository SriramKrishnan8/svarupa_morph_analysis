from flask import Flask, request, Response, jsonify, make_response
from flask_socketio import SocketIO
import json

from vedic_morph_analyser_sh.wsmp_sh import run_sh_text, run_sh_morph_analysis
from sh_to_term_json.generate_wsmp_results import generate_results, generate_word_results
from cleaning import clean_all
from handle_iti import replace_iti, get_iti_strings

from scl_sandhi_interface.transliteration import *
from scl_sandhi_interface.sandhi_words import sandhi_join

from byt5_analyzer.byt5_analyzer import Byt5Analyzer
from byt5_analyzer.cli import run_byt5_text

app = Flask(__name__)
socketio = SocketIO(app)

print("Loading ByT5 Model (this will take a moment)...")
byt5_engine = Byt5Analyzer()
print("ByT5 Model loaded successfully.")

status_codes = {
    "success": 200,          # SH is able to segment either fully or partially
    "timeout": 504,          # SH timeout (temporarily 30s)
    "error": 400,            # Input Error
    "failed": 500,           # Unknown Anomaly
    "unrecognized": 503,     # SH cannot recognize or segment
}

status_messages = {
    "success": "SH is able to segment either fully or partially",
    "timeout": "SH timeout (temporarily 30s)",
    "error": "Input Error",
    "failed": "Unknown Anomaly",
    "unrecognized": "SH cannot recognize or segment it",
}


# ---------- Helper ----------
def make_json_response(response_json, status_code):
    """
    Create a Flask Response with UTF-8 JSON (ensure_ascii=False).
    """
    
    return Response(
        response=json.dumps(response_json, ensure_ascii=False),
        status=status_code,
        mimetype='application/json'
    )


# ---------- Core Functions ----------
def wsmp_sh_res(mantra_id, mantra_text):
    """ Get word segmentation and morphological analysis of a sentence """
    
    if not mantra_id or not mantra_text:
        response_json = {
            "status": "error",
            "error": "Missing input_id or input_text"
        }
        return response_json, status_codes.get("error")
    
    try:
        cleaned_mantra = clean_all(mantra_text)
        
        sent_analysis = run_sh_text(
            cleaned_mantra, "DN", lex="MW", 
            us="f", output_encoding="deva", segmentation_mode="s", 
            text_type="t", stemmer="t"
        )
        
        status = sent_analysis.get("status", "")
        error = sent_analysis.get("error", "")

        if status == "success":
            sent_analysis_str = json.dumps(sent_analysis, ensure_ascii=False)
            response_json, _ = generate_results(mantra_id, cleaned_mantra, sent_analysis_str, "sent")
            status_code = status_codes.get("success")
        else:
            response_json = {
                "status": status,
                "error" : error
            }
            status_code = status_codes.get(status, status_codes.get("failed"))
            
    except Exception as e:
        response_json = {
            "status": "failed",
            "error": str(e)
        }
        status_code = status_codes.get("failed")
    
    return response_json, status_code
        


def mp_sh_res(term_index, term_text):
    """ Get possible morphological analyses of the given word """
    
    response_json = {
        "term_index": term_index,
        "term_text": term_text,
    }

    if not term_index or not term_text:
        response_json.update({
            "status" : "error",
            "error": "Missing input_id or input_text",
        })
        status_code = status_codes.get("error")    
        return response_json, status_code
    
    try:
        cleaned_text = clean_all(term_text)
        iti_entries_dict = get_iti_strings()
        segmented_term, sandhied_term, hyphenated_term = replace_iti(cleaned_text, iti_entries_dict)
        
        morph_analysis_sa = run_sh_morph_analysis(
            sandhied_term, "DN", lex="MW", 
            us="f", output_encoding="deva", segmentation_mode="b", 
            text_type="f", stemmer="t"
        )
            
        morph_analysis_hy = run_sh_morph_analysis(
            hyphenated_term, "DN", lex="MW", 
            us="f", output_encoding="deva", segmentation_mode="b", 
            text_type="f", stemmer="t"
        )
        
        status = ""
        error = ""
        if morph_analysis_sa.get("status", "") == "success":
            status = "success"
            error = morph_analysis_sa.get("error", "")
            morph_analysis = morph_analysis_sa
        elif morph_analysis_hy.get("status", "") == "success":
            status = "success"
            error = morph_analysis_hy.get("error", "")
            morph_analysis = morph_analysis_hy
        else:
            status = morph_analysis_sa.get("status", "failure")
            error = morph_analysis_sa.get("error", "unknown error")
            morph_analysis = morph_analysis_sa
        
        if status == "success":
            morph_analysis_str = json.dumps(morph_analysis, ensure_ascii=False)
            morph_analysis_obj = generate_word_results(term_index, cleaned_text, morph_analysis_str, "word")
            response_json.update({
                "status" : "success",
                "term_json_new": morph_analysis_obj,
            })
            status_code = status_codes.get("success")
        else:
            response_json.update({
                "status" : "failed",
                "error" : error,
                "term_json_new": [],
            })
            status_code = status_codes.get(status, status_codes.get("failed"))
            
    except Exception as e:
        response_json.update({
            "status" : "failed",
            "error": str(e),
            "term_json_new": [],
        })
        status_code = status_codes.get("failed")
    
    return response_json, status_code


def word_segmentation(input_text, mode, text_type):
    """ 
    Segment a Sanskrit text using SH segmenter with configurable mode and type

    Args:
        input_text (str): Input Sanskrit text.
        mode (str): Segmentation mode, either "s" (single) or "l" (list).
        text_type (str): Input text type, either sentence "s" or word "w".

    Returns:
        tuple: (response_json, status_code)
    
    """
    
    if not input_text:
        return {
            "status" : "failure",
            "error": "Missing input_text"
        }, status_codes.get("error")
    
    try:
        cleaned_text = clean_all(input_text)
        seg_mode = "s" if mode not in {"s", "l"} else mode
        seg_text_type = "f" if text_type == "w" else "t"
        
        sent_analysis = run_sh_text(
            cleaned_text, 
            "DN", 
            lex="MW", 
            us="f", 
            output_encoding="deva", 
            segmentation_mode=seg_mode, 
            text_type=seg_text_type,  # "t" for sent, "f" for word
            stemmer="t"
        )
        
        status = sent_analysis.get("status", "")
        error = sent_analysis.get("error", "")
        segmentation = sent_analysis.get("segmentation", [])

        if status == "success":
            if not segmentation:
                return {
                    "status": "failure",
                    "error": "No segmentation"
                }, status_codes.get("failed")
            
            # single segmentation mode: only first valid result
            if seg_mode == "s" and "error" not in segmentation[0]:
                return {
                    "status": "success",
                    "segmentation": segmentation[:1]
                }, status_codes.get("success")
            
            # list segmentation mode: return full result
            if seg_mode == "l":
                return {
                    "status": "success",
                    "segmentation": segmentation
                }, status_codes.get("success")
            
            # segmentation failure
            return {
                "status": "failure",
                "error": segmentation[0]
            }, status_codes.get("failed")
        
        # general failure
        return {
            "status": "failure",
            "error": f"{status} - {error}"
        }, status_codes.get(status, status_codes.get("failed"))
    
    except Exception as e:
        return {"status": "failure", "error": str(e)}, status_codes.get("failed")
    

def scl_word_sandhi(first, second, sandhi_type):
    """ """

    internal = True if sandhi_type == "i" else False
    
    try:
        first_word = input_transliteration(first.strip(), "DN")[0]
        second_word = input_transliteration(second.strip(), "DN")[0]
        
        sandhied_word = sandhi_join(first_word, second_word, internal)
        
        sandhi_word_out = output_transliteration(sandhied_word, "deva")[0]

        return {"status": "success", "result": sandhi_word_out}, status_codes.get("success")
    except Exception as e:
        return {"status": "failure", "error": str(e)}, status_codes.get("failed")
    

def scl_sandhi(input_text):
    """ """

    sentences = [s.strip() for s in input_text.split('.') if s.strip()]
    
    sandhied_sentences = []

    for sentence in sentences:
        words = sentence.split(" ")
        
        processed_words = []
        for word in words:
            if "-" in word:
                components = word.split("-")
                sandhied_cpd_word = components[0]
                for i in range(1, len(components)):
                    sandhied_cpd_word = sandhi_join(sandhied_cpd_word, components[i], internal=True)
                
                processed_words.append(sandhied_cpd_word)
            else:
                processed_words.append(word)
        
        if not processed_words:
            continue

        final_sentence = processed_words[0]

        for i in range(1, len(processed_words)):
            first_word = final_sentence
            second_word = processed_words[i]

            final_sentence = sandhi_join(first_word, second_word, internal=False)
        
        sandhied_sentences.append(final_sentence)
    
    return " . ".join(sandhied_sentences) + (" ." if sandhied_sentences else "")
    

def scl_sent_sandhi(input_text):
    """ """
    try:
        input_wx = input_transliteration(input_text, "DN")[0]
        
        sandhied_output = scl_sandhi(input_wx)

        sandhi_word_out = output_transliteration(sandhied_output, "deva")[0]

        return {"status": "success", "result": sandhi_word_out}, status_codes.get("success")
    except Exception as e:
        return {"status": "failure", "error": str(e)}, status_codes.get("failed")


def byt5_wsmp_res(mantra_id, mantra_text):
    """ Get ByT5 segmentation and morphological analysis """
    if not mantra_id or not mantra_text:
        return {"status": "error", "error": "Missing input_id or input_text"}, status_codes.get("error")
    
    try:
        cleaned_mantra = clean_all(mantra_text)
        res = run_byt5_text(byt5_engine, cleaned_mantra, "DN", "deva", "wsmp")
        
        if res.get("status") == "success":
            res["mantra_index"] = mantra_id
            return res, status_codes.get("success")
            
        return {"status": "failed", "error": res.get("error", "Unknown error")}, status_codes.get("failed")
    except Exception as e:
        return {"status": "failed", "error": str(e)}, status_codes.get("failed")

def byt5_mp_res(term_index, term_text):
    """ Get ByT5 morphological analysis for a single term """
    if not term_index or not term_text:
        return {"status": "error", "error": "Missing term_index or term_text"}, status_codes.get("error")
    
    try:
        cleaned_text = clean_all(term_text)
        res = run_byt5_text(byt5_engine, cleaned_text, "DN", "deva", "mp")
        
        if res.get("status") == "success":
            res["term_index"] = term_index
            return res, status_codes.get("success")
            
        return {"status": "failed", "error": res.get("error", "Unknown error")}, status_codes.get("failed")
    except Exception as e:
        return {"status": "failed", "error": str(e)}, status_codes.get("failed")

def byt5_ws_res(input_text):
    """ Get ByT5 segmentation """
    if not input_text:
        return {"status": "error", "error": "Missing 'input_text'"}, status_codes.get("error")
    
    try:
        cleaned_text = clean_all(input_text)
        
        res = run_byt5_text(byt5_engine, cleaned_text, "DN", "deva", "ws")
        
        if res.get("status") == "success":
            return res, status_codes.get("success")
            
        return {"status": "failed", "error": res.get("error", "Unknown error")}, status_codes.get("failed")
    except Exception as e:
        return {"status": "failed", "error": str(e)}, status_codes.get("failed")


#-- App Routes --#


@app.route('/sh-wsmp', methods=['GET'])
def wsmp_sh_res_get():
    """ """
    
    mantra_id = request.args.get('mantra_index')
    mantra_text = request.args.get('mantra')

    return make_json_response(*wsmp_sh_res(mantra_id, mantra_text))


@app.route('/sh-wsmp', methods=['POST'])
def wsmp_sh_res_post():
    """ """
    
    data = request.get_json()
    
    mantra_id = data.get('mantra_index')
    mantra_text = data.get('mantra')

    return make_json_response(*wsmp_sh_res(mantra_id, mantra_text))
    
    
@app.route('/sh-mp', methods=['POST'])
def mp_sh_res_post():
    """ """
    
    data = request.get_json()
    
    term_index = data.get('term_index')
    term_text = data.get('term_text')

    return make_json_response(*mp_sh_res(term_index, term_text))


@app.route('/sh-ws', methods=['POST'])
def sh_segmentation():
    """
    API endpoint for Sanskrit Heritage word segmentation.

    Expects JSON payload:
    {
        "input": "<input text>",
        "mode": "s" | "l"   # optional, defaults to "s"
        "type": "s" | "w"   # compound segmentation - "w", defaults to "s"
    }
    """
    
    data = request.get_json(silent=True) or {}
    input_text = data.get('input', "")
    mode = data.get('mode', 's')
    text_type = data.get('type', 's')

    if not input_text:
        return make_response(
            jsonify({
                "status" : "error",
                "error": "Missing 'input_text'"
            }), status_codes.get("error")
        )
    
    return make_json_response(*word_segmentation(input_text, mode, text_type))


@app.route('/scl-word-sandhi', methods=['POST'])
def samsaadhanii_word_sandhi():
    """
    API endpoint for Samsaadhanii word sandhi.

    Expects JSON payload:
    {
        "first": "<first word>",
        "second": "<second word>"
        "type": "i" (internal) | "e" (external) # defaults to "e"
    }
    """
    
    data = request.get_json(silent=True) or {}
    first = data.get('first', '')
    second = data.get('second', '')
    sandhi_type = data.get('type', 'e')

    if not first and not second:
        return make_response(
            jsonify({
                "status" : "error",
                "error": "Missing 'first' and 'second' words"
            }), status_codes.get("error")
        )    
    
    return make_json_response(*scl_word_sandhi(first, second, sandhi_type))


@app.route('/scl-sent-sandhi', methods=['POST'])
def samsaadhanii_sent_sandhi():
    """
    API endpoint for Samsaadhanii sent sandhi.

    Expects JSON payload:
    {
        "input": "<input_text>",
    }
    """
    
    data = request.get_json(silent=True) or {}
    input_text = data.get('input', '')
    
    if not input_text:
        return make_response(
            jsonify({
                "status" : "error",
                "error": "Missing 'input_text'"
            }), status_codes.get("error")
        )    
    
    return make_json_response(*scl_sent_sandhi(input_text))


@app.route('/byt5-wsmp', methods=['GET', 'POST'])
def byt5_wsmp_route():
    """ """
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        mantra_id = data.get('mantra_index')
        mantra_text = data.get('mantra')
    else:
        mantra_id = request.args.get('mantra_index')
        mantra_text = request.args.get('mantra')

    return make_json_response(*byt5_wsmp_res(mantra_id, mantra_text))


@app.route('/byt5-mp', methods=['POST'])
def byt5_mp_route():
    """ """
    data = request.get_json(silent=True) or {}
    term_index = data.get('term_index')
    term_text = data.get('term_text')

    return make_json_response(*byt5_mp_res(term_index, term_text))


@app.route('/byt5-ws', methods=['POST'])
def byt5_ws_route():
    """ """
    data = request.get_json(silent=True) or {}
    input_text = data.get('input', "")

    return make_json_response(*byt5_ws_res(input_text))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

