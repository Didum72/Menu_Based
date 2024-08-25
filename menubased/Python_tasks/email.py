from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

def send_email(sender_email, password, receiver_email, subject, message):
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        
        # Attach the message
        msg.attach(MIMEText(message, 'plain'))
        
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login to the email server
        server.login(sender_email, password)
        
        # Send the email
        server.send_message(msg)
        server.quit()
        
        return "Email sent successfully!"
    
    except Exception as e:
        return str(e)

@app.route('/send_email', methods=['POST'])
def handle_send_email():
    data = request.json
    sender_email = data.get('sender_email')
    password = data.get('password')
    receiver_email = data.get('receiver_email')
    subject = data.get('subject')
    message = data.get('message')
    
    result = send_email(sender_email, password, receiver_email, subject, message)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
