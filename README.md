# Quick Start Guide

Get the application running in under 5 minutes.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

## 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Copy environment template
cp src/.env.template src/.env
```

## 2. Start the Application

```bash
make all
```

This single command will:
- Build the Docker images
- Start PostgreSQL
- Start the FastAPI application

## 3. Access the application
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Adminer (DB UI): http://localhost:7080

## 4. Stop the Application

```bash
# Stop all services
make all-down
```

## Common Commands

| Command | Description |
|---------|-------------|
| `make all` | Start all services |
| `make all-down` | Stop all services |
| `make app-logs` | View application logs |
| `make app-shell` | Access app container shell |

For more commands, see the [Development Guide](./development.md#available-make-commands).
