# app.py
from flask import Flask, request, abort, make_response
from twilio.twiml.messaging_response import MessagingResponse
from agents import process_whatsapp_message, process_ussd_input
from db import get_session, update_session, init_db
import os

app = Flask(__name__)

# Initialize DB on startup
init_db()

# ==================== WHATSAPP (Twilio) ====================
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()
    media_url = request.values.get("MediaUrl0")
    profile_name = request.values.get("ProfileName", "User")

    response_text = process_whatsapp_message(incoming_msg, media_url, profile_name)

    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)


# ==================== USSD (Africa's Talking) ====================
@app.route("/ussd/callback", methods=["POST"])
def ussd_callback():
    if request.method != "POST":
        abort(400)

    session_id = request.values.get("sessionId")
    phone_number = request.values.get("phoneNumber")
    user_input = request.values.get("text", "").strip()

    if not session_id:
        return "END Error: Missing session", 400

    # Get or initialize session
    session = get_session(session_id)
    if not session:
        update_session(session_id, phone_number, step=1, temp_data="")
        return "CON Karibu NoChai! 💪\nHii ni AI yako ya kukataa rushwa.\nAndika maelezo ya rushwa uliyokutana nayo (mahali, kiasi, nani aliuliza)"

    current_step = session["step"]
    temp_data = session["temp_data"] or ""

    response = process_ussd_input(session_id, phone_number, user_input, current_step, temp_data)

    resp = make_response(response, 200)
    resp.headers["Content-Type"] = "text/plain"
    return resp


# Health check
@app.route("/")
def home():
    return "NoChai AI Server Running 🟢 | USSD + WhatsApp Anti-Corruption Bot"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)