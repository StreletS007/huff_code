from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

# ---------------------------------------
# SendGrid Email Helper
# ---------------------------------------

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")  # example: "hr@yourdomain.com"

def send_sendgrid_email(to_email, subject, body):
    """
    Sends an email using SendGrid API.
    """
    url = "https://api.sendgrid.com/v3/mail/send"

    data = {
        "personalizations": [{
            "to": [{"email": to_email}]
        }],
        "from": {"email": FROM_EMAIL},
        "subject": subject,
        "content": [
            {
                "type": "text/plain",
                "value": body
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)
    return response.status_code, response.text

# ---------------------------------------
# RESCHEDULE PAGE
# ---------------------------------------

@app.route("/reschedule", methods=["GET"])
def show_reschedule_page():
    return render_template("reschedule.html")


@app.route("/reschedule", methods=["POST"])
def save_reschedule():
    new_slots = request.form.get("new_slots")
    print("Candidate submitted new slots:", new_slots)

    # Later: Save to DB or forward to WatsonX
    return "Thanks! Your new availability has been submitted."

# ---------------------------------------
# SEND EMAIL — Normal Booking Email
# ---------------------------------------

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

If you need to reschedule, use the link below:
https://backend-email-7jn1.onrender.com/reschedule

Best regards,
HR Team
"""

    code, resp = send_sendgrid_email(candidate_email, subject, body)

    if code == 202:
        return jsonify({"status": "email_sent"}), 200
    else:
        return jsonify({"status": "error", "details": resp}), 500

# ---------------------------------------
# SEND EMAIL — No Slot Found Email
# ---------------------------------------

@app.route("/sendNoSlotEmail", methods=["POST"])
def send_no_slot_email():
    data = request.json
    candidate_name = data.get("candidate_name")
    candidate_email = data.get("candidate_email")

    subject = "Update Your Availability"
    body = f"""
Hi {candidate_name},

We could not find a matching interview slot based on your availability.

Please update your availability using the link below:
https://backend-email-7jn1.onrender.com/reschedule

Once you submit new timings, we will attempt matching again.

Thanks,
HR Team
"""

    code, resp = send_sendgrid_email(candidate_email, subject, body)

    if code == 202:
        return jsonify({"status": "email_sent"}), 200
    else:
        return jsonify({"status": "error", "details": resp}), 500

# ---------------------------------------
# HOME PAGE
# ---------------------------------------

@app.route("/", methods=["GET"])
def home():
    return "Backend is running", 200


# ---------------------------------------
# RUN LOCALLY
# ---------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
