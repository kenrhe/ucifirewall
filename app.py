from flask import render_template, request, send_from_directory, jsonify
from config import app, db


import requests
import json
import os

#===================================
# Routes ####
#===================================

@app.route('/')
def home():
    # print str(db.users.find_one({"email" : "hhrhee@uci.edu"}))
    return render_template('index.html', analysis=analyze("hhrhee@uci.edu"))


def get_user_data(subject_id):
    send_url = 'http://sensoria.ics.uci.edu:8001/semanticobservation/get?requestor_id=hhrhee@uci.edu&service_id=1&subject_id=%s&type=presence&limit=100' % (subject_id)
    r = requests.get(send_url)
    j = json.loads(r.text)

    return j

def get_frequency(data, room):
    total = len(data)
    count = 0
    for p in data:
        print(p['payload']['Location'])
        print(room)
        if p['payload']['Location'] == room:
            count += 1
    percentage = float(count) / float(total) * 100.0
    return "%.2f" % (percentage)

def is_authorized(user, room):
    if user == None:
        return None

    if room in user['authorized']:
        return True
    
    return False

def analyze(subject_id):
    data = get_user_data(subject_id)
    finished = []

    user = db.users.find_one({"email" : subject_id})

    for p in data:
        clean = {}
        clean['room'] = p['payload']['Location']
        clean['timestamp'] = p['timestamp']
        clean['frequency'] = get_frequency(data, clean['room'])
        clean['authorized'] = is_authorized(user, clean['room'])
        finished.append(clean)

    # print(finished)
    return finished

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)