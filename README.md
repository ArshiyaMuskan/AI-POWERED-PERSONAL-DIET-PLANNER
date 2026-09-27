# AI-Powered Personal Diet Planner with Cloud Storage

A beginner-friendly, industry-oriented Cloud Computing course project combining a React frontend, FastAPI REST backend, JWT authentication, database persistence, cloud-storage-ready file handling, and an AI-style rule-based recommendation engine with an optional external AI provider.

> **Important:** This project uses synthetic/demo data only. Generated meal plans are educational/general-wellness examples and are **not medical or clinical nutrition advice**.

## Architecture

```text
Browser
   |
   v
React + Vite Frontend
   |
   | REST/JSON + JWT
   v
FastAPI Backend
   |
   +--> JWT Authentication
   |
   +--> Rule-based AI / optional AI provider
   |
   +--> SQLite (local) / PostgreSQL-compatible deployment
   |
   +--> Local object-storage simulation / Supabase Storage adapter
   |
   v
Dashboard
```

## Features

- Registration, login, logout
- JWT-based authentication
- Protected user dashboard
- User profile management
- Vegetarian, vegan and general/non-vegetarian preferences
- Balanced, weight-management demo and fitness-oriented demo goals
- Rule-based personalized meal-plan generation
- Optional external AI provider with safe local fallback
- Saved diet plans
- File upload/download/delete
- Per-user authorization checks
- SQLite local database
- Storage abstraction that can use local files or Supabase Storage
- REST API documentation through FastAPI
- Automated backend tests
- CORS configuration
- Environment-based secrets
- Docker support
- GitHub-friendly documentation

## Technology Stack

- Frontend: React, Vite, JavaScript
- Backend: Python, FastAPI, SQLAlchemy, Pydantic
- Authentication: JWT + bcrypt password hashing
- Local database: SQLite
- Cloud database option: PostgreSQL/Supabase
- Storage: local `storage/` simulation or Supabase Storage
- AI: deterministic rule-based engine; optional external provider
- Testing: pytest
- Deployment: Docker, Render/Railway/Fly.io-style platforms, Vercel/Netlify for frontend, Supabase for managed DB/storage

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Backend:
`http://127.0.0.1:8000`

Swagger:
`http://127.0.0.1:8000/docs`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:
`http://localhost:5173`

### 3. Demo workflow

1. Register a synthetic demo account.
2. Log in.
3. Complete the profile.
4. Generate a plan.
5. Save the plan.
6. Upload a small food/meal image.
7. View saved plans and files.
8. Log out and log back in.

## Environment Variables

See `backend/.env.example` and `frontend/.env.example`.

Never commit real API keys, passwords, JWT secrets, cloud credentials, or service-role keys.

## Cloud Deployment Strategy

### Student-friendly

- Frontend -> Vercel/Netlify
- Backend -> Render/Railway/Fly.io-style Python service
- Database -> Supabase PostgreSQL
- Storage -> Supabase Storage
- Optional AI provider -> environment variable
- GitHub -> source control and CI

### AWS-style architecture

```text
CloudFront/CDN
      |
      v
S3 static frontend
      |
      v
API Gateway / ALB
      |
      v
FastAPI containers / ECS / EC2
      |
   +--+---------+
   |            |
   v            v
RDS PostgreSQL  S3 Object Storage
      |
      v
CloudWatch Logs/Monitoring
```

## Security Notes

- Passwords are hashed with bcrypt.
- JWT secret is loaded from environment variables.
- CORS is configurable.
- Uploaded files are validated by size and extension.
- API routes require a valid JWT where appropriate.
- Database queries are scoped to the authenticated user.
- Do not use this project with real medical data.
- For production, add managed secrets, HTTPS, rate limiting, audit logging, backups, stronger file scanning and a production object-storage policy.

## API Summary

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login |
| GET | `/api/profile` | Get profile |
| PUT | `/api/profile` | Update profile |
| POST | `/api/plans/generate` | Generate and save plan |
| GET | `/api/plans` | List current user's plans |
| GET | `/api/plans/{id}` | Get one plan |
| DELETE | `/api/plans/{id}` | Delete own plan |
| POST | `/api/files` | Upload file |
| GET | `/api/files` | List own files |
| GET | `/api/files/{id}/download` | Download own file |
| DELETE | `/api/files/{id}` | Delete own file |
| GET | `/api/health` | Health check |

## Testing

```bash
cd backend
pytest -q
```

## GitHub Commit Strategy

Suggested incremental commits:

```text
Initialize cloud diet planner project
Create cloud application architecture
Add user authentication
Implement user profile management
Add AI diet recommendation engine
Implement diet plan REST API
Integrate database layer
Add cloud object storage abstraction
Build user dashboard
Add AI fallback mechanism
Add application tests
Add deployment configuration
Complete README and documentation
```

## Disclaimer

This application is an educational Cloud Computing project. Its generated meal plans are general wellness examples based on demo preferences. They are not medical advice, diagnosis, treatment, or a substitute for a qualified healthcare professional or registered dietitian.


## Supabase Storage Mode

The backend includes a lightweight Supabase Storage adapter using the Supabase Storage HTTP API, so no SDK credential is hardcoded.

Set:

```env
STORAGE_BACKEND=supabase
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVER_ONLY_SERVICE_ROLE_KEY
SUPABASE_BUCKET=meal-files
```

**Never expose `SUPABASE_SERVICE_ROLE_KEY` to the React frontend.** Keep it only in the backend environment.

For a fully local demo, leave `STORAGE_BACKEND=local`.
