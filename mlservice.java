package com.phishing.service;

import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;

public class MLService {

    public String getPrediction(Object features) {

        RestTemplate restTemplate = new RestTemplate();

        String url = "http://localhost:5000/predict";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<Object> request = new HttpEntity<>(features, headers);

        ResponseEntity<String> response =
                restTemplate.postForEntity(url, request, String.class);

        return response.getBody();
    }
}