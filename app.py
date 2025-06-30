from flask import Flask, request, jsonify
import pandas as pd

# URL of the Google Sheet published as CSV
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmzKG-WtuZQ79ajXoWg0GilXTcTzZ6Sz-0S1pCAwYpHeN6xGtndSUcr2pbEYf8UpaIB_v1HDEs0wOp/pub?output=csv"

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # Browser test
    if request.method == "GET":
        return "✅ Webhook is live. Use POST to ask a question."

    try:
        # Load CSV data from Google Sheet
        df = pd.read_csv(CSV_URL)
        user_msg = request.json.get("message", "").strip().lower()

        # Handle empty message
        if not user_msg:
            return jsonify({"reply": "❗ Please enter a valid message."})

        # Search for matching question
        for _, row in df.iterrows():
            if row['Question'].strip().lower() in user_msg:
                return jsonify({"reply": row['Answer']})

        return jsonify({"reply": "🤖 Sorry, I don't have an answer for that."})
    
    except Exception as e:
        return jsonify({"reply": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
