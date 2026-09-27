# Interview Preparation

## 1. Explain your project.
I built a cloud-ready personal diet planner as a Cloud Computing course project. The frontend is React and the backend is FastAPI. I implemented JWT authentication, user profiles, database-backed diet plans, object-storage-style file handling and a rule-based AI recommendation engine. The recommendation layer can optionally call an external AI provider, but it falls back to a local engine so the project remains runnable without a paid API.

## 2. Why did you use a REST API?
It separates the frontend from backend business logic. The same backend can support a web frontend, mobile app or another client.

## 3. What is the difference between a database and object storage?
The database stores structured records such as users and diet plans. Object storage stores files such as images or exported documents and keeps metadata such as filename and path in the database.

## 4. How did you implement authentication?
Registration hashes the password. Login verifies the hash and returns a signed JWT. Protected routes decode the token and identify the current user.

## 5. How did you prevent one user from seeing another user's plans?
Every plan query includes both the requested plan ID and the authenticated user's ID. Therefore a valid token alone does not grant access to another user's records.

## 6. How does the AI component work?
The default implementation is deterministic and rule-based. It selects food examples according to dietary preference and creates a general wellness summary based on the goal. An optional external provider can be configured and the response is validated before being accepted.

## 7. What happens if the AI service fails?
The application catches provider errors and returns the local rule-based plan. This improves availability and prevents the application from depending completely on an external AI service.

## 8. How would you scale the application?
I would keep the API stateless, run multiple backend instances behind a load balancer, move from SQLite to managed PostgreSQL, use object storage for files, add caching/CDN where useful, and use queues for slow background jobs.

## 9. What security controls did you implement?
Password hashing, JWT authentication, authorization checks, CORS configuration, environment variables for secrets, input validation, upload size/type restrictions and user-scoped database queries.

## 10. How would you deploy it in a major cloud?
I could put the frontend behind a CDN, run the FastAPI service in containers, use managed PostgreSQL, object storage for files, a gateway/load balancer for API traffic, managed secrets and centralized monitoring/logging.
