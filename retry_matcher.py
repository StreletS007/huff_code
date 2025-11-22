import os
import json
import requests

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model

BASE = "https://backend-email-7jn1.onrender.com"

def fetch_updated_availability():
    r = requests.get(f"{BASE}/api/get_updated_availability")
    return r.json()

def get_interviewers():
    r = requests.get(f"{BASE}/api/get_interviewers")
    return r.json()

def llm_match(candidate_slots, interviewer_slots):

    prompt = f"""
You are a scheduling AI.

Candidate new availability:
{candidate_slots}

Interviewer availability:
{interviewer_slots}

Find the earliest overlapping 30-minute slot.
If match exists, respond ONLY in JSON:
{{
  "match_found": "yes",
  "slot_start": "...",
  "slot_end": "...",
  "interviewer_id": "..."
}}

If no match, respond:
{{
  "match_found": "no"
}}
"""

    creds = Credentials(
        api_key=os.environ["WATSONX_API_KEY"],
        url=os.environ["WATSONX_URL"]
    )

    model = Model(
        model_id="meta-llama/llama-3-8b-instruct",
        credentials=creds,
        project_id=os.environ["PROJECT_ID"]
    )

    response = model.generate(
        input_text=prompt,
        parameters={
            "decoding_method": "greedy",
            "max_new_tokens": 200
        }
    )

    text = response["results"][0]["generated_text"]

    try:
        return json.loads(text)
    except:
        return {"match_found": "no"}

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

def main():
    updated = fetch_updated_availability()
    if not updated:
        print("No updates yet.")
        return
    
    interviewers = get_interviewers()

    for email, slots in updated.items():
        print("Checking:", email)

        match = llm_match(slots, interviewers)

        if match.get("match_found") == "yes":
            print("Match found for:", email)
            create_booking(match, email)
            send_email(email, match)
            clear(email)
        else:
            print("No overlap for:", email)

if __name__ == "__main__":
    main()
