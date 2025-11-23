🧠 SmartSlot — AI-Powered Interview Scheduling using IBM Watsonx Orchestrate

SmartSlot is an agentic AI interview scheduling system powered by IBM watsonx Orchestrate, designed to remove the delay, friction, and manual coordination involved in scheduling interviews between candidates and HR teams.

Using LLM reasoning, workflow automation, calendar parsing, and email integrations, SmartSlot ensures interviews are scheduled smoothly — or escalated automatically when no match exists.

This project demonstrates full use of Watsonx Orchestrate tools, agent toolsets, workflow orchestration, LLM-powered decision-making, and real-world HR automation.

🚀 Features
🌐 Modern Candidate UI

FullCalendar-based drag-and-drop interface

Auto-conversion to ISO8601 time slots

Smooth submission → backend integration

🧠 LLM-Powered Slot Matching

IBM Watsonx Orchestrate agent + digital skills

Overlap detection using llama-3 models

Structured JSON responses

Reasoned explanation for match/no-match

🔁 Automatic Retry System

GitHub Actions cron job

Fetches updated availability

Re-runs Orchestrate matching

Sends booking emails automatically

📬 Email Automation

Using SendGrid API:

Interview confirmation

No-slot notifications

HR escalation emails

🏢 Real HR Workflow Logic

Stores candidate availability

Attempts matching

Retries on update

Escalates when repeated failures occur

🧩 System Architecture
Candidate UI → Backend API → Save Availability  
          ↓
GitHub Cron → WatsonX Orchestrate Workflow  
          ↓
LLM Tool → Best Slot or No-Match  
          ↓
Backend → SendGrid Emails → Candidate / HR

🧠 Use of IBM Watsonx Orchestrate (Hackathon Requirement)

SmartSlot uses Orchestrate’s full capability:

✔ 1. Custom Digital Skill (Tool)

slot_matcher / availability_parser

Accepts candidate + interviewer availability

Calls llama-3 LLM

Determines overlap

Recommends a time slot

Returns structured JSON

✔ 2. Orchestrated Workflow

The workflow:

Reads inputs

Invokes your custom tool

Checks match/no match

Sends a clear output back to backend

✔ 3. Agent + Toolset

The SmartSlot agent uses this tool automatically, allowing:

Automated decisions

Reasoning-based matching

Multi-step orchestration

✔ 4. Integrations

Backend connects via API

Emails sent via SendGrid

Automatic retries via GitHub Actions

Frontend calendar ingestion

This fully meets the challenge theme:

“Build the next generation of agentic AI with watsonx Orchestrate.”

🖥️ Live Backend
https://backend-email-7jn1.onrender.com/

📡 Backend API Endpoints
POST /api/save_updated_availability

Save new candidate availability.

GET /api/get_updated_availability

View stored availability.

GET /reschedule

Legacy reschedule page.

POST /sendEmail

Send booking confirmation email.

POST /sendNoSlotEmail

Send “no slot found” email.

POST /sendHREscalation

Escalate when matching repeatedly fails.

POST /api/clear_availability/<email>

Clear candidate availability.

POST /api/match

Run initial LLM match.

POST /api/retry

Retry matching manually.

🖼️ Frontend Calendar Libraries
https://unpkg.com/fullcalendar@6.1.8/main.min.css
https://unpkg.com/fullcalendar@6.1.8/main.min.js
https://unpkg.com/fullcalendar@6.1.8/index.global.min.js
https://cdn.jsdelivr.net/npm/moment@2.29.4/moment.min.js

📬 SendGrid Integration

SendGrid API:

https://api.sendgrid.com/v3/mail/send


Environment variables:

SENDGRID_API_KEY = hijk
FROM_EMAIL = lmno

🧠 Watsonx Orchestrate Credentials
WATSONX_API_KEY = defg
WATSONX_PROJECT_ID = abcd
WATSONX_REGION = ca-tor

🧪 How to Test the Entire System (Step-by-Step)
✔ 1. Open the Calendar UI
https://backend-email-7jn1.onrender.com/select_availability

✔ 2. Enter your email

Example:

test@example.com

✔ 3. Select a time by dragging on the calendar

The block turns blue.

✔ 4. Click Submit Availability

You should see a success message.

✔ 5. Confirm backend stored it

Visit:

https://backend-email-7jn1.onrender.com/api/get_updated_availability


You’ll see your email + slots.

✔ 6. GitHub Action Triggers Matching

Every few minutes:

Calls Watsonx Orchestrate

Runs your agent + digital skill

Determines a time

✔ 7. Check your email

You will receive:

🎉 If a slot is found

Interview Confirmation Email

🔁 If no match

Please update your availability email

📢 If still no matches

HR escalation email

This demonstrates full real-world automation.

🏁 Why SmartSlot Matters

Removes manual HR bottlenecks

Reduces candidate drop-offs

Uses LLM reasoning for decisions

Perfect real-world use case for Orchestrate

Future-of-work AI system

Fully autonomous scheduling pipeline
