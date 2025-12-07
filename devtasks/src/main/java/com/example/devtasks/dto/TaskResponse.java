package com.example.devtasks.dto;

import java.time.LocalDate;
import java.time.LocalDateTime;

import com.example.devtasks.entity.Domain;
import com.example.devtasks.entity.TaskPriority;
import com.example.devtasks.entity.TaskStatus;
import com.example.devtasks.entity.TaskType;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class TaskResponse {
    private Long id;
    private String title;
    private String description;
    private TaskStatus taskStatus;
    private TaskPriority taskPriority;
    private LocalDate dueDate;
    private Long projectId;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private Long createdById;
    private Long assignedToId;
    private Domain domain;
    private TaskType taskType;
    private int estimatedHours;

}
