
# Report/Presentation Assignment

## The goal of this assignemnt is to provide experience on understanding documentation, working on unfamiliar * created code, familiarising yourself with production-ready code. 

You are to clone and tinker with the given template (architecture-sample-app) and read through the relevant sections of the Software Engineering Bible. You are also encouraged to do further additional research (e.g what is S3/AWS) to better understand how exactly the application functions.

Architecture-Sample-App: https://github.com/Ronandt/Architecture-Sample-App
Software Engineering Bible: https://docs.google.com/document/d/1GKBNkuOWUwuF6SQbBu9atvg8SUxaNDDEaDFgCV9PjDY/edit?tab=t.0

### Architecture-Sample-App
In order to run this application, you will need to know how to setup Keycloak and be able to run the frontend and the backend. Refer to template_setup_backend.md and template_setup_backend.md. 

## Recommended Contents

0. Brief intro — what is the template, what problem does it solve, and who would use it
1. Architecture diagram — the major components (frontend, backend, Keycloak, S3/Minio, PostgreSQL) and how they connect to each other
2. Concepts from the stack not taught in training — explain what each unfamiliar piece is and the role it plays (see the list below for guidance)
3. Live demo — run the template locally and show the login flow, a protected route, and an admin-only action
4. Code walkthrough — trace one request through the system: from the frontend, through the backend, through auth, to the database and back
5. How you would extend it — pick one feature and explain concretely how you would add it to the template

*Things that was not taught in the training/Explicitely not taught
- Code architecture (How to architecture your app Services, repository pattern, guard patterns , error handling) (IMPORTANT)
- File organisation
- Middleware
- Keycloak + (Keycloak Adapter [python-keycloak])
- S3/Boto/Minio + (Keycloak Adapter)
- SSL
- Env Management & Settings 
- Postgres3 Database
- Dependency Injection
- Logging
- Unit Testing
- Infrastructure & Deployment(if you really want to do this lol
)
- Extending the architecture
-Difference in production and development (no inspect etc)

For example for code architecture you can explain:
- What is the difference between a repository and a service, and why are they kept separate?
- How are exceptions raised in a service and where do they get caught and turned into HTTP responses?
- How is dependency injection used — what does FastAPI's `Depends()` actually do at runtime?
- Why is the repository pattern useful when you want to swap out the database later?

Or for authentication you can explain:
- How is the JWT token passed from the frontend to the backend on each request?
- Which part of the code checks the roles or identity of the user, and how does it do it?
- How are tokens refreshed — what happens when an access token expires?
- What is the difference between a realm, a client, a group, and a role in Keycloak?
- What does the Keycloak adapter (python-keycloak) do 

Or for file storage (S3/Minio) you can explain:
- What is object storage 
- Image retireve flow etc
- What is a presigned URL and why would you use one instead of routing the file through the backend?
- What does Boto3 do and how does Minio fit in as a local alternative to AWS S3?
- Where in the codebase does a file upload get handled — what goes to S3 and what gets stored in the database?

Or for environment and settings you can explain:
- Why should secrets never be hardcoded in the codebase — what is the actual risk?
- How does the template load config from environment variables, and what library manages this?
- What is the difference between a `.env` file used locally and how secrets are managed in a real deployed environment?

Or for logging you can explain:
- What gets logged and at what level (DEBUG, INFO, WARNING, ERROR)?
- How would you use the logs to trace what happened during a failed request?
- What is structured logging and why is it easier to search through than plain text output?

Or for the database (PostgreSQL vs SQLite) you can explain:
- What practical differences does a developer notice when switching from SQLite to PostgreSQL?
- What does the template do differently in its database setup compared to the SQLite version in the tutorials?

Or for prod vs development you can explain:
- Why can't you inspect or debug a production app the same way you do locally?
- What changes between a development config and a production config (CORS, debug mode, secret keys, HTTPS)?
- What does it mean for an app to be stateless and why does it matter for deployment?


Your trainer will also ask a few questions about the application and contents in the Software Engineering Bible to ensure that your understanding is solid.