
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
- Keycloak (Keycloak Adapter)
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


Your trainer will also ask a few questions about the application and contents in the Software Engineering Bible to ensure that your understanding is solid.