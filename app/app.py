from flask_cors import CORS
from flask import Flask, request, jsonify

import os
import secrets
from typing import Dict
from brf_engine import BRFNameFinder

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  
CORS(app) # This will enable CORS for all routes

brf_search_engine = BRFNameFinder(save_path='cache.json', load_cache=True)
        
def has_all_required_fields(data_object:Dict[str, any], fields:list[str]) -> bool:
    return data_object and all(key in data_object for key in fields)

@app.route('/get_brf')
def get_brf():
    if request.args.get('address') == None:
        return jsonify({'error': 'Invalid request, must provide address'}), 400

    address = request.args.get('address')
    print(address)

    response = brf_search_engine.find_brf(address)
    if response == None or response['items'] == []:
        response = jsonify({ "items": [ {"name": "Unable to find anything here"} ] })
    print(response)

    return response

@app.route('/start_new_session')
def start_new_session(): 
    brf_search_engine.start_new_session()
    return jsonify({"message": "started new session"}), 200

@app.route('/change_user_agent')
def change_user_agent():
    brf_search_engine.change_user_agent()
    return jsonify({"message": "changed user agent"}), 200

if __name__ == "__main__":
    if os.environ['FLASK_ENV'] == 'production':
        app.run(app)
    else:
        app.run(app, debug=True)