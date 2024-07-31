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

@app.route('/sh-wsmp', methods=['GET'])
def wsmp_sh_res():
    mantra_id = request.args.get('mantra_index')
    mantra_text = request.args.get('mantra')
    
    if not mantra_id or not mantra_text:
#        return jsonify({"error": "Missing input_id or input_text"}), 400
        response_json = {"error": "Missing input_id or input_text"}
        response_json_str = json.dumps(response_json, ensure_ascii=False)
        return Response(
            response=response_json_str,
            status=400,
            mimetype='application/json'
        )
    
    try:
        cleaned_mantra = clean_all(mantra_text)
        
        sent_analysis = run_sh_text(cgi_file, cleaned_mantra, "DN", lex="MW", 
            us="f", output_encoding="deva", segmentation_mode="s", 
            text_type="t", stemmer="t")
        
        if sent_analysis["status"] == "success":
            sent_analysis_str = json.dumps(sent_analysis, ensure_ascii=False)
            sent_analysis_json, status = generate_results(mantra_id, cleaned_mantra, sent_analysis_str, "sent")
            status_code = 200
        else:
            sent_analysis_json = {}
            status_code = 504
        
        response_json = json.dumps(sent_analysis_json, ensure_ascii=False)
        
        return Response(
            response=response_json,
            status=status_code,
            mimetype='application/json'
        )
    
    except Exception as e:
#        return jsonify({"error": str(e)}), 500
        response_json = {"error": str(e)}
        response_json_str = json.dumps(response_json, ensure_ascii=False)
        return Response(
            response=response_json,
            status=500,
            mimetype='application/json'
        )
        

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)

