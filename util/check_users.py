from pymongo import MongoClient
from twilio.rest import TwilioRestClient
import requests
import json

a = open("../dev_config.cfg")
config = {}

for line in a:
    z = line.split("=")
    if "\n" in z[1]:
        config[z[0]] = z[1][1:-2]
    else:
        config[z[0]] = z[1][1:-1]

mc = MongoClient(config["MONGODB_URI"])
db = mc.heroku_wcxhtdf7

client = TwilioRestClient(config['TWILIO_ACCOUNT_SID'], config['TWILIO_AUTH_TOKEN'])

def get_user_data(subject_id):
    send_url = 'http://sensoria.ics.uci.edu:8001/semanticobservation/get?requestor_id=hhrhee@uci.edu&service_id=1&subject_id=%s&type=presence&limit=100' % (subject_id)
    r = requests.get(send_url)
    j = json.loads(r.text)

    return j

def text(to, body):
    message = client.messages.create(to=to, from_=config['TWILIO_NUMBER'],
                                     body=body)

def check():
    users = db.users.find()

    for user in users:
        data = get_user_data(user['email'])
        print "Checking user %s..." % (user['name'])
        if data[0]['payload']['Location'] not in user['authorized'] and data[0]['timestamp'] != user['timestamp'] and not(user['root']):
            print "WARNING: User %s is in an UNAUTHORIZED area. Sending notifications to all available security."
            text("2012500807", "Security Alert: %s is not authorized to be in room %s." % (user['name'], data[0]['payload']['Location']))
            db.users.update({"_id" : user['_id']}, {"$set" : {"timestamp" : data[0]['timestamp']}})
        else:
            pass
import time
while True:
    check()
    time.sleep(5)
# text("2012500807", "")