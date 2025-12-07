package com.example.devtasks.dto;

import java.time.LocalDate;

import com.example.devtasks.entity.Domain;
import com.example.devtasks.entity.TaskPriority;
import com.example.devtasks.entity.TaskStatus;
import com.example.devtasks.entity.TaskType;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class TaskRequest {
    @NotBlank(message="Title is required")
    private String title;
    private String description;
    @NotNull(message = "Status is required")
    private TaskStatus status;
    private TaskPriority priority;
    private LocalDate dueDate;
    private Long assignedToId;
    private Domain domain;
    private TaskType taskType;
    private int estimatedHours;

}
