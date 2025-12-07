package com.example.devtasks.service;

import com.example.devtasks.dto.UserRequest;
import com.example.devtasks.dto.UserResponse;

import java.util.List;

public interface UserService {
    UserResponse createUser(UserRequest request);
    UserResponse getUserById(Long id);
    List<UserResponse> getAllUsers();
    void deleteUser(Long id);
}
