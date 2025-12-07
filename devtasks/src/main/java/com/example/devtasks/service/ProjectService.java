package com.example.devtasks.service;

import java.util.List;

import com.example.devtasks.dto.ProjectRequest;
import com.example.devtasks.dto.ProjectResponse;

public interface ProjectService {
    
    ProjectResponse createProject(ProjectRequest projectRequest);
    ProjectResponse getProjectById(Long id);
    List<ProjectResponse> getAllProjects();
    ProjectResponse updateProject(Long id, ProjectRequest projectRequest);
    void deleteProject(Long id);
}
