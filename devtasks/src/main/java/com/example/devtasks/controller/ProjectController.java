package com.example.devtasks.controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.devtasks.dto.ProjectRequest;
import com.example.devtasks.dto.ProjectResponse;
import com.example.devtasks.service.ProjectService;

import jakarta.validation.Valid;



@RestController
@RequestMapping("/api/projects")
public class ProjectController {
    private final ProjectService projectService;
    public ProjectController(ProjectService projectService) {
        this.projectService = projectService;
    }
    @PostMapping  
    public ResponseEntity<ProjectResponse> createProject(@Valid @RequestBody ProjectRequest request) {
        return ResponseEntity
        .status(HttpStatus.CREATED)
        .body(projectService.createProject(request));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ProjectResponse> getProjectById(@PathVariable Long id) {
        return ResponseEntity
        .ok(projectService.getProjectById(id));
    }

    @GetMapping
    public ResponseEntity<List<ProjectResponse>> getAllProjects() {
        return ResponseEntity
        .ok(projectService.getAllProjects());
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<ProjectResponse> updateProject(@PathVariable Long id, @Valid @RequestBody ProjectRequest request) {
        return ResponseEntity
        .ok(projectService.updateProject(id, request));
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProject(@PathVariable Long id) {
        projectService.deleteProject(id);
        return ResponseEntity.noContent().build();
    }
}
