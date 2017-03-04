from flask import render_template, request, send_from_directory, jsonify
from config import app


import requests
import json
import os

#===================================
# Routes ####
#===================================

@app.route('/')
def home():
    get_weather_report("fzabala@uci.edu")
    return render_template('index.html')


def get_weather_report(subject_id):
    send_url = 'http://sensoria.ics.uci.edu:8001/semanticobservation/get?requestor_id=hhrhee@uci.edu&service_id=1&subject_id=%s&type=presence&limit=100' % (subject_id)
    r = requests.get(send_url)
    j = json.loads(r.text)

    print(j)

    return j

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)