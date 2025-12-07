package com.example.devtasks.service.impl;

import com.example.devtasks.dto.UserRequest;
import com.example.devtasks.dto.UserResponse;
import com.example.devtasks.entity.User;
import com.example.devtasks.exceptions.ResourceNotFoundException;
import com.example.devtasks.repository.UserRepository;
import com.example.devtasks.service.UserService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    @Transactional
    public UserResponse createUser(UserRequest request) {
        if (request.getUsername() == null || request.getUsername().isBlank()) {
            throw new IllegalArgumentException("username is required");
        }
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new IllegalArgumentException("username already exists");
        }

        User u = new User();
        u.setUsername(request.getUsername());
        u.setFullName(request.getFullName());
        u.setEmail(request.getEmail());
        u.setDomain(request.getDomain());
        u.setWebHook(request.getWebHook());

        User saved = userRepository.save(u);
        return map(saved);
    }

    @Override
    @Transactional(readOnly = true)
    public UserResponse getUserById(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + id));
        return map(user);
    }

    @Override
    @Transactional(readOnly = true)
    public List<UserResponse> getAllUsers() {
        return userRepository.findAll().stream().map(this::map).collect(Collectors.toList());
    }

    @Override
    @Transactional
    public void deleteUser(Long id) {
        if (!userRepository.existsById(id)) throw new ResourceNotFoundException("User not found: " + id);
        userRepository.deleteById(id);
    }

    private UserResponse map(User u) {
        return UserResponse.builder()
                .id(u.getId())
                .username(u.getUsername())
                .fullName(u.getFullName())
                .email(u.getEmail())
                .createdAt(u.getCreatedAt())
                .domain(u.getDomain())
                .webHook(u.getWebHook())
                .build();
    }
}
