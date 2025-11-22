from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route("/sendEmail", methods=["POST"])
def send_email():
    data = request.json

    candidate_name = data.get("candidate_name")
    candidate_email = data.get("candidate_email")
    date = data.get("date")
    start = data.get("start")
    end = data.get("end")


    subject = "Your Interview Slot is Scheduled"
    body = f"""
Hi {candidate_name},

Your interview has been scheduled.

📅 Date: {date}
⏰ Time: {start} - {end}

If you need to reschedule, reply to this email.

Best regards,
HR Team
"""


    sender_email = "YOUR_EMAIL@gmail.com"
    sender_password = "YOUR_APP_PASSWORD"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = candidate_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))


    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, candidate_email, msg.as_string())
        server.quit()

        return jsonify({"status": "email_sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "Backend is running", 200

@app.route("/sendNoSlotEmail", methods=["POST"])
def send_no_slot_email():
    data = request.json
    candidate_name = data.get("candidate_name")
    candidate_email = data.get("candidate_email")

    subject = "Next Steps: Please Update Your Availability"

    body = f"""
Hi {candidate_name},

We could not find a matching interview slot based on the availability provided.

Please use the link below to choose new availability:
https://your-frontend-link.com/reschedule

Once you submit new timings, we will attempt to match with the HR/team again.

Thanks,
HR Team
"""

    # TODO: Implement your email sending logic here

    return jsonify({"status": "sent"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


