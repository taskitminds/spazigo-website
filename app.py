import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# --- Gemini API Configuration ---
# IMPORTANT: It's highly recommended to set your API key as an environment variable
# for security reasons, rather than hardcoding it.
# You can get your key from Google AI Studio.
try:
    # Attempt to get the API key from an environment variable
    gemini_api_key = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=gemini_api_key)
except KeyError:
    # Fallback for development if the environment variable is not set.
    # REPLACE "YOUR_API_KEY" WITH YOUR ACTUAL GEMINI API KEY.
    gemini_api_key = "YOUR_API_KEY"
    if gemini_api_key == "YOUR_API_KEY":
        print("CRITICAL: Gemini API key is not configured.")
        print("Please set the GEMINI_API_KEY environment variable or replace 'YOUR_API_KEY' in app.py")
    genai.configure(api_key=gemini_api_key)


# Initialize the Gemini model, using the fast 'flash' version for chat.
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/")
def index():
    """
    Renders the main chat page.
    """
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handles chat requests by sending the user's message to the Gemini API
    and returning the AI's response.
    """
    # Get the user's message from the request
    user_message = request.json.get("message", "").strip()

    # Handle empty messages
    if not user_message:
        return jsonify({"reply": "Please enter a message."}), 400
    
    # Check if the API key is still the placeholder
    if gemini_api_key == "YOUR_API_KEY":
         return jsonify({"reply": "The connection to the oracle is severed. The API key has not been configured."})

    # --- Mythic Level Prompt Engineering with Full Context ---
    # This enhanced prompt provides the AI with deep context about the Spazigo platform,
    # followed by instructions on its persona.
    prompt = f"""
You are the AI assistant for a startup called **Spazigo**. Your job is to help users by answering clearly, simply, and effectively — especially small business traders, exporters, and local logistics providers.

🧠 Here’s everything you should remember about Spazigo:

---

🚀 **What is Spazigo?**
Spazigo is a logistics onboarding and space-sharing platform for SMEs. It helps traders and logistics providers connect for booking available space in **trucks, ships, trains, and planes**, especially for **small or partial shipments (LTL)**.

---

💡 **Who uses Spazigo?**
1. **Traders / Exporters / Small Businesses**
   - They want to book space in someone else’s transport.
   - They often don’t understand logistics terms or tech.

2. **Logistics Providers (LSPs)**
   - They have trucks, containers, or vehicles with free space.
   - They want to list their available cargo slots and get bookings.

---

🛠️ **Platform Features**:
- Multi-modal support (Road, Rail, Air, Ship)
- Partial shipment matching (LTL / Less-than-truckload)
- Real-time available space listing by verified LSPs
- Shipper self-registration with document verification
- In-app chat between traders and LSPs
- Built-in secure payments
- Analytics dashboard for shipment tracking
- Smart match engine and filters

---

🔐 **Your Tech Stack** (You, the AI, must be aware of this for context):
- Flutter frontend with dark mode and custom navigation
- Backend in Python using FastAPI + MongoDB + GridFS
- Local encrypted Hive DB for tasks/notes
- Gemini AI used for chatbot replies
- Tailwind HTML designs converted into Flutter
- `Provider` and `SharedPreferences` used for theme management

---

📣 **How You Should Reply**:
- Speak in a **simple**, friendly, and **clear tone** — like talking to a small trader.
- Avoid technical terms unless asked for.
- Be concise, supportive, and explain anything confusing.
- Use real-world examples (like “You can book half a truck going from Mumbai to Delhi.”)
- Never say “I don’t know” — always suggest what to do or who can help.
- Relate your answers back to how Spazigo solves the problem.

---

Now the user says:

"{user_message}"

Respond in a helpful, easy-to-understand way, as Spazigo’s official assistant.
"""

    try:
        # --- Call the Gemini API ---
        # Generate content based on the detailed prompt
        response = model.generate_content(prompt)
        ai_reply = response.text

    except Exception as e:
        # --- Graceful Error Handling ---
        print(f"Error calling Gemini API: {e}")
        ai_reply = "The trade winds are turbulent... I am unable to respond at this moment. Please try again later."

    # Return the AI's reply as JSON
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port from environment or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
