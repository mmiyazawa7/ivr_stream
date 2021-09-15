
# coding: utf-8

# In[ ]:


from flask import Flask,request, Response,session
import requests
import json
import nexmo
import datetime
from base64 import urlsafe_b64encode
import os
import calendar
# from jose import jwt
import jwt # https://github.com/jpadilla/pyjwt -- pip3 install PyJWT
import coloredlogs, logging
from uuid import uuid4

# test

# for heroku, please put all env parameters to 'Config Vars` in heroku dashboard
# from dotenv import load_dotenv
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

api_key = os.environ.get("API_KEY") 
api_secret = os.environ.get("API_SECRET")
application_id = os.environ.get("APPLICATION_ID")

private_key = os.environ.get("PRIVATE_KEY")

# keyfile = "private.key"

url = "https://api.nexmo.com/v1/calls"

webhook_url = os.environ.get("WEBHOOK_URL")

web_port = os.environ.get("WEB_PORT")

virtual_number = os.environ.get("LVN")
admin_number = os.environ.get("ADMIN_NUMBER")

session={}
client_sms = nexmo.Client(key=api_key, secret=api_secret)


@app.route('/ivrstart',methods=['GET', 'POST'])
def japanivr():

    arg_to = request.args['to']
    arg_from = request.args['from']

    session['to'] = arg_to
    session['from'] = arg_from

    logger.debug('From: %s', arg_from)
    logger.debug('To: %s', arg_to)


    
    ncco=[{
	        "action": "stream",
	        "streamUrl": ["https://github.com/mmiyazawa7/streams/blob/master/0_message.mp3?raw=true"],
            "bargeIn": "true"
	      },
          {
            "action": "input",
            "timeOut": "30",
            "submitOnHash": "true",
            "eventUrl": [ webhook_url + "/dtmfresponse"]
            }]
    js=json.dumps(ncco)
    resp=Response(js, status=200, mimetype='application/json')
    print(resp.data)
    return resp


@app.route('/dtmfresponse',methods=['GET', 'POST'])
def dtmfresponse():

    currentDT = datetime.datetime.now()
    date =currentDT.strftime("%Y-%m-%d %H:%M:%S")

    webhookContent = request.json
    print(webhookContent)
    try:
        result = webhookContent['dtmf']
    except:
        pass

    logger.debug("The User enter: " + str(result) + "\n")
    logger.debug(date)

    sms_text = "We received call from " + session['from'] + " on " + date
    response_SMS = client_sms.send_message({'from': 'NexmoJapan', 'to': admin_number, 'text': sms_text})
    logger.debug(response_SMS)
    logger.debug(sms_text)
    
    if result == '1':
        ncco = [
                {
                    "action": "stream",
                    "streamUrl": ["https://github.com/mmiyazawa7/streams/blob/master/1_message.mp3?raw=true"],
                },
                {
                    "action": "stream",
                    "streamUrl": ["https://github.com/mmiyazawa7/streams/blob/master/0_message.mp3?raw=true"],
                    "bargeIn": "true"
	           },
                {
                    "action": "input",
                    "timeOut": "30",
                    "submitOnHash": "true",
                    "eventUrl": [ webhook_url + "/dtmfresponse"]
                }
            ]
        js = json.dumps(ncco)
        resp = Response(js, status=200, mimetype='application/json')
        logger.debug('Response NCCO Menu_1 Stream')
        print(resp)
        return resp
    elif result == '2':
        ncco = [
                {
                    "action": "stream",
                    "streamUrl": ["https://github.com/mmiyazawa7/streams/blob/master/2_message.mp3?raw=true"],
                },
                {
                    "action": "stream",
                    "streamUrl": ["https://github.com/mmiyazawa7/streams/blob/master/0_message.mp3?raw=true"],
                    "bargeIn": "true"
                },
                {
                    "action": "input",
                    "timeOut": "30",
                    "submitOnHash": "true",
                    "eventUrl": [ webhook_url + "/dtmfresponse"]
                }
            ]
        js = json.dumps(ncco)
        resp = Response(js, status=200, mimetype='application/json')
        logger.debug('Response NCCO Menu_2 Stream')
        print(resp)
        return resp
    elif result == '3':
        ncco = [
                {
                    "action": "stream",
                    "streamUrl": ["https://github.com/mmiyazawa7/streams/blob/master/3_message.mp3?raw=true"],
                },
                {
                    "action": "stream",
                    "streamUrl": ["https://github.com/mmiyazawa7/streams/blob/master/0_message.mp3?raw=true"],
                    "bargeIn": "true"
                },
                {
                    "action": "input",
                    "timeOut": "30",
                    "submitOnHash": "true",
                    "eventUrl": [ webhook_url + "/dtmfresponse"]
                }
            ]
        js = json.dumps(ncco)
        resp = Response(js, status=200, mimetype='application/json')
        logger.debug('Response NCCO Menu_2 Stream')
        print(resp)
        return resp
    elif result == '4':
        ncco = [
                {
                    "action": "stream",
                    "streamUrl": ["https://github.com/mmiyazawa7/streams/blob/master/0_message.mp3?raw=true"],
                    "bargeIn": "true"
                },
                {
                    "action": "input",
                    "timeOut": "30",
                    "submitOnHash": "true",
                    "eventUrl": [ webhook_url + "/dtmfresponse"]
                }
            ]
        js = json.dumps(ncco)
        resp = Response(js, status=200, mimetype='application/json')
        logger.debug('Response NCCO Menu_2 Stream')
        print(resp)
        return resp
    else:
        ncco = [
                {
                    "action": "talk",
                    "text": "　入力が間違えています。電話を切るか、メニュー番号を押してください",
                    "voiceName": "Mizuki"
                },
                {
                    "action": "stream",
                    "streamUrl": ["https://github.com/mmiyazawa7/streams/blob/master/0_message.mp3?raw=true"],
                    "bargeIn": "true"
                },
                {
                    "action": "input",
                    "timeOut": "30",
                    "submitOnHash": "true",
                    "eventUrl": [ webhook_url + "/dtmfresponse"]
                }
            ]
        js = json.dumps(ncco)
        resp = Response(js, status=200, mimetype='application/json')
        logger.debug('Wrong Input.Try Again Message')
        print(resp)
        return resp
    return "success"

@app.route('/event', methods=['GET', 'POST', 'OPTIONS'])
def display():
    r = request.json
    print(r)
    return "OK"


if __name__ == '__main__':
    app.run(port=web_port)

