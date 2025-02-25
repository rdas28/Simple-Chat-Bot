from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

# Load Gemini API Key
genai.configure(api_key="Your_GEMINI_KEY")

# Initialize Model
model = genai.GenerativeModel("gemini-pro")

# Chat History
history = []

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Append to chat history
    history.append(f"You: {user_input}")
    full_prompt = "\n".join(history)

    # Generate response from Gemini AI
    response = model.generate_content(full_prompt)
    bot_reply = response.text.strip()

    # ✅ Fix: Remove duplicate prefixes
    bot_reply = bot_reply.replace("Gemini:", "").replace("Bard:", "").strip()

    # Append clean bot response to history
    history.append(f"Gemini: {bot_reply}")

    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)  # Change port here


