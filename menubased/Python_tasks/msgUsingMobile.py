# msgUsingMobile.py
from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# Replace these with your Twilio account details
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.json
    to_number = data['to_number']
    message_body = data['message_body']

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return jsonify({'status': 'success', 'message': 'SMS sent successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
