package com.example.devtasks.dto;

import com.example.devtasks.entity.Domain;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class UserRequest {
    @NotBlank
    private String username;
    private String fullName;
    private String email;
    private Domain domain;
    private String webHook;
}
