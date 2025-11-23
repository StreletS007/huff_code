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

# ---------------------------------------
# SELECT AVAILABILITY PAGE (new UI)
# ---------------------------------------

@app.route("/select_availability", methods=["GET"])
def show_select_availability():
    return render_template("select_availability.html")


@app.route("/reschedule", methods=["POST"])
def save_reschedule():
    new_slots = request.form.get("new_slots")
    print("Candidate submitted new slots:", new_slots)
    return "Thanks! Your new availability has been submitted."


# ---------------------------------------
# SEND BOOKING EMAIL
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
# SEND “NO SLOT FOUND” EMAIL
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

Once you submit new timings, matching will be attempted again.

Thanks,
HR Team
"""

    code, resp = send_sendgrid_email(candidate_email, subject, body)

    if code == 202:
        return jsonify({"status": "email_sent"}), 200
    else:
        return jsonify({"status": "error", "details": resp}), 500


# ---------------------------------------
# HR ESCALATION EMAIL (Step D)
# ---------------------------------------

@app.route("/sendHREscalation", methods=["POST"])
def send_hr_escalation():
    data = request.json
    candidate_email = data.get("candidate_email")
    new_slots = data.get("new_slots")

    subject = "Escalation: No Interview Slot Found"
    body = f"""
Hello HR Team,

This is an automated escalation.

Candidate: {candidate_email}
Updated Availability: {new_slots}

We attempted LLM-driven matching and no suitable interviewer slot was found.

ACTION REQUIRED:
• Review interviewer availability
• Add new time slots
• Adjust staffing if needed

Regards,
Auto Scheduler System
"""

    # HR mailbox here
    HR_EMAIL = "aseriousglass@gmail.com"

    code, resp = send_sendgrid_email(HR_EMAIL, subject, body)

    if code == 202:
        return jsonify({"status": "hr_notified"}), 200
    else:
        return jsonify({"status": "error", "details": resp}), 500


# ---------------------------------------
# UPDATED AVAILABILITY (Step C)
# ---------------------------------------

updated_availability = {}
# Example:
# { "candidate@example.com": "2025-12-01T09:00Z/2025-12-01T10:00Z" }


@app.route("/api/save_updated_availability", methods=["POST"])
def save_updated_availability():
    data = request.json
    candidate_email = data.get("candidate_email")
    new_slots = data.get("new_slots")

    if not candidate_email or not new_slots:
        return jsonify({"error": "Missing fields"}), 400

    updated_availability[candidate_email] = new_slots
    print("Saved updated availability:", updated_availability)

    return jsonify({"status": "saved"}), 200


@app.route("/api/get_updated_availability", methods=["GET"])
def get_updated_availability():
    return jsonify(updated_availability), 200


@app.route("/api/clear_availability/<email>", methods=["POST"])
def clear_availability(email):
    if email in updated_availability:
        del updated_availability[email]
        return jsonify({"status": "cleared"}), 200

    return jsonify({"status": "not_found"}), 404


# ---------------------------------------
# HOME PAGE
# ---------------------------------------

@app.route("/", methods=["GET"])
def home():
    return "Backend is running", 200


# ---------------------------------------
# RUN LOCALLY ONLY
# ---------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
