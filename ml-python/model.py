# ============================================================
#  model.py  –  Train and Save the Phishing Detection ML Model
#
#  Algorithm: Logistic Regression (simple, beginner-friendly)
#  Features:  We extract simple text features from URLs/text
#
#  Run this FIRST to generate "phish_model.pkl"
#  Command:   python model.py
# ============================================================

import pickle                          # to save/load the model
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline  # chains vectorizer + model
from sklearn.metrics import accuracy_score

# ---- Step 1: Create a small labeled dataset ----
#
# In a real project, you'd use a large dataset (e.g. PhishTank).
# Here we use a small handcrafted dataset to keep it simple.
#
# Label:  0 = Safe,  1 = Phishing

training_data = [
    # Phishing examples (label = 1)
    ("http://paypa1-secure-login.xyz/verify-account",        1),
    ("http://amazon-update-billing.com/login",               1),
    ("http://secure-bank-alert.net/reset-password",          1),
    ("http://faceb00k-verify.com/confirm-identity",          1),
    ("http://apple-id-suspended.info/unlock-now",            1),
    ("click here to claim your free prize now",              1),
    ("urgent: your account has been compromised verify now", 1),
    ("http://192.168.1.1/admin/steal-credentials",           1),
    ("http://login-update.secure-site.ru/bank",              1),
    ("win a free iphone just enter your password",           1),
    ("http://netflix-billing-issue.com/update-card",         1),
    ("http://paypal-account-verify.co/signin",               1),
    ("free gift card click this link now to redeem",         1),
    ("http://google-security-alert.biz/verify-email",        1),
    ("http://microsoft-support-warning.com/fix-now",         1),

    # Safe examples (label = 0)
    ("http://www.google.com/search?q=python",                0),
    ("https://www.wikipedia.org/wiki/Machine_learning",      0),
    ("https://github.com/user/my-project",                   0),
    ("https://stackoverflow.com/questions/12345",            0),
    ("https://www.amazon.com/dp/B08N5WRWNW",                 0),
    ("https://mail.google.com/mail/u/0/inbox",               0),
    ("hello how are you doing today",                        0),
    ("https://www.youtube.com/watch?v=abc123",               0),
    ("https://docs.spring.io/spring-boot/docs/current",      0),
    ("meeting at 3pm today in conference room B",            0),
    ("https://www.python.org/downloads/",                    0),
    ("https://www.linkedin.com/in/johndoe",                  0),
    ("please review the attached project proposal",          0),
    ("https://www.reddit.com/r/learnprogramming/",           0),
    ("the weather in new york today is sunny and warm",      0),
]

# ---- Step 2: Separate inputs and labels ----
texts  = [item[0] for item in training_data]   # list of URL/text strings
labels = [item[1] for item in training_data]   # list of 0 or 1

# ---- Step 3: Build a Pipeline ----
#
# A Pipeline chains two steps:
#   (a) TfidfVectorizer: converts text → numbers (word frequency matrix)
#   (b) LogisticRegression: learns patterns and makes predictions
#
# Using a Pipeline makes it easy to save and reuse both steps together.

model_pipeline = Pipeline([
    ("tfidf",  TfidfVectorizer(
        analyzer="char_wb",   # character n-grams work well for URLs
        ngram_range=(3, 4),   # look at sequences of 3–4 characters
        max_features=5000     # limit vocabulary size
    )),
    ("clf", LogisticRegression(
        max_iter=200,         # number of training iterations
        random_state=42       # for reproducibility
    ))
])

# ---- Step 4: Train the model on our dataset ----
print("🚀 Training the phishing detection model...")
model_pipeline.fit(texts, labels)

# ---- Step 5: Quick accuracy check on training data ----
# (In real projects, use a separate test set!)
predictions = model_pipeline.predict(texts)
accuracy = accuracy_score(labels, predictions)
print(f"✅ Training accuracy: {accuracy * 100:.1f}%")

# ---- Step 6: Save the trained model to disk ----
# We use pickle to serialize the Pipeline object
MODEL_FILE = "phish_model.pkl"
with open(MODEL_FILE, "wb") as f:
    pickle.dump(model_pipeline, f)

print(f"💾 Model saved to: {MODEL_FILE}")
print("   Now run: python app.py  to start the Flask API server.")

# ---- Step 7: Quick demo predictions ----
print("\n📋 Sample predictions:")
test_samples = [
    "http://paypal-secure-login.xyz/verify",
    "https://www.google.com",
    "you won a free iphone click here",
    "https://github.com/openai/gpt-4"
]
for sample in test_samples:
    result = model_pipeline.predict([sample])[0]
    label  = "⚠️ Phishing" if result == 1 else "✅ Safe"
    print(f"  {label}  →  {sample[:60]}")
