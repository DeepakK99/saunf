package com.example.devtasks.service.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.devtasks.dto.TaskRequest;
import com.example.devtasks.dto.TaskResponse;
import com.example.devtasks.entity.Project;
import com.example.devtasks.entity.Task;
import com.example.devtasks.entity.TaskStatus;
import com.example.devtasks.entity.User;
import com.example.devtasks.exceptions.ResourceNotFoundException;
import com.example.devtasks.repository.ProjectRepository;
import com.example.devtasks.repository.TaskRepository;
import com.example.devtasks.repository.UserRepository;
import com.example.devtasks.service.TaskService;



@Service
public class TaskServiceImpl implements TaskService {
    private final TaskRepository taskRepository;
    private final ProjectRepository projectRepository;
    private final UserRepository userRepository;

    public TaskServiceImpl(TaskRepository taskRepository, ProjectRepository projectRepository, UserRepository userRepository) {
        this.taskRepository = taskRepository;
        this.projectRepository = projectRepository;
        this.userRepository = userRepository;
    }

    private List<TaskResponse> mapToResponse(List<Task> tasks) {
    return tasks.stream()
        .map(this::mapToResponse)
        .collect(Collectors.toList());
    }
    private TaskResponse mapToResponse(Task task) {
    return TaskResponse.builder()
            .id(task.getId())
            .title(task.getTitle())
            .description(task.getDescription())
            .taskStatus(task.getStatus())
            .taskPriority(task.getPriority())
            .dueDate(task.getDueDate())
            .projectId(task.getProject() != null ? task.getProject().getId() : null)
            .createdById(task.getCreatedBy() !=null ? task.getCreatedBy().getId() : null)
            .assignedToId(task.getAssignedTo() != null ? task.getAssignedTo().getId() : null)
            .createdAt(task.getCreatedAt())
            .updatedAt(task.getUpdatedAt())
            .domain(task.getDomain())
            .taskType(task.getTaskType())
            .estimatedHours(task.getEstimatedHours())
            .build();
    }

    @Override
    @Transactional
    public TaskResponse createTask(Long projectId, TaskRequest request, Long creatorId) {
        Project project = projectRepository.findById(projectId).orElseThrow(() -> new ResourceNotFoundException("Project not found"));
        // get creator info
        User creator = userRepository.findById(creatorId)
        .orElseThrow(() -> new ResourceNotFoundException("Creator user not found: " + creatorId));
        
        // get assigned to inifo
        User assignee = null;
        if (request.getAssignedToId() != null) {
            assignee = userRepository.findById(request.getAssignedToId())
                .orElseThrow(() -> new ResourceNotFoundException("Assignee not found: " + request.getAssignedToId()));
        }

        Task task = new Task();
        task.setTitle(request.getTitle());
        task.setPriority(request.getPriority());
        task.setDescription(request.getDescription());
        task.setDueDate(request.getDueDate());
        task.setStatus(request.getStatus());
        task.setDomain(request.getDomain());
        task.setTaskType(request.getTaskType());
        task.setEstimatedHours(request.getEstimatedHours());
        task.setProject(project);
        task.setCreatedBy(creator);
        task.setAssignedTo(assignee);
        return mapToResponse(taskRepository.save(task));
    }

    @Override
    @Transactional(readOnly = true)
    public TaskResponse getTaskById(Long id) {
        return mapToResponse(taskRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Task not found")));
    }

    @Override
    @Transactional(readOnly = true)
    public List<TaskResponse> getTasksByProject(Long projectId) {
        return mapToResponse(taskRepository.findByProjectId(projectId));
    }

    @Override
    @Transactional(readOnly = true)
    public List<TaskResponse> getTasksByProjectAndStatus(Long projectId, TaskStatus status) {
        return mapToResponse(taskRepository.findByProjectIdAndStatus(projectId, status));
    }

    @Override
    @Transactional
    public TaskResponse updateTask(Long id, TaskRequest request) {
        Task existing = taskRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Task not found: " + id));
        User assignedTo = userRepository.findById(request.getAssignedToId()).orElseThrow(() -> new ResourceNotFoundException("User not found: " + id));
        existing.setTitle(request.getTitle());
        existing.setDescription(request.getDescription());
        existing.setStatus(request.getStatus());
        existing.setPriority(request.getPriority());
        existing.setDueDate(request.getDueDate());
        existing.setDomain(request.getDomain());
        existing.setTaskType(request.getTaskType());
        existing.setEstimatedHours(request.getEstimatedHours());
        existing.setAssignedTo(assignedTo);
        return mapToResponse(taskRepository.save(existing)); 
    }

    @Override
    @Transactional
    public void deleteTask(Long id) {
        if (!taskRepository.existsById(id)) {
            throw new RuntimeException("Task not found");
        }
        taskRepository.deleteById(id);
    }

    @Override
    @Transactional
    public TaskResponse assignTaskToUser(Long taskId, Long userId) {
        Task task = taskRepository.findById(taskId)
                .orElseThrow(() -> new ResourceNotFoundException("Task not found: " + taskId));
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + userId));
        task.setAssignedTo(user);
        Task saved = taskRepository.save(task);
        return mapToResponse(saved);
}

}
