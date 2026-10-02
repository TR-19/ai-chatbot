from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Ollama API endpoint (local)
OLLAMA_URL = "http://localhost:11434/api/generate"

# Store chat history for memory
chat_history = []


@app.route('/')
def intro():
    return render_template("intro.html")


@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")


@app.route('/chat', methods=['POST'])
def chat():
    global chat_history

    user_message = request.json.get("message", "").strip()

    if user_message == "":
        return jsonify({"reply": "Please type a message."})

    # Add user message to history
    chat_history.append(f"User: {user_message}")

    # Keep only last 6 messages for faster memory
    if len(chat_history) > 6:
        chat_history = chat_history[-6:]

    context_prompt = "\n".join(chat_history)

    # BEST PROMPT (General + AI focus + Grammar correct + Friendly + Memory)
    prompt = f"""
You are Idopia AI Assistant, a smart and friendly chatbot.

You can answer questions from any domain such as:
AI, Machine Learning, Deep Learning, Programming, Science, Math, Technology, Education, and General Knowledge.

Instructions:
1. Always respond with correct grammar and professional English.
2. Be conversational and interactive like a real assistant.
3. If the user asks follow-up questions, use previous chat context.
4. Keep the answer short: maximum 3 to 4 lines.
5. If the user asks "advantages", "disadvantages", or "applications", answer based on the previous topic.
6. If the question is unclear, politely ask what exactly the user means.

Conversation so far:
{context_prompt}

Assistant:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()
        reply = result.get("response", "").strip()

        if reply == "":
            reply = "I could not generate a response. Please try again."

    except Exception as e:
        reply = f"Error: {str(e)}"

    # Add bot response to history
    chat_history.append(f"Assistant: {reply}")

    return jsonify({"reply": reply})


if __name__ == "__main__":
    print("Starting Idopia AI Assistant...")
    app.run(debug=True)