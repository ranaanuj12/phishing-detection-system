# 🛡 PhishGuard – Phishing Detection System

A beginner-friendly phishing detection system that integrates:
**HTML/CSS/JS Frontend → Java Spring Boot Backend → Python Flask ML Model**

---

## 📁 Folder Structure

```
phishing-detector/
│
├── frontend/
│   ├── index.html      ← The webpage UI
│   ├── style.css       ← All styling
│   └── script.js       ← Fetch API calls to Java backend
│
├── backend/
│   ├── pom.xml         ← Maven build file (Java dependencies)
│   └── src/main/java/com/phishguard/
│       ├── PhishGuardApplication.java  ← Main Spring Boot entry point
│       ├── PhishController.java        ← REST API endpoint (/check)
│       └── PhishService.java           ← Calls Python Flask API
│
└── ml_model/
    ├── model.py          ← Trains & saves the ML model
    ├── app.py            ← Flask server exposing /predict endpoint
    └── requirements.txt  ← Python packages to install
```

---

## 🔄 How It Works (Full Flow)

```
User types URL/text in browser
       ↓
[Frontend: script.js]
  POST http://localhost:8080/check
  Body: { "input": "http://suspicious.com" }
       ↓
[Java: PhishController.java]
  Receives request, passes to PhishService
       ↓
[Java: PhishService.java]
  POST http://localhost:5000/predict
  Body: { "text": "http://suspicious.com" }
       ↓
[Python: app.py + model.py]
  Runs Logistic Regression model
  Returns: { "prediction": 1 }
       ↓
[Java: PhishService → PhishController]
  Returns: { "result": 1 } to frontend
       ↓
[Frontend: script.js]
  Shows ⚠️ Phishing Detected! (or ✅ Safe)
```

---

## 🛠 VS Code Setup

### Extensions to Install

Open VS Code → Extensions panel (Ctrl+Shift+X) → Search and install:

| Extension | Purpose |
|---|---|
| **Extension Pack for Java** (Microsoft) | Java language support, Maven, Spring Boot |
| **Spring Boot Extension Pack** (VMware) | Run Spring Boot apps easily |
| **Python** (Microsoft) | Python language support |
| **Pylance** (Microsoft) | Better Python IntelliSense |
| **Live Server** (Ritwick Dey) | Open HTML files in browser with auto-refresh |
| **REST Client** (Humao) | Test APIs directly in VS Code |

---

## 🚀 Step-by-Step Running Guide

### Prerequisites (Install these first)

- **Java 17+** → https://adoptium.net/
- **Maven 3.8+** → https://maven.apache.org/download.cgi
- **Python 3.9+** → https://www.python.org/downloads/
- **VS Code** → https://code.visualstudio.com/

Verify installation:
```bash
java -version       # should show 17.x.x
mvn -version        # should show 3.x.x
python --version    # should show 3.x.x
```

---

### Step 1 – Open Project in VS Code

```bash
# In VS Code, open the phishing-detector folder:
File → Open Folder → select  phishing-detector/
```

---

### Step 2 – Set Up and Run the Python ML Server

Open a **new terminal** in VS Code (`Ctrl+`` ` ``):

```bash
# Navigate to the ml_model folder
cd ml_model

# Install required Python packages
pip install -r requirements.txt

# Train the model (creates phish_model.pkl)
python model.py

# Start the Flask API server
python app.py
```

✅ You should see:
```
✅ Model loaded successfully.
🌐 Starting PhishGuard Flask ML server on http://localhost:5000
```

**Test it:** Open your browser → `http://localhost:5000/health`
Should show: `{"message": "PhishGuard ML API is up ✅", "status": "running"}`

---

### Step 3 – Run the Java Spring Boot Backend

Open a **second terminal** in VS Code (`Ctrl+Shift+5` to split):

```bash
# Navigate to the backend folder
cd backend

# Run the Spring Boot app using Maven
mvn spring-boot:run
```

First run will download dependencies (~1–2 min). After that:

✅ You should see:
```
✅ PhishGuard Backend is running on http://localhost:8080
```

---

### Step 4 – Open the Frontend

**Option A – Using Live Server (recommended):**
1. In VS Code, right-click `frontend/index.html`
2. Select **"Open with Live Server"**
3. Browser opens automatically at `http://127.0.0.1:5500`

**Option B – Direct file:**
1. Navigate to `frontend/` folder in your file explorer
2. Double-click `index.html`
3. Opens in your default browser

---

### Step 5 – Test the System

1. In the browser, type a suspicious URL like:
   ```
   http://paypal-secure-login.xyz/verify-account
   ```
2. Click **Check Now**
3. You should see: **⚠️ Phishing Detected!**

Try a safe URL:
```
https://www.google.com
```
You should see: **✅ Safe**

---

## 🧪 Testing Each Part Independently

### Test Python Flask only (without Java):
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "http://paypa1-verify.xyz"}'

# Expected: {"prediction": 1, "label": "Phishing", "confidence": 95.2}
```

### Test Java backend only (without frontend):
```bash
curl -X POST http://localhost:8080/check \
  -H "Content-Type: application/json" \
  -d '{"input": "https://www.google.com"}'

# Expected: {"result": 0}
```

---

## ❓ Troubleshooting

| Problem | Solution |
|---|---|
| `mvn: command not found` | Add Maven to PATH or use VS Code Spring Boot extension |
| `python: command not found` | Try `python3` instead of `python` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| Frontend shows "could not connect" | Make sure Java server is running on port 8080 |
| Java shows "Error contacting Python" | Make sure Flask server is running on port 5000 |
| Port already in use | Kill the process or change the port number |

---

## 📌 Port Summary

| Service | Port | URL |
|---|---|---|
| Python Flask ML | 5000 | http://localhost:5000 |
| Java Spring Boot | 8080 | http://localhost:8080 |
| Frontend (Live Server) | 5500 | http://localhost:5500 |

---

## 🔮 Ideas to Extend This Project

- Add a database to log all checked URLs
- Use a real phishing dataset (PhishTank, OpenPhish)
- Add more ML features (URL length, special char count, domain age)
- Add user login with Spring Security
- Deploy to cloud (AWS / Heroku / Railway)
