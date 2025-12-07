package com.example.devtasks.dto;

import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;

import com.example.devtasks.entity.Domain;

@Data
@Builder
public class UserResponse {
    private Long id;
    private String username;
    private String fullName;
    private String email;
    private LocalDateTime createdAt;
    private Domain domain;
    private String webHook;
}
