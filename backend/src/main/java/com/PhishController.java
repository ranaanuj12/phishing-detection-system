// ============================================================
//  PhishController.java  –  REST API Controller
//
//  Handles HTTP requests from the frontend.
//  Exposes one endpoint: POST /check
//
//  The frontend calls this → we call Python ML → return result
// ============================================================

package com.phishguard;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

// @RestController means this class handles web requests and
// returns data (JSON) directly, not HTML pages
@RestController

// @CrossOrigin allows the frontend (a different origin/port)
// to call this API — without this, browsers block the request
@CrossOrigin(origins = "*")
public class PhishController {

    // Spring automatically injects the PhishService bean here
    @Autowired
    private PhishService phishService;

    /**
     * POST /check
     *
     * Receives JSON from frontend:  { "input": "http://some-url.com" }
     * Returns JSON to frontend:     { "result": 0 }  or  { "result": 1 }
     *
     * @param requestBody  - Map representing the incoming JSON body
     * @return             - Map representing the outgoing JSON response
     */
    @PostMapping("/check")
    public Map<String, Object> checkUrl(@RequestBody Map<String, String> requestBody) {

        // Extract the "input" field from the incoming JSON
        String userInput = requestBody.get("input");

        System.out.println("📥 Received input: " + userInput);

        // Call the service layer to contact the Python ML model
        int predictionResult = phishService.getPrediction(userInput);

        System.out.println("📤 Prediction result: " + predictionResult + 
                           (predictionResult == 1 ? " (Phishing)" : " (Safe)"));

        // Build and return the JSON response
        Map<String, Object> response = new HashMap<>();
        response.put("result", predictionResult);  // 0 = Safe, 1 = Phishing
        return response;
    }
}
