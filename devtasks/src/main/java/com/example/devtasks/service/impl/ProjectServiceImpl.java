package com.example.devtasks.service.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.example.devtasks.dto.ProjectRequest;
import com.example.devtasks.dto.ProjectResponse;
import com.example.devtasks.entity.Project;
import com.example.devtasks.exceptions.ResourceNotFoundException;
import com.example.devtasks.repository.ProjectRepository;
import com.example.devtasks.service.ProjectService;

@Service
public class ProjectServiceImpl implements ProjectService{
    private final ProjectRepository projectRepository;

    public ProjectServiceImpl(ProjectRepository projectRepository) {
        this.projectRepository = projectRepository;
    }
    private List<ProjectResponse> mapToResponse(List<Project> projects) {
    return projects.stream()
        .map(this::mapToResponse)
        .collect(Collectors.toList());
    }
    private ProjectResponse mapToResponse(Project project) {
    return ProjectResponse.builder()
            .id(project.getId())
            .name(project.getName())
            .description(project.getDescription())
            .createdAt(project.getCreatedAt())
            .updatedAt(project.getUpdatedAt())
            .build();
    }


    @Override
    public ProjectResponse createProject(ProjectRequest request) {
        Project project = new Project();
        project.setName(request.getName());
        project.setDescription(request.getDescription());
        Project saved = projectRepository.save(project);
        return mapToResponse(saved);
    }

    @Override
    public ProjectResponse getProjectById(Long id) {
        Project project = projectRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Project not found with id:" + id));
        return mapToResponse(project);
    }

    @Override
    public List<ProjectResponse> getAllProjects() {
        List<Project> projects = projectRepository.findAll();
        
        return mapToResponse(projects);
    }

    @Override
    public ProjectResponse updateProject(Long id, ProjectRequest request) {
        Project existing = projectRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Project not found with id:" + id));
        existing.setName(request.getName());
        existing.setDescription(request.getDescription());

        return mapToResponse(projectRepository.save(existing));
    }

    @Override
    public void deleteProject(Long id) {
        if (!projectRepository.existsById(id)) {
            throw new RuntimeException("Project not found with id:" + id);
        }
        projectRepository.deleteById(id);
    }
}
