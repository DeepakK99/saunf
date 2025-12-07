package com.example.devtasks.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.devtasks.entity.Project;

@Repository
public interface ProjectRepository extends JpaRepository<Project, Long> {

    
}
