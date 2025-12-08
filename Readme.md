# 🚀 AI-Powered Task Classification & Auto-Assignment Backend

A **backend-only, Jira-like task management system** that automatically **classifies, prioritizes, and assigns tasks using a local LLM**. Built with a **distributed, asynchronous microservice architecture** using Spring Boot, FastAPI, Celery, Redis, and Qdrant for semantic search.

This project demonstrates **AI-driven automation**, **event-driven design**, and **scalable async processing** in a real-world backend system.

---

## 📌 Features

* ✅ **Project & Task CRUD APIs**
* 🤖 **Automatic task classification** (domain, priority, time estimate) using a **local LLM**
* 👥 **Workload-based auto-assignment**
* ⚡ **Asynchronous background processing** with Celery + Redis
* 🔍 **Semantic task search** using **Qdrant + MiniLM embeddings**
* 🔔 **Event-driven Discord notifications**
* 🗄️ **Database migrations with Flyway**
* 🐳 **Fully containerized using Docker & Docker Compose**

---

## 🧱 Tech Stack

| Layer                   | Technology              |
| ----------------------- | ----------------------- |
| API & Business Logic    | Spring Boot             |
| AI & Background Workers | FastAPI, Celery         |
| Message Broker          | Redis                   |
| Relational Database     | MySQL                   |
| LLM                     | Ollama (Gemma3)         |
| Embeddings              | all-MiniLM              |
| Vector Database         | Qdrant                  |
| Migrations              | Flyway                  |
| Deployment              | Docker & Docker Compose |

---

## 🏗️ System Architecture (High Level)

* **Spring Boot** → Core APIs, business logic, database ownership
* **FastAPI** → AI pipelines & async workers
* **Redis** → Message broker for Celery
* **Qdrant** → Semantic vector search
* **Discord Webhooks** → Notifications

---

## 🔄 Task Processing Flow

1. User creates a task via **Spring Boot API**
2. Task is stored in **MySQL**
3. Spring Boot calls **FastAPI** to trigger background processing
4. **Classification Worker**:

   * Calls the LLM via **Ollama**
   * Updates classification in DB
   * Pushes:

     * Notification job
     * Auto-assignment job
5. **Auto-Assignment Worker**:

   * Selects user with **minimum workload**
   * Updates task assignment in DB
   * Pushes notification job
6. **Notification Worker**:

   * Sends **Discord notifications** with rate limiting
7. **Embedding Worker**:

   * Task is **embedded and stored in Qdrant** for semantic search

---

## 🛡️ Failure Handling & Reliability

* ⏳ Timeouts on LLM calls
* 🔁 Celery **soft & hard time limits**
* 🔄 **Automatic retries** on transient failures
* 🧯 **Fallback default classification values**
* ✅ **Idempotent DB updates** for safe retries

---

## 🧪 Local Setup

### Prerequisites

* Docker
* Docker Compose

### Start All Services

```bash
docker-compose up --build
```

### This starts:

* Spring Boot API
* FastAPI AI Service
* Redis
* MySQL
* Qdrant
* Celery Workers

\* **Important:** Ollama must be **installed and running separately** on your machine.  
Make sure to **pull and run the required LLM and embedding models** before starting the system.


---

## 🚧 Future Enhancements

* 🔐 **Authentication & Authorization**
  Secure user access with login, JWT-based authentication, and **role-based access control (RBAC)**.

* 🖥️ **Frontend Application**
  A full-featured web UI for project and task management with real-time updates.

* 💬 **Task Comments & Activity Logs**
  Enable threaded comments on tasks with a complete activity history for better collaboration and traceability.

* ⏰ **Automated Due Date Monitoring**
  Periodic background checks for:

  * Overdue tasks
  * Unassigned tasks
    with automatic reminders and alerts.

* ⏱️ **Scheduled Jobs with Celery Beat**
  Use **Celery Beat for reliable periodic job execution** to:

  * Send recurring notifications
  * Perform health checks
  * Trigger maintenance workflows

* 🏛️ **Single Database Ownership via Spring Boot**  

  * Migrate all direct database access from Python services to **Spring Boot as the sole DB owner**, enforcing strict service boundaries and improving data integrity, security, and long-term maintainability.


---

## 📂 Project Use Cases

* AI-powered task triage
* Automated resource allocation
* Smart backlog management
* Semantic task discovery
* Event-driven enterprise workflows

---

## 🧑‍💻 Author

Built by **Deepak Kumar Sahu**
Senior Software Engineer

---
