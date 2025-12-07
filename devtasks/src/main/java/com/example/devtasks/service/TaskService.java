package com.example.devtasks.service;

import java.util.List;

import com.example.devtasks.dto.TaskRequest;
import com.example.devtasks.dto.TaskResponse;
import com.example.devtasks.entity.TaskStatus;

public interface TaskService {
    TaskResponse createTask(Long projectId, TaskRequest taskRequest, Long creatorId);
    TaskResponse getTaskById(Long id);
    List<TaskResponse> getTasksByProject(Long projectId);
    List<TaskResponse> getTasksByProjectAndStatus(Long projectId, TaskStatus status);
    TaskResponse updateTask(Long id, TaskRequest taskRequest);
    TaskResponse assignTaskToUser(Long taskId, Long userId);
    void deleteTask(Long id);
}
