package com.example.devtasks.controller;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import com.example.devtasks.dto.TaskRequest;
import com.example.devtasks.dto.TaskResponse;
import com.example.devtasks.entity.TaskStatus;
import com.example.devtasks.service.TaskService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api")
public class TaskController {
    
    private final TaskService taskService;

    @Value("${python.service.url}")
    private String pythonUrl; 

    public TaskController(TaskService taskService) {
        this.taskService = taskService;
    }

    @PostMapping("/projects/{projectId}/tasks")
    public ResponseEntity<TaskResponse> createTask(@PathVariable Long projectId, @RequestParam Long creatorId, @Valid @RequestBody TaskRequest request) {
        TaskResponse res = taskService.createTask(projectId, request, creatorId);
        triggerPythonPipeline(res.getId());
        return ResponseEntity.status(HttpStatus.CREATED).body(res);
    }

    @GetMapping("/tasks/{taskId}")
    public ResponseEntity<TaskResponse> getTaskById(@PathVariable Long taskId) {
        return ResponseEntity.ok(taskService.getTaskById(taskId));
    }

    @GetMapping("/projects/{projectId}/tasks")
    public ResponseEntity<List<TaskResponse>> getTasks(@PathVariable Long projectId, @RequestParam(required = false) TaskStatus status) {
        if (status!=null) {
            return ResponseEntity.ok(taskService.getTasksByProjectAndStatus(projectId, status));
        }
        return ResponseEntity.ok(taskService.getTasksByProject(projectId));
    }

    @PutMapping("/tasks/{taskId}")
    public ResponseEntity<TaskResponse> updateTask(@PathVariable Long taskId, @Valid @RequestBody TaskRequest request) {
        return ResponseEntity.ok(taskService.updateTask(taskId, request));
    }

    @DeleteMapping("/tasks/{taskId}")
    public ResponseEntity<Void> deleteTask(@PathVariable Long taskId) {
        taskService.deleteTask(taskId);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/tasks/{taskId}/assign/{userId}")
    public ResponseEntity<TaskResponse> assignTask(@PathVariable Long taskId, @PathVariable Long userId) {
        return ResponseEntity.ok(taskService.assignTaskToUser(taskId, userId));
    }

    private void triggerPythonPipeline(Long taskId) {
        RestTemplate restTemplate = new RestTemplate();


        Map<String, Object> payload = Map.of("task_id", taskId);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, Object>> request = new HttpEntity<>(payload, headers);

        try {
            ResponseEntity<String> response = restTemplate.postForEntity(pythonUrl, request, String.class);
            System.out.println("Python pipeline triggered, status: " + response.getStatusCode());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
