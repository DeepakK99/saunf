package com.example.devtasks.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String username;

    @Column(length = 200)
    private String full_name;

    @Column(unique = true, length = 200)
    private String email;

    @Column(nullable = false, updatable = false)
    private LocalDateTime created_at;

    @Column(nullable = false)
    private String discord_webhook;

    @Enumerated(EnumType.STRING)
    private Domain domain;

    @Column(nullable = false)
    private boolean is_active;

    public User() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getFullName() { return full_name; }
    public void setFullName(String fullName) { this.full_name = fullName; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public LocalDateTime getCreatedAt() { return created_at; }
    public void setCreatedAt(LocalDateTime createdAt) { this.created_at = createdAt; }

    public Domain getDomain() {
        return domain;
    }
    public void setDomain(Domain domain) {
        this.domain = domain;
    }

    public boolean getIsActive() {
        return is_active;
    }

    public void setIsActive(boolean is_active) {
        this.is_active = is_active;
    }

    public String getWebHook() {
        return discord_webhook;
    }
    public void setWebHook(String webHook) {
        this.discord_webhook = webHook;
    }

    @PrePersist
    public void prePersist() {
        if (this.created_at == null) this.created_at = LocalDateTime.now();
        this.is_active = true;
    }
}
