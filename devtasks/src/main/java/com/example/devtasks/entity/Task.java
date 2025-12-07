package com.example.devtasks.entity;

import java.time.LocalDate;
import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonIgnore;

import jakarta.persistence.*;

@Entity
@Table(name = "tasks")
public class Task {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TaskStatus status;

    @Enumerated(EnumType.STRING)
    private TaskPriority priority;

    private LocalDate due_date;

    @Enumerated(EnumType.STRING)
    private Domain domain;

    @Enumerated(EnumType.STRING)
    private TaskType task_type;

    private int estimated_hours;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JsonIgnore
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

    @Column(nullable = false, updatable = false)
    private LocalDateTime created_at;

    private LocalDateTime updated_at;

    @PrePersist
    public void prePersist() {
        this.created_at = LocalDateTime.now();
        this.updated_at = this.created_at;
        if (this.status == null) {
            this.status = TaskStatus.TODO;
        }
    }

    @PostPersist
    public void preUpdate() {
        this.updated_at = LocalDateTime.now();
    }

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "created_by", nullable = false)
    private User created_by;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "assigned_to")
    private User assigned_to;

    public Task () {}

    public Long getId() {
    return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public TaskStatus getStatus() {
        return status;
    }

    public void setStatus(TaskStatus status) {
        this.status = status;
    }

    public TaskPriority getPriority() {
        return priority;
    }

    public void setPriority(TaskPriority priority) {
        this.priority = priority;
    }

    public LocalDate getDueDate() {
        return due_date;
    }

    public void setDueDate(LocalDate due_date) {
        this.due_date = due_date;
    }

    public Domain getDomain() {
        return domain;
    }

    public void setDomain(Domain domain) {
        this.domain = domain;
    }

    public TaskType getTaskType() {
        return task_type;
    }

    public void setTaskType(TaskType task_type) {
        this.task_type = task_type;
    }

    public int getEstimatedHours() {
        return estimated_hours;
    }

    public void setEstimatedHours(int estimated_hours) {
        this.estimated_hours = estimated_hours;
    }

    public Project getProject() {
        return project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public LocalDateTime getCreatedAt() {
        return created_at;
    }

    public void setCreatedAt(LocalDateTime created_at) {
        this.created_at = created_at;
    }

    public LocalDateTime getUpdatedAt() {
        return updated_at;
    }

    public void setUpdatedAt(LocalDateTime updated_at) {
        this.updated_at = updated_at;
    }

    public User getCreatedBy() {
        return created_by;
    }

    public void setCreatedBy(User created_by) {
        this.created_by = created_by;
    }

    public User getAssignedTo() {
        return assigned_to;
    }

    public void setAssignedTo(User assigned_to) {
        this.assigned_to = assigned_to;
    }


}


