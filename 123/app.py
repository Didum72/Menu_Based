from flask import Flask, request, jsonify
import smtplib

app = Flask(__name__)

def send_email(subject, body, to_email):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        from_email = "janvisharma4102003@gmail.com"
        password = "janvi_2003"
        message = f'Subject: {subject}\n\n{body}'

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, message)
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {e}"

@app.route('/send_email', methods=['POST'])
def api_send_email():
    data = request.json
    subject = data.get('subject')
    body = data.get('body')
    to_email = data.get('to_email')

    result = send_email(subject, body, to_email)
    if "successfully" in result:
        return jsonify({"status": "success", "message": result}), 200
    else:
        return jsonify({"status": "error", "message": result}), 500

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
