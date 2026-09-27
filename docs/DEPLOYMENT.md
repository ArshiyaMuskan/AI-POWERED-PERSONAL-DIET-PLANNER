# Deployment Guide

## Local

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Managed student-friendly architecture

### Database
Create a PostgreSQL database on a managed provider such as Supabase. Set:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
```

Install the PostgreSQL SQLAlchemy driver if needed:

```bash
pip install psycopg[binary]
```

### Backend
Deploy `backend/` as a Python web service. Set:

```text
Build: pip install -r requirements.txt
Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set all environment variables in the provider's secret/environment settings.

### Frontend
Deploy `frontend/` as a static Vite site.

Build:

```text
npm install
npm run build
```

Output directory:

```text
dist
```

Set:

```env
VITE_API_URL=https://YOUR-BACKEND-DOMAIN
```

### Storage
The included implementation is local storage for zero-cost development. For a true cloud demonstration, replace the storage adapter with S3/Supabase Storage and store only metadata in `user_files`.

## AWS/Azure/GCP mapping

AWS:
- S3 -> object storage
- RDS PostgreSQL -> managed database
- ECS/EC2/Lambda -> backend
- API Gateway/ALB -> API entry
- CloudFront -> frontend/CDN
- CloudWatch -> logs/monitoring
- Secrets Manager -> secrets

Azure:
- Blob Storage
- Azure Database for PostgreSQL
- App Service/Container Apps/Functions
- API Management
- Azure Monitor
- Key Vault

GCP:
- Cloud Storage
- Cloud SQL
- Cloud Run/Compute Engine/Cloud Functions
- API Gateway
- Cloud Monitoring/Logging
- Secret Manager
