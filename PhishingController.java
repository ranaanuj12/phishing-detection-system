package com.phishing.controller;

import org.springframework.web.bind.annotation.*;
import java.util.*;

import com.phishing.service.*;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class PhishingController {

    private UrlProcessingService urlService = new UrlProcessingService();
    private FeatureExtractionService featureService = new FeatureExtractionService();
    private MLService mlService = new MLService();

    @PostMapping("/check")
    public Map<String, Object> checkUrl(@RequestBody Map<String, String> request) {

        String url = request.get("url");

        String processedUrl = urlService.processUrl(url);

        var features = featureService.extractFeatures(processedUrl);

        String prediction = mlService.getPrediction(features);

        Map<String, Object> response = new HashMap<>();
        response.put("processedUrl", processedUrl);
        response.put("prediction", prediction);

        return response;
    }
}