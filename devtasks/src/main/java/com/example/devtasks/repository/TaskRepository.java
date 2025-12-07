package com.example.devtasks.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.devtasks.entity.Task;
import com.example.devtasks.entity.TaskStatus;

public interface TaskRepository extends JpaRepository<Task, Long> {
    List<Task> findByProjectId(Long projectId);
    List<Task> findByProjectIdAndStatus(Long projectId, TaskStatus status);
}
