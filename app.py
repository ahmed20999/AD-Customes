from flask import Flask, request, jsonify
import pandas as pd

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmzKG-WtuZQ79ajXoWg0GilXTcTzZ6Sz-0S1pCAwYpHeN6xGtndSUcr2pbEYf8UpaIB_v1HDEs0wOp/pub?output=csv"

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        df = pd.read_csv(CSV_URL)
        user_msg = request.json.get("message", "").lower()

        for _, row in df.iterrows():
            if row['Question'].lower() in user_msg:
                return jsonify({"reply": row['Answer']})

        return jsonify({"reply": "Sorry, I don't have an answer for that."})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)