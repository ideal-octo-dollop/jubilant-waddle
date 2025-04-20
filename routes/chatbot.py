from flask import Blueprint, render_template, request, jsonify
import requests
from utils import login_required

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route("/chatbot")
@login_required
def chatbot_ui():
    return render_template("chatbot.html")

@chatbot_bp.route("/ask", methods=["POST"])
@login_required
def ask_phi():
    user_input = request.json.get("prompt", "")
    
    try:
        payload = {
            "model": "llama3",
            "prompt": user_input,
            "stream": False
        }

        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return jsonify({"response": data.get("response", "")})
        else:
            return jsonify({"error": f"Ollama API error: {response.status_code}"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Connection error: {str(e)}"}), 503