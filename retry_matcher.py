import requests
import json

BASE = "https://backend-email-7jn1.onrender.com"

def fetch_updated_availability():
    r = requests.get(f"{BASE}/api/get_updated_availability")
    return r.json()

def get_interviewers():
    r = requests.get(f"{BASE}/api/get_interviewers")
    return r.json()

def retry_match(candidate_email, new_slots, interviewers):
    cand_start, cand_end = new_slots.split("/")

    # very simple overlap check
    for interviewer in interviewers:
        iv_id = interviewer["id"]
        for slot in interviewer["free_slots"]:
            iv_start, iv_end = slot.split("/")
            if cand_start >= iv_start and cand_end <= iv_end:
                return {
                    "match_found": True,
                    "interviewer_id": iv_id,
                    "slot_start": cand_start,
                    "slot_end": cand_end
                }
    return {"match_found": False}

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
        match = retry_match(email, slots, interviewers)
        
        if match["match_found"]:
            print("Match found for:", email)
            booking = create_booking(match, email)
            send_email(email, match)
            clear(email)
        else:
            print("No overlap for:", email)

if __name__ == "__main__":
    main()
