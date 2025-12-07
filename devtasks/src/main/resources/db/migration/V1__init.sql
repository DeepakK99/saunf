CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    email VARCHAR(255) NOT NULL UNIQUE,
    discord_webhook VARCHAR(255),
    domain VARCHAR(255),
    created_at DATETIME,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE projects (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at DATETIME,
    updated_at DATETIME
);

CREATE TABLE tasks (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    domain VARCHAR(255),
    status VARCHAR(255),
    task_type VARCHAR(50),
    priority VARCHAR(255),
    estimated_hours INT,
    created_by BIGINT,
    assigned_to BIGINT,
    project_id BIGINT,
    created_at DATETIME,
    updated_at DATETIME,
    due_date DATETIME,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_created_by (created_by),
    INDEX idx_assigned_to (assigned_to),
    INDEX idx_project_id (project_id)
);

CREATE TABLE notifications (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    recipient VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(255) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stages (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_id BIGINT NOT NULL,
    stage VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_task_id (task_id)
);
