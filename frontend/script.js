// ============================================================
//  script.js  –  PhishGuard Frontend Logic
//  
//  Flow: User Input → Java Backend (/check) → Show Result
//  
//  NOTE: Java backend must be running on http://localhost:8080
// ============================================================

// ---- URL of the Java Spring Boot backend ----
const BACKEND_URL = "http://localhost:8080/check";

/**
 * Main function called when user clicks "Check Now".
 * It reads the input, sends it to the Java backend,
 * and displays the Safe or Phishing result.
 */
async function checkInput() {

  // --- Step 1: Read user input ---
  const inputBox = document.getElementById("urlInput");
  const userInput = inputBox.value.trim();   // remove extra spaces

  // --- Step 2: Validate (don't allow empty input) ---
  if (!userInput) {
    showError("⚠️ Please enter a URL or text first.");
    return;
  }

  // --- Step 3: Show loading state on button ---
  setLoading(true);
  hideResult();
  hideError();

  try {
    // --- Step 4: Send POST request to Java backend ---
    // We send JSON: { "input": "http://example.com" }
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ input: userInput })
    });

    // --- Step 5: Check if the network response is OK ---
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    // --- Step 6: Parse JSON response from backend ---
    // Expected format: { "result": 0 } or { "result": 1 }
    // 0 = Safe, 1 = Phishing
    const data = await response.json();

    // --- Step 7: Display the result to the user ---
    displayResult(data.result);

  } catch (error) {
    // If anything goes wrong (backend down, network error, etc.)
    console.error("Error contacting backend:", error);
    showError("❌ Could not connect to backend. Make sure the Java server is running on port 8080.");
  } finally {
    // Always turn off loading state
    setLoading(false);
  }
}


/**
 * Displays the result box as either Safe or Phishing.
 * @param {number} result - 0 means Safe, 1 means Phishing
 */
function displayResult(result) {
  const resultBox   = document.getElementById("resultBox");
  const resultIcon  = document.getElementById("resultIcon");
  const resultLabel = document.getElementById("resultLabel");
  const resultDesc  = document.getElementById("resultDesc");

  // Remove any previous color class
  resultBox.classList.remove("safe", "phishing", "hidden");

  if (result === 0) {
    // --- SAFE ---
    resultBox.classList.add("safe");
    resultIcon.textContent  = "✅";
    resultLabel.textContent = "Safe";
    resultDesc.textContent  = "This URL/text appears to be legitimate. No phishing signals detected.";

  } else if (result === 1) {
    // --- PHISHING ---
    resultBox.classList.add("phishing");
    resultIcon.textContent  = "⚠️";
    resultLabel.textContent = "Phishing Detected!";
    resultDesc.textContent  = "This URL/text shows signs of phishing. Do NOT click or share this link.";

  } else {
    // Unexpected result from server
    showError("Unexpected response from server. Please try again.");
  }
}


/**
 * Shows or hides the loading spinner on the button.
 * @param {boolean} isLoading - true to show spinner, false to hide
 */
function setLoading(isLoading) {
  const btnText   = document.getElementById("btnText");
  const btnLoader = document.getElementById("btnLoader");
  const checkBtn  = document.getElementById("checkBtn");

  if (isLoading) {
    btnText.textContent = "Checking...";
    btnLoader.classList.remove("hidden");
    checkBtn.disabled = true;    // prevent double-clicks
  } else {
    btnText.textContent = "Check Now";
    btnLoader.classList.add("hidden");
    checkBtn.disabled = false;
  }
}


/** Hides the result box */
function hideResult() {
  const resultBox = document.getElementById("resultBox");
  resultBox.classList.add("hidden");
  resultBox.classList.remove("safe", "phishing");
}


/**
 * Shows an error message below the button.
 * @param {string} message - The error text to display
 */
function showError(message) {
  const errorMsg = document.getElementById("errorMsg");
  errorMsg.textContent = message;
  errorMsg.classList.remove("hidden");
}


/** Hides the error message */
function hideError() {
  const errorMsg = document.getElementById("errorMsg");
  errorMsg.classList.add("hidden");
}


// ---- Allow pressing Enter (Ctrl+Enter) to trigger check ----
document.addEventListener("DOMContentLoaded", () => {
  const inputBox = document.getElementById("urlInput");
  inputBox.addEventListener("keydown", (event) => {
    // Ctrl+Enter or Cmd+Enter submits
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      checkInput();
    }
  });
});
