from flask import Blueprint, jsonify, render_template, request
from google import genai
import os
BuddyBot_bp = Blueprint('BuddyBot',__name__)

@BuddyBot_bp.route('/BuddyBot',methods=['GET','POST'])
def chat():
    if request.method == "GET":
        return render_template("chat.html")

    payload = request.get_json(silent=True) or {}
    prompt = payload.get("Input")
    if not isinstance(prompt, str) or not prompt.strip():
        return jsonify({"error": "Invalid input"}), 400

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY is not configured"}), 503

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
            contents=prompt.strip(),
            config={
                "temperature": 0.5,
                "max_output_tokens": 1200,
                "system_instruction": (
                    "You are Buddy Bot, a warm, dependable emotional-support companion. "
                    "Be gently chirpy and encouraging without being childish, forced, "
                    "or overly cheerful. Respond with maturity, patience, empathy, and "
                    "clear practical guidance. Listen carefully, validate the user's "
                    "feelings, and ask thoughtful follow-up questions when helpful. "
                    "Offer small, realistic coping steps such as breathing, grounding, "
                    "rest, journaling, or reaching out to a trusted person. Never shame, "
                    "diagnose, or make promises you cannot keep. Do not pretend to be a "
                    "therapist or emergency service. If the user may be in immediate "
                    "danger or considering self-harm, respond calmly and directly: "
                    "encourage them to contact local emergency services or a crisis line, "
                    "and to stay with a trusted person if possible. Keep responses "
                    "concise, reassuring, and focused on the user's next safe step. "
                    "Keep normal replies under 180 words, use complete sentences, "
                    "and never stop in the middle of a sentence or bullet point."
                ),
            },
        )
        if not response.text:
            return jsonify({"error": "Gemini returned an empty response"}), 502
        return jsonify({"message": response.text})
    except Exception:
        return jsonify({"error": "The support chatbot is unavailable right now"}), 502
