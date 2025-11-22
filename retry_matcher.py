import os
import json
import requests
from ibm_watsonx_ai import Credentials, WatsonxAI

BASE = "https://backend-email-7jn1.onrender.com"

# -----------------------------
# WatsonX Config
# -----------------------------
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_REGION = os.getenv("WATSONX_REGION")

creds = Credentials(
    api_key=WATSONX_API_KEY,
    service_url=f"https://api.{WATSONX_REGION}.ml.cloud.ibm.com"
)

llm = WatsonxAI(
    credentials=creds,
    project_id=WATSONX_PROJECT_ID,
    model_id="meta-llama/llama-3-8b-instruct",
    params={"decoding_method": "greedy"}
)

# -----------------------------
# API Helpers
# -----------------------------

def fetch_updated_availability():
    return requests.get(f"{BASE}/api/get_updated_availability").json()

def get_interviewers():
    return requests.get(f"{BASE}/api/get_interviewers").json()

def create_booking(match, candidate_email):
    payload = {
        "slot_start": match["slot_start"],
        "slot_end": match["slot_end"],
        "candidate_id": candidate_email,
        "interviewer_id": match["interviewer_id"]
    }
    return requests.post(f"{BASE}/create_booking", json=payload).json()

def send_email(candidate_email, match):
    payload = {
        "candidate_name": candidate_email.split("@")[0],
        "candidate_email": candidate_email,
        "date": match["slot_start"].split("T")[0],
        "start": match["slot_start"].split("T")[1],
        "end": match["slot_end"].split("T")[1],
    }
    return requests.post(f"{BASE}/sendEmail", json=payload).json()

def clear(candidate_email):
    requests.post(f"{BASE}/api/clear_availability/{candidate_email}")

# -----------------------------
# LLM Matching Function
# -----------------------------

def llm_match(candidate_slots, interviewer_data):
    prompt = f"""
You are an AI scheduling assistant.

Candidate availability:
{candidate_slots}

Interviewer availability:
{interviewer_data}

Find the earliest overlapping 30-minute window.

Return ONLY valid JSON in exactly this format:

If match found:
{{
 "match_found": "yes",
 "slot_start": "YYYY-MM-DDTHH:MMZ",
 "slot_end":   "YYYY-MM-DDTHH:MMZ",
 "interviewer_id": "string"
}}

If no overlap:
{{
 "match_found": "no"
}}
"""

    raw = llm.generate_text(prompt=prompt)
    print("LLM Raw Output:", raw)

    try:
        return json.loads(raw)
    except:
        return {"match_found": "no"}

# -----------------------------
# MAIN RETRY MATCHER LOGIC
# -----------------------------

def main():
    updated = fetch_updated_availability()
    if not updated:
        print("No updates yet.")
        return

    interviewers = get_interviewers()

    # Prepare interviewer structured data
    interviewer_data = []
    for iv in interviewers:
        interviewer_data.append({
            "interviewer_id": iv["id"],
            "slots": iv["free_slots"]
        })

    for email, slots in updated.items():
        print("Checking:", email)
        match = llm_match(slots, interviewer_data)

        if match.get("match_found") == "yes":
            print("LLM found match for:", email)
            create_booking(match, email)
            send_email(email, match)
            clear(email)
        else:
            print("LLM: No overlap for:", email)


if __name__ == "__main__":
    main()
