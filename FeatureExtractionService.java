package com.phishing.service;

import com.phishing.model.UrlFeatures;

public class FeatureExtractionService {

    public UrlFeatures extractFeatures(String url) {
        UrlFeatures f = new UrlFeatures();

        f.length = url.length();
        f.hasHttps = url.startsWith("https") ? 1 : 0;
        f.hasAt = url.contains("@") ? 1 : 0;
        f.hasHyphen = url.contains("-") ? 1 : 0;

        return f;
    }
}
