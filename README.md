# Travel Planner API

A REST API built with Django and Django REST Framework for planning visits to artworks and exhibitions from the [Art Institute of Chicago](https://www.artic.edu/). Users can create projects, add places (artworks) to them, and track their visit progress.

---

## Tech Stack

- **Python 3** / **Django**
- **Django REST Framework**
- **Simple JWT** — authentication via JWT tokens
- **drf-spectacular** — auto-generated OpenAPI schema (Swagger / ReDoc)
- **httpx** — async-friendly HTTP client for external API calls
- **django-environ** — environment variable management
- **SQLite** — default database (easily swappable)
- **django-debug-toolbar** — development debugging
- **Gunicorn** — WSGI server for production
- **Docker** / **Docker Compose** — containerized deployment

---

## Project Structure

```
.
├── apps/
│   ├── auth/               # User registration, login, logout
│   │   ├── models.py       # Custom User model
│   │   ├── serializers.py  # Register / Login / Refresh serializers
│   │   ├── validators.py   # Email & password validators
│   │   ├── views.py        # Registration, Login, Logout views
│   │   └── urls.py
│   └── planner/            # Projects and places management
│       ├── models.py       # Project, ProjectPlace models
│       ├── serializers.py  # CRUD serializers for projects and places
│       ├── utils.py        # Business logic, external API validation
│       ├── views.py        # API views
│       └── urls.py
├── config/
│   ├── settings.py
│   └── urls.py
├── docker/
│   └── entrypoint.sh       # Migrations, collectstatic, superuser, Gunicorn startup
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env.dev` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
API_BASE_URL=https://api.artic.edu/api/v1/artworks
CACHE_TTL=3600
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

---

## API Documentation

Interactive docs are available after starting the server:

| Interface | URL |
|-----------|-----|
| Swagger UI | `http://127.0.0.1:8000/api/docs/` |
| ReDoc | `http://127.0.0.1:8000/api/redoc/` |
| OpenAPI Schema | `http://127.0.0.1:8000/api/schema/` |

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | Register a new user |
| `POST` | `/api/auth/login/` | Log in and receive JWT tokens |
| `POST` | `/api/auth/token/refresh/` | Refresh access token |
| `POST` | `/api/auth/logout/` | Log out the current user |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/planner/projects/` | List all projects for the current user |
| `POST` | `/api/planner/projects/` | Create a new project |
| `GET` | `/api/planner/projects/<id>/` | Retrieve a project |
| `PUT` | `/api/planner/projects/<id>/` | Fully update a project |
| `PATCH` | `/api/planner/projects/<id>/` | Partially update a project |
| `DELETE` | `/api/planner/projects/<id>/` | Delete a project (only if no visited places) |

### Project Places

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/planner/projects/<id>/places/` | List all places in a project |
| `POST` | `/api/planner/projects/<id>/places/` | Add a place to a project |
| `GET` | `/api/planner/projects/<id>/places/<place_id>/` | Retrieve a specific place |
| `PUT` | `/api/planner/projects/<id>/places/<place_id>/` | Fully update a place |
| `PATCH` | `/api/planner/projects/<id>/places/<place_id>/` | Partially update a place |

---

## Business Rules

- A project must contain **at least 1** and no more than **10 places**.
- Each place is identified by an `external_id` validated against the Art Institute of Chicago API.
- The same place cannot be added to the same project more than once.
- A project is automatically marked as **completed** when all of its places are marked as visited.
- A project **cannot be deleted** if it contains any visited places.

---

## Authentication

The API uses **JWT (JSON Web Token)** authentication via `djangorestframework-simplejwt`.

Include the access token in the `Authorization` header for all protected endpoints:

```
Authorization: Bearer <access_token>
```

---

## Validation

### Email
- Must follow standard email format.
- Cannot start or end with a dot, or contain consecutive dots.
- Only letters, digits, and the characters `. _ - +` are allowed before the `@`.

### Password
- Minimum 8 characters.
- Must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.

---

## Admin Panel

Available at `http://127.0.0.1:8000/admin/` after creating a superuser.

Registered models: `User`, `Project`, `ProjectPlace`.

---

## Docker Deployment

The project includes a production-ready Docker setup using **Gunicorn** as the WSGI server.

### Build and run

```bash
docker compose up --build
```

### Environment variables for production

Create a `.env.prod` file in the project root (used by `docker-compose.yml`):

```env
SECRET_KEY=your-secret-key
DEBUG=False
API_BASE_URL=https://api.artic.edu/api/v1/artworks
CACHE_TTL=3600

# Optional: auto-create superuser on first run
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=StrongPassword123!
```

### What the entrypoint does on startup

1. Runs `python manage.py migrate`
2. Runs `python manage.py collectstatic`
3. Creates a superuser if `DJANGO_SUPERUSER_*` variables are set and the user doesn't already exist
4. Starts Gunicorn on port `8000` (overridable via `PORT` env variable)

### Docker image details

- Base image: `python:3.11-slim`
- Runs as a non-root user (`app`, UID/GID 1000)
- Static files served via a shared `static_volume`
- Network: `planner_network`
