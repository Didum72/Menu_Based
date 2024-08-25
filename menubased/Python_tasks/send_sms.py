from flask import Flask, render_template, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials (Replace with your actual Twilio SID and Auth Token)
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'

client = Client(account_sid, auth_token)

def send_sms(sender_phone, receiver_phone, message):
    try:
        message = client.messages.create(
            body=message,
            from_=sender_phone,
            to=receiver_phone
        )
        return "SMS sent successfully!"
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('sendSMS.html')  # This renders the sendSMS.html file

@app.route('/send_sms', methods=['POST'])
def handle_send_sms():
    data = request.json
    sender_phone = data.get('sender_phone')
    receiver_phone = data.get('receiver_phone')
    message = data.get('message')
    
    result = send_sms(sender_phone, receiver_phone, message)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
