// ============================================================
//  PhishService.java  –  Business Logic / Service Layer
//
//  This class handles the actual "work":
//    1. Takes the user's input string
//    2. Sends it to the Python Flask ML API (localhost:5000)
//    3. Parses the response and returns 0 (Safe) or 1 (Phishing)
//
//  The Controller should NOT talk to Python directly —
//  that logic lives here in the Service layer (cleaner design).
// ============================================================

package com.phishguard;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;

import java.util.HashMap;
import java.util.Map;

// @Service tells Spring that this is a service component
// Spring will create one instance and share it (a "bean")
@Service
public class PhishService {

    // URL of the Python Flask ML server
    // Flask runs on port 5000 by default
    private static final String PYTHON_ML_URL = "http://localhost:5000/predict";

    /**
     * Sends the user's input to the Python ML server and returns the prediction.
     *
     * @param userInput  - The URL or text entered by the user
     * @return           - 0 if Safe, 1 if Phishing, -1 if error
     */
    public int getPrediction(String userInput) {

        try {
            // RestTemplate is Spring's built-in HTTP client
            RestTemplate restTemplate = new RestTemplate();

            // Build the JSON body to send to Python:  { "text": "http://..." }
            Map<String, String> requestBody = new HashMap<>();
            requestBody.put("text", userInput);

            // Set Content-Type header to application/json
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            // Wrap body + headers into an HttpEntity object
            HttpEntity<Map<String, String>> httpEntity = new HttpEntity<>(requestBody, headers);

            // Make the POST request to Python Flask
            // The response comes back as a Map (parsed from JSON)
            ResponseEntity<Map> response = restTemplate.exchange(
                PYTHON_ML_URL,          // URL to call
                HttpMethod.POST,        // HTTP method
                httpEntity,             // request body + headers
                Map.class               // expected response type
            );

            // Extract the "prediction" field from Python's JSON response
            // Python returns: { "prediction": 0 } or { "prediction": 1 }
            Map<String, Object> responseBody = response.getBody();
            if (responseBody != null && responseBody.containsKey("prediction")) {
                return (Integer) responseBody.get("prediction");
            }

        } catch (Exception e) {
            // Log the error – this usually means Python server isn't running
            System.err.println("❌ Error contacting Python ML server: " + e.getMessage());
            System.err.println("   Make sure the Python Flask server is running on port 5000.");
        }

        // Return -1 to indicate something went wrong
        return -1;
    }
}
