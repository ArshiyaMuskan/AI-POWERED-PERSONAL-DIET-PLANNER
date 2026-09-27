# Architecture and Cloud Mapping

## Layers

1. Client: React browser application.
2. Application: FastAPI REST API.
3. Authentication: JWT access tokens.
4. AI: local rule engine with optional external-provider fallback.
5. Data: SQL database.
6. Object storage: local simulation with a clean adapter boundary for cloud storage.
7. Deployment: container-ready.

## Cloud Concepts

| Concept | Project location |
|---|---|
| SaaS | The finished browser application behaves as a web service |
| PaaS | A managed host can run the FastAPI and React services |
| IaaS | AWS EC2/Azure VM/GCP Compute Engine can host the containers |
| Cloud DB | Replace local SQLite with Supabase/PostgreSQL |
| Object storage | Replace local storage service with S3/Supabase Storage |
| REST API | FastAPI endpoints |
| Authentication | JWT |
| Authorization | Every user-scoped query filters by authenticated user ID |
| Serverless | Optional future migration of API functions |
| Scalability | Stateless API + managed DB + object storage |
| Load balancing | Put multiple backend instances behind an ALB/API gateway |
| API gateway | Can front the backend in AWS/Azure/GCP |
| Secrets | Environment variables / managed secret stores |
| Logging | Container/platform logs; add structured logging for production |
| Monitoring | Platform health checks + future CloudWatch/Azure Monitor/Cloud Monitoring |
| CI/CD | GitHub Actions can test and build on every push |

## Data Flow

```text
User
  |
  v
React
  |
  | HTTPS JSON
  v
FastAPI
  |
  +--> JWT verification
  |
  +--> User profile
  |
  +--> AI engine
  |      |
  |      +--> external AI if configured
  |      |
  |      +--> local fallback
  |
  +--> SQL database
  |
  +--> Object storage
  |
  v
Dashboard
```
