# Backend Setup Guide

## Prerequisites

- Python 3.11+
- A running Keycloak instance and S3-compatible store — see [`keycloak_and_s3_setup.md`](keycloak_and_s3_setup.md) for how to set both up (that guide is shared across apps; this file only covers what's specific to this one)

---

## 1. Install Dependencies

From the `architecture-project-backend/` directory:

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

---

## 2. Configure the `.env` File

The `.env` file lives at `architecture-project-backend/app/.env`. Copy the template below and fill in your values.

```env
# Database
DATABASE_URL=sqlite:///./test.db

# Keycloak (required)
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=your-realm
KEYCLOAK_CLIENT_ID=your-client-id
KEYCLOAK_CLIENT_SECRET=your-client-secret
KEYCLOAK_CERT_FILEPATH=          # Path to SSL cert file, or leave blank to skip verification

# Keycloak (optional)
KEYCLOAK_ALLOWED_GROUPS=         # Comma-separated group names to allow
KEYCLOAK_ADMIN_ROLE=             # Role name that grants admin access
KEYCLOAK_ADMIN_USERNAME=         # Admin service account username (dev only)
KEYCLOAK_ADMIN_PASSWORD=         # Admin service account password (dev only)
KEYCLOAK_TIMEOUT=10

# S3 (Required)
S3_ENDPOINT=https://s3.amazonaws.com
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_BUCKET=
S3_SSL_CERT=

# App
CORS_ORIGINS=["http://localhost:5173"]
LOG_LEVEL=INFO
```

### Required vs Optional

| Variable | Required | Notes |
|---|---|---|
| `KEYCLOAK_URL` | Yes | Base URL of your Keycloak server |
| `KEYCLOAK_REALM` | Yes | Name of the realm the app belongs to |
| `KEYCLOAK_CLIENT_ID` | Yes | Client ID registered in the realm |
| `KEYCLOAK_CLIENT_SECRET` | Yes (confidential client) | Required for token/refresh/logout endpoints |
| `KEYCLOAK_CERT_FILEPATH` | No | SSL cert for self-signed Keycloak instances |
| `KEYCLOAK_ADMIN_USERNAME/PASSWORD` | No | Dev/test only — never use in production |
| `DATABASE_URL` | No | Defaults to a local SQLite file |

---

## 3. Run the Server

The app must be started with **uvicorn** from the `app/` directory so that bare imports (`from shared.config import ...`) resolve correctly.

```bash
cd architecture-project-backend/app
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

---

## Keycloak & S3 Setup

Full step-by-step instructions (starting Keycloak/MinIO, creating a realm/client/groups, token verification, bucket + access key setup, production S3) live in the shared reference: [`keycloak_and_s3_setup.md`](keycloak_and_s3_setup.md).

The only thing specific to *this* app is which `.env` variables it reads and how it enforces them — covered in the [`.env` section above](#2-configure-the-env-file). In short:

- `KEYCLOAK_ALLOWED_GROUPS` is enforced by `get_current_user` in `shared/dependencies.py` — a request whose JWT groups don't intersect with this list gets HTTP 403. Leave it empty to allow all authenticated users.
- The S3 client is `infrastructure.adapters.s3_adapter.S3BucketClient` — same code path for MinIO locally and real S3 in production, only the `.env` values change.
