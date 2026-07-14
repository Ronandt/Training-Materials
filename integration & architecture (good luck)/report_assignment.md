# Report/Presentation Assignment

The goal of this assignment is to provide experience understanding documentation, working with unfamiliar code written by someone else, and familiarising yourself with production-ready code.

You are to clone and tinker with the given template (architecture-sample-app) and read through the relevant sections of the Software Engineering Bible. You are also encouraged to do further additional research (e.g. what is S3/AWS) to better understand how exactly the application functions.

**Read the Software Engineering Bible before you start writing anything.** It's not optional background reading — several of the "Concepts explicitly not covered in training" below (code architecture, error handling, logging, testing) are exactly the topics it covers in general terms. Read the relevant sections *first*, then go confirm/contrast what you find against how this specific template actually does it. Skipping straight to the code without it means you're guessing at *why* the code is structured the way it is, not just *what* it does.

Architecture-Sample-App: https://github.com/Ronandt/Architecture-Sample-App
Software Engineering Bible: https://docs.google.com/document/d/1GKBNkuOWUwuF6SQbBu9atvg8SUxaNDDEaDFgCV9PjDY/edit?tab=t.0

### Architecture-Sample-App
In order to run this application, you will need to know how to setup Keycloak and be able to run the frontend and the backend. Refer to `template_setup_backend.md` and `template_setup_frontend.md` — and [`keycloak_and_s3_setup.md`](keycloak_and_s3_setup.md) (and its short [slide primer](keycloak-s3-basics-slides.pdf), if you want the basic mental model before diving in) for the Keycloak/S3 setup steps themselves.

## Recommended Contents

0. Brief intro — what is the template, what problem does it solve, and who would use it
1. Architecture diagram — the major components (frontend, backend, Keycloak, S3/Minio, PostgreSQL) and how they connect to each other
2. Concepts from the stack not taught in training — explain what each unfamiliar piece is and the role it plays (see the list below for guidance)
3. Live demo — run the template locally and show the login flow, a protected route, and an admin-only action
4. Code walkthrough — trace one request through the system: from the frontend, through the backend, through auth, to the database and back
5. How you would extend it — pick one feature and explain concretely how you would add it to the template. Going further and actually building the feature yourself — however small — is strongly encouraged: it's the fastest way to find out whether you actually understood the architecture, not just read about it, and gives you something real to show during the live demo.

*Concepts explicitly not covered in the training:*
- Code architecture — how to architect your app: services, repository pattern, guard patterns, error handling (**important**)
- File organisation
- Middleware
- Keycloak + the Keycloak adapter (`python-keycloak`)
- S3/Boto3/Minio + the S3 adapter
- SSL
- Env management & settings
- PostgreSQL
- Dependency injection
- Logging
- Unit testing
- Infrastructure & deployment (optional — only if you want to go further)
- Extending the architecture
- Difference between production and development (no inspect/debug tools, etc.)

For example for code architecture you can explain:
- What is the difference between a repository and a service, and why are they kept separate?
- How are exceptions raised in a service and where do they get caught and turned into HTTP responses?
- How is dependency injection used — what does FastAPI's `Depends()` actually do at runtime?
- Why is the repository pattern useful when you want to swap out the database later?
- If you needed to talk to an external API, how would you connect to it — where would the service/adapter layers fit in?
- If you have an API adapter, should it return an SQLAlchemy model since that's one level below the service layer? If not, what should it use to encapsulate data instead?

Or for authentication you can explain:
- How is the JWT token passed from the frontend to the backend on each request?
- Which part of the code checks the roles or identity of the user, and how does it do it?
- How are tokens refreshed — what happens when an access token expires?
- What is the difference between a realm, a client, a group, and a role in Keycloak?
- What does the Keycloak adapter (`python-keycloak`) do?
- What is the difference between a confidential client and a public client?

Or for file storage (S3/Minio) you can explain:
- What is object storage?
- What does the image upload/retrieve flow look like end to end?
- What is a presigned URL and why would you use one instead of routing the file through the backend?
- What does Boto3 do and how does Minio fit in as a local alternative to AWS S3?
- Where in the codebase does a file upload get handled — what goes to S3 and what gets stored in the database?

Or for environment and settings you can explain:
- Why should secrets never be hardcoded in the codebase — what is the actual risk?
- How does the template load config from environment variables, and what library manages this?
- What is the difference between a `.env` file used locally and how secrets are managed in a real deployed environment?

Or for file organisation you can explain:
- Why are the files organised that way — why by feature rather than by repository or service?

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