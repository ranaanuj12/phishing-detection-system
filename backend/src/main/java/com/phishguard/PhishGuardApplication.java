// ============================================================
//  PhishGuardApplication.java  –  Spring Boot Entry Point
//
//  This is the main class that starts the entire Java backend.
//  Spring Boot auto-configures everything when you run this.
// ============================================================

package com.phishguard;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

// @SpringBootApplication combines:
//   @Configuration   – marks this as a config class
//   @EnableAutoConfiguration – lets Spring Boot auto-setup
//   @ComponentScan   – scans this package for controllers/services
@SpringBootApplication
public class PhishGuardApplication {

    public static void main(String[] args) {
        // This single line boots up the entire Spring application
        SpringApplication.run(PhishGuardApplication.class, args);
        System.out.println("✅ PhishGuard Backend is running on http://localhost:8080");
    }
}
