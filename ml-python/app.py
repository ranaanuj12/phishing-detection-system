# ============================================================
#  app.py  –  Flask API Server for ML Predictions
#
#  This file loads the trained model and exposes one endpoint:
#    POST /predict
#    Input:  { "text": "http://some-url.com" }
#    Output: { "prediction": 0 }  or  { "prediction": 1 }
#
#  Run AFTER model.py:   python app.py
#  Server starts at:     http://localhost:5000
# ============================================================

import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS   # allows Java backend to call this API

# ---- Create the Flask application ----
app = Flask(__name__)

# Allow Cross-Origin requests (needed so Java can call Python)
CORS(app)

# ---- Load the saved model at startup ----
MODEL_FILE = "phish_model.pkl"

print("📦 Loading phishing detection model...")
try:
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)   # load the trained Pipeline
    print("✅ Model loaded successfully.")
except FileNotFoundError:
    print("❌ Model file not found! Please run model.py first.")
    model = None


# ============================================================
#  Route: POST /predict
#  
#  Called by Java backend to get a prediction from the ML model.
# ============================================================
@app.route("/predict", methods=["POST"])
def predict():

    # --- Step 1: Check that we received JSON data ---
    data = request.get_json()

    if not data:
        # Return error if body is empty or not JSON
        return jsonify({"error": "No JSON data received"}), 400

    # --- Step 2: Extract the "text" field from the request body ---
    text_input = data.get("text", "").strip()

    if not text_input:
        return jsonify({"error": "Field 'text' is required"}), 400

    # --- Step 3: Check model is loaded ---
    if model is None:
        return jsonify({"error": "ML model not loaded. Run model.py first."}), 500

    # --- Step 4: Run prediction ---
    # model.predict() expects a list, returns a list
    prediction = model.predict([text_input])[0]   # 0 or 1

    # Get the probability score (confidence)
    proba = model.predict_proba([text_input])[0]  # [prob_safe, prob_phishing]
    confidence = round(float(max(proba)) * 100, 1)

    print(f"🔍 Input: {text_input[:60]}")
    print(f"   Result: {'Phishing' if prediction == 1 else 'Safe'} ({confidence}% confidence)")

    # --- Step 5: Return the result as JSON ---
    return jsonify({
        "prediction":  int(prediction),   # 0 = Safe, 1 = Phishing
        "confidence":  confidence,         # e.g. 91.3 (percent)
        "label":       "Phishing" if prediction == 1 else "Safe"
    })


# ============================================================
#  Route: GET /health
#  
#  Simple health check — useful to confirm the server is running.
#  Open http://localhost:5000/health in your browser to test.
# ============================================================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "model_loaded": model is not None,
        "message": "PhishGuard ML API is up ✅"
    })


# ---- Start the server ----
if __name__ == "__main__":
    print("🌐 Starting PhishGuard Flask ML server on http://localhost:5000")
    print("   Press Ctrl+C to stop the server.")
    app.run(host="0.0.0.0", port=5000, debug=True)
