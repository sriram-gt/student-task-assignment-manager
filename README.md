# STAM — Student Task & Assignment Manager

A full-stack web application for students to manage assignments and tasks efficiently. Built with modern technologies across the entire stack — from a React frontend to Kubernetes deployment with live monitoring.

![Dashboard](https://img.shields.io/badge/Status-Active-brightgreen)
![React](https://img.shields.io/badge/React-18-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Deployed-blue)

---

## Features

- **Authentication** — JWT-based register, login, and password reset
- **Task Management** — Create, edit, delete, and complete tasks
- **Priority Levels** — High, Medium, Low with color coding
- **Due Dates & Times** — Set specific deadlines with time picker
- **Smart Filters** — Filter by All, Pending, Completed, High Priority, Overdue
- **Sort Options** — Sort by Latest, Due Date, or Priority
- **Search** — Search tasks by title or description
- **Dashboard Stats** — Live counts for Total, Completed, Pending, Overdue
- **Completion Progress** — Visual progress bar for overall completion rate
- **Browser Notifications** — Reminders when tasks are due in 30 minutes or overdue
- **Profile Page** — Account details with completion statistics
- **Dark Glassmorphism UI** — Modern dark theme with glass-effect cards

---

## Tech Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| React 18 | UI framework |
| React Router v7 | Client-side routing |
| Axios | API communication |
| Tailwind CSS v4 | Utility styling |
| React Hot Toast | Toast notifications |
| Vite 8 | Build tool |

### Backend
| Technology | Purpose |
|-----------|---------|
| FastAPI | REST API framework |
| SQLAlchemy | ORM |
| PostgreSQL 15 | Primary database |
| Alembic | Database migrations |
| JWT (python-jose) | Authentication tokens |
| Passlib + bcrypt | Password hashing |
| Prometheus Instrumentator | Metrics exposure |

### DevOps
| Technology | Purpose |
|-----------|---------|
| Docker | Containerization |
| Docker Compose | Local orchestration |
| GitHub Actions | CI/CD pipeline |
| Kubernetes | Container orchestration |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization |

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React Frontend │────▶│  FastAPI Backend │────▶│   PostgreSQL DB  │
│   (Nginx:80)    │     │   (Port 8000)   │     │   (Port 5432)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
             ┌──────▼──────┐        ┌──────▼──────┐
             │  Prometheus  │        │   Grafana    │
             │  (Port 9090) │        │  (Port 3000) │
             └─────────────┘        └─────────────┘
```

---

## Project Structure

```
student-task-assignment-manager/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   └── task_service.py
│   │   ├── database.py
│   │   ├── config.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   └── test_tasks.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Profile.jsx
│   │   │   └── ForgotPassword.jsx
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── TaskCard.jsx
│   │   │   ├── TaskForm.jsx
│   │   │   └── SearchBar.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── App.jsx
│   ├── Dockerfile
│   └── nginx.conf
│
├── k8s/
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   └── frontend-service.yaml
│
├── monitoring/
│   └── prometheus.yml
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Docker Desktop

### 1. Clone the repository

```bash
git clone https://github.com/sriram-gt/student-task-assignment-manager.git
cd student-task-assignment-manager
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file in the backend folder:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/stam
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Create the database in PostgreSQL:

```sql
CREATE DATABASE stam;
```

Run the server:

```bash
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`

### 4. Run with Docker Compose

```bash
docker-compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

---

## CI/CD Pipeline

Every push to `main` triggers the GitHub Actions pipeline:

```
Push to main
     │
     ├──▶ Backend Tests (pytest)
     │         └── 6 tests across auth and tasks
     │
     ├──▶ Frontend Build (Vite)
     │         └── Production build verification
     │
     └──▶ Build & Push Docker Images
               ├── ghcr.io/sriram-gt/stam-backend:latest
               └── ghcr.io/sriram-gt/stam-frontend:latest
```

---

## Kubernetes Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify pods are running
kubectl get pods

# Access the frontend
kubectl port-forward service/frontend 8080:80
```

App available at `http://localhost:8080`

---

## Monitoring

Prometheus scrapes metrics from the FastAPI backend every 15 seconds.

Metrics available at `http://localhost:8000/metrics`

Import Grafana dashboard ID `18739` for FastAPI observability:
- Request rate per endpoint
- Response time percentiles
- Error rates
- Active connections

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current user |
| POST | `/auth/forgot-password` | Reset password |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create task |
| GET | `/tasks` | Get all tasks (with filters) |
| GET | `/tasks/{id}` | Get task by ID |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/tasks/search?q=` | Search tasks |
| GET | `/tasks/dashboard` | Get dashboard stats |

---

## Database Schema

```sql
users
  id            SERIAL PRIMARY KEY
  name          VARCHAR NOT NULL
  email         VARCHAR UNIQUE NOT NULL
  password_hash VARCHAR NOT NULL
  created_at    TIMESTAMP DEFAULT NOW()

tasks
  id          SERIAL PRIMARY KEY
  title       VARCHAR NOT NULL
  description VARCHAR
  priority    ENUM('low', 'medium', 'high') DEFAULT 'medium'
  due_date    TIMESTAMP
  completed   BOOLEAN DEFAULT FALSE
  user_id     INTEGER REFERENCES users(id)
  created_at  TIMESTAMP DEFAULT NOW()
```

---

## Running Tests

```bash
cd backend
venv\Scripts\activate
pytest tests/ -v
```

```
tests/test_auth.py::test_register         PASSED
tests/test_auth.py::test_login_invalid    PASSED
tests/test_auth.py::test_login_valid      PASSED
tests/test_tasks.py::test_create_task     PASSED
tests/test_tasks.py::test_get_tasks       PASSED
tests/test_tasks.py::test_get_tasks_unauthorized  PASSED
```

---

## Author

**Sriram**
B.Tech Computer Science — VIT Chennai
GitHub: [@sriram-gt](https://github.com/sriram-gt)

---

## License

This project is open source and available under the [MIT License](LICENSE).
