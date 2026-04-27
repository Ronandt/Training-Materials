
# Report/Presentation Assignment

## The goal of this assignemnt is to provide experience on understanding documentation, working on unfamiliar * created code, familiarising yourself with production-ready code. 

You are to clone and tinker with the given template (architecture-sample-app) and read through the relevant sections of the Software Engineering Bible. You are also encouraged to do further additional research (e.g what is S3/AWS) to better understand how exactly the application functions.

Architecture-Sample-App: https://github.com/Ronandt/Architecture-Sample-App
Software Engineering Bible: https://docs.google.com/document/d/1GKBNkuOWUwuF6SQbBu9atvg8SUxaNDDEaDFgCV9PjDY/edit?tab=t.0

### Architecture-Sample-App
In order to run this application, you will need to know how to setup Keycloak and be able to run the frontend and the backend. Refer to template_setup_backend.md and template_setup_backend.md. 

## Recommended Contents

**Part 1 — What you built (your work)**

0. Brief intro — what the SWEGP project is, what it does, and the stack you chose
1. Data model walkthrough — your SQLAlchemy models, relationships, and how Alembic managed the schema
2. API tour — a Pydantic schema you are proud of, a route that does something interesting, any validation or error handling you added
3. Frontend walkthrough — your React Router structure, a `useQuery` / `useMutation` flow end-to-end, and one shadcn component you used well
4. Live demo — show the core user flow: create something, view it, update it, delete it
5. What you would do differently or add next

**Part 2 — The architecture template (high level)**

6. What problem does the template solve that your project does not yet address?
7. Architecture diagram — what the major pieces are (frontend, backend, Keycloak, S3/Minio, database) and how they connect
8. One thing you found interesting or surprising in the template code

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


