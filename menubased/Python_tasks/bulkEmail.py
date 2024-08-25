# bulkEmail.py
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/send_emails', methods=['POST'])
def send_emails():
    data = request.json
    smtp_server = 'smtp.example.com'  # Change to your SMTP server
    smtp_port = 587  # Change to your SMTP server port
    smtp_user = 'your_email@example.com'  # Change to your email
    smtp_password = 'your_password'  # Change to your email password

    sender_email = smtp_user
    subject = data['subject']
    body = data['body']
    recipient_emails = data['emails']

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)

            for recipient_email in recipient_emails:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                server.sendmail(sender_email, recipient_email, msg.as_string())

        return jsonify({'status': 'success', 'message': 'Emails sent successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
