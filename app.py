from flask import Flask, request, Response
import logging
from flask_socketio import SocketIO

import json

from vedic_morph_analyser_sh.wsmp_sh import run_sh_text, cgi_file
from sh_to_term_json.generate_wsmp_results import generate_results
from cleaning import clean_all

# Replace the path with the SKT path
cgi_file = "/usr/lib/cgi-bin/SKT/sktgraph2"

app = Flask(__name__)
socketio = SocketIO(app)

status_messages = {
    200 : "success", # SH is able to segment either fully or partially
    504: "timeout", # SH time out (temporarily 30s)
    400: "error", # Input Error
    500: "failed", # Unknown Anomaly
    503: "unrecognized", # SH cannot recognize or segment it
}

status_codes = {
    "success": 200, # SH is able to segment either fully or partially
    "timeout": 504, # SH time out (temporarily 30s)
    "error": 400, # Input Error
    "failed": 500, # Unknown Anomaly
    "unrecognized": 503, # SH cannot recognize or segment it
}

status_messages = {
    "success": "SH is able to segment either fully or partially",
    "timeout": "SH time out (temporarily 30s)",
    "error": "Input Error",
    "failed": "Unknown Anomaly",
    "unrecognized": "SH cannot recognize or segment it",
}


def wsmp_sh_res(mantra_id, mantra_text):
    """ """
    
    if not mantra_id or not mantra_text:
        response_json = {"error": "Missing input_id or input_text"}
        status_code = 400
        return response_json, status_code
    
    try:
        cleaned_mantra = clean_all(mantra_text)
        
        sent_analysis = run_sh_text(cgi_file, cleaned_mantra, "DN", lex="MW", 
            us="f", output_encoding="deva", segmentation_mode="s", 
            text_type="t", stemmer="t")
        
        status = sent_analysis.get("status", "")
        error = sent_analysis.get("error", "")
        if status == "success":
            sent_analysis_str = json.dumps(sent_analysis, ensure_ascii=False)
            response_json, _ = generate_results(mantra_id, cleaned_mantra, sent_analysis_str, "sent")
            status_code = 200
        else:
            response_json = {status : error}
            status_code = status_codes.get(status, 500)
            
    except Exception as e:
        response_json = {"failed": str(e)}
        status_code = 500
    
    return response_json, status_code
        

@app.route('/sh-wsmp', methods=['GET'])
def wsmp_sh_res_get():
    """ """
    
    mantra_id = request.args.get('mantra_index')
    mantra_text = request.args.get('mantra')
    
    response_json, status_code = wsmp_sh_res(mantra_id, mantra_text)
    
    response_json_str = json.dumps(response_json, ensure_ascii=False)
    
    return Response(
        response=response_json_str,
        status=status_code,
        mimetype='application/json'
    )


@app.route('/sh-wsmp', methods=['POST'])
def wsmp_sh_res_post():
    """ """
    
    data = request.get_json()
    
    mantra_id = data.get('mantra_index')
    mantra_text = data.get('mantra')
    
    response_json, status_code = wsmp_sh_res(mantra_id, mantra_text)
    
    response_json_str = json.dumps(response_json, ensure_ascii=False)
    
    return Response(
        response=response_json_str,
        status=status_code,
        mimetype='application/json'
    )
    

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)

