from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # Basic reply logic (can be replaced with AI later)
    if "track" in user_message:
        reply = "Please provide your tracking ID."
    elif "quote" in user_message:
        reply = "Sure, what type of freight are you shipping?"
    elif "hello" in user_message or "hi" in user_message:
        reply = "Hello! How can I assist you with your logistics today?"
    else:
        reply = "I'm here to help with tracking, booking, and freight questions!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
