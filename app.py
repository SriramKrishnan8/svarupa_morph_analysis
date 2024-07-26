from flask import Flask, request, Response
import logging

import json

#sys.path.append("./vedic_morph_analyser_sh")
#sys.path.append("./sh_to_term_json")

from vedic_morph_analyser_sh.wsmp_sh import run_sh_text, cgi_file
from sh_to_term_json.generate_wsmp_results import generate_results

# Replace the path with the SKT path
cgi_file = "/usr/lib/cgi-bin/SKT_Experimental/sktgraph2"

app = Flask(__name__)

@app.route('/sh-wsmp', methods=['GET'])
def wsmp_sh_res():
    mantra_id = request.args.get('mantra_index')
    mantra_text = request.args.get('mantra')
    
    if not mantra_id or not mantra_text:
        return jsonify({"error": "Missing input_id or input_text"}), 400
    
    try:
        sent_analysis = run_sh_text(cgi_file, mantra_text, "DN", lex="MW", 
            us="f", output_encoding="deva", segmentation_mode="s", 
            text_type="t", stemmer="t")
        
        sent_analysis_str = json.dumps(sent_analysis, ensure_ascii=False)
        
        sent_analysis_json, status = generate_results(mantra_id, mantra_text, sent_analysis_str, "sent")
        
        response_json = json.dumps(sent_analysis_json, ensure_ascii=False)
        
        return Response(
            response=response_json,
            status=200,
            mimetype='application/json'
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

