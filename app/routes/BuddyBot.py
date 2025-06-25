from flask import Blueprint,render_template,request,jsonify,Response
import os
import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse,GenerationConfig
BuddyBot_bp = Blueprint('BuddyBot',__name__)

@BuddyBot_bp.route('/BuddyBot',methods=['GET','POST'])
def chat():
    Gemini_api_key = os.getenv('GEMINI_API_KEY')
    userInput = request.get_json()
    # print(userInput)
    if not userInput or 'Input' not in userInput:
      return jsonify({"error": "Invalid input"}), 400
    prompt = userInput['Input']
    genai.configure(api_key=Gemini_api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config= genai.types.GenerationConfig(
            temperature=0.5,
            max_output_tokens=500
        ),
        system_instruction="You are an empathetic support chatbot designed to assist users who may be experiencing trauma-related distress, such as symptoms of PTSD. Your role is to offer compassionate, non-judgmental emotional support, help users feel heard and safe, and gently guide them toward positive coping strategies and self-care."
    )
    response = model.generate_content(prompt)
    return jsonify({"message":response.text})
