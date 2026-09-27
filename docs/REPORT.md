# Project Report

## Abstract

The AI-Powered Personal Diet Planner with Cloud Storage is an educational cloud computing application that demonstrates authentication, REST APIs, database persistence, object storage, personalized recommendation logic and cloud deployment architecture. The system accepts synthetic user profile data and generates general wellness meal-plan examples.

## Introduction

Traditional desktop-only applications can make centralized access, persistence and multi-device use difficult. A cloud-oriented architecture separates presentation, application logic, data and storage so that the system can be deployed and scaled independently.

## Problem Statement

Students need a practical application through which cloud concepts can be demonstrated rather than discussed only theoretically.

## Objectives

- Build a full-stack cloud-ready application.
- Implement authentication and authorization.
- Store user-specific structured data.
- Demonstrate object storage.
- Implement AI-style personalized recommendations.
- Demonstrate testing and deployment.

## Existing System

A simple local diet application may store everything in one device and lack centralized authentication, scalable storage and API separation.

## Proposed System

The proposed system uses a browser frontend, FastAPI REST backend, authenticated API calls, relational data storage, object storage and a recommendation engine.

## Cloud Computing Concepts

The architecture demonstrates SaaS, PaaS and IaaS mappings, cloud database, object storage, API design, security, scalability, deployment, monitoring and CI/CD.

## Technology Stack

React, Vite, FastAPI, Python, SQLAlchemy, SQLite/PostgreSQL, JWT, bcrypt and object-storage abstraction.

## System Architecture

See `docs/ARCHITECTURE.md`.

## Database Design

Users own many diet plans and many uploaded files. Foreign keys connect plans/files to the authenticated user.

## AI Recommendation Logic

The local engine selects meal examples according to dietary preference and uses the goal to produce an educational explanatory note. An optional external AI provider can be configured; failures fall back to the local engine.

## Authentication

Passwords are hashed. Login returns a JWT. Protected endpoints extract the user ID from the token and scope database queries to that user.

## API Design

FastAPI provides documented REST endpoints and automatic OpenAPI documentation.

## Testing

Automated pytest tests cover authentication, authorization, profile management, plan generation and health checks.

## Cloud Deployment

The application can be deployed using managed frontend/backend services and a managed PostgreSQL/object-storage provider. It is also container-ready.

## Security

The project demonstrates password hashing, JWT, CORS configuration, input validation, upload limits, ownership checks and environment variables.

## Scalability

A stateless API can be replicated behind a load balancer. Managed PostgreSQL handles persistence while object storage handles files. CDN, caching and asynchronous queues can be added as traffic increases.

## Results

The completed application provides a working demonstration of a cloud-oriented full-stack workflow using synthetic data.

## Limitations

- The default local storage is not durable distributed object storage.
- The local recommendation engine is not a clinical nutrition system.
- Production-grade monitoring, rate limiting and malware scanning require additional infrastructure.

## Future Scope

- Real cloud object storage adapter
- Managed PostgreSQL deployment
- Serverless API option
- CDN
- Background task queue
- Observability dashboard
- Stronger file security
- CI/CD pipeline
- Optional LLM provider with strict output validation

## Conclusion

The project demonstrates how cloud computing concepts can be combined into a practical, portfolio-ready web application while keeping a free local development path.
