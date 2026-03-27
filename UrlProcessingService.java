package com.phishing.service;

public class UrlProcessingService {

    public String processUrl(String url) {
        if (!url.startsWith("http")) {
            url = "http://" + url;
        }
        return url.toLowerCase().trim();
    }
}
