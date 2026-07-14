# Keycloak & S3 Setup Reference

A reusable reference for wiring **Keycloak** (auth) and an **S3-compatible object store** (production S3 or local MinIO) into a backend built on the shared architecture template. Not tied to one specific app — the concepts, admin-console steps, and `.env` variable names below match the shared backend template's conventions; adjust names/paths if your app deviates from it.

**Slides:** [`keycloak-s3-basics-slides.pdf`](keycloak-s3-basics-slides.pdf) — a short conceptual primer (what a realm/client/group is, what a presigned URL solves) if you want the basic mental model before working through the setup steps below. It's deliberately shallow — the report assignment still expects you to research the app-specific details yourself.

Each app's own setup guide (e.g. `template_setup_backend.md`) should link here for the "how do I configure Keycloak/S3" steps, and keep only its own app-specific `.env` values and run instructions.

---

## Keycloak Setup

### 1. Start Keycloak

The easiest way is Docker:

```bash
docker run -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest start-dev
```

Open the admin console at `http://localhost:8080`.

### 2. Create a Realm

1. Log in as `admin / admin`.
2. Click **Create realm**.
3. Enter a **Realm name** (e.g. `portal`) — this becomes `KEYCLOAK_REALM`.
4. Click **Create**.

### 3. Create a Client

1. Inside your realm go to **Clients → Create client**.
2. Set **Client ID** (e.g. `my-app`) — this becomes `KEYCLOAK_CLIENT_ID`.
3. Set **Client authentication** to **On** (makes it a confidential client).
4. Under **Valid redirect URIs** add `http://localhost:8000/*`.
5. Save, then go to the **Credentials** tab and copy the **Client secret** — this becomes `KEYCLOAK_CLIENT_SECRET`.

### 4. Create a Test User (optional)

1. Go to **Users → Add user**.
2. Fill in a username and click **Create**.
3. On the **Credentials** tab set a password and turn off **Temporary**.

### 5. Groups

Groups control which users can access the API. The app reads a `groups` claim from the JWT and checks it against `KEYCLOAK_ALLOWED_GROUPS`.

#### Create a Group

1. In the Keycloak admin console go to **Groups → Create group**.
2. Give it a name (e.g. `portal-users`).
3. Add users to the group: open a user → **Groups** tab → **Join Group**.

#### Add Groups to the Token

By default Keycloak does **not** include group membership in the JWT. You need to add a mapper to your client:

1. Go to **Clients → your-client → Client scopes**.
2. Click the dedicated scope (same name as your client, e.g. `my-app-dedicated`).
3. Go to **Mappers → Add mapper → By configuration → Group Membership**.
4. Set the fields:
   - **Name**: `groups`
   - **Token Claim Name**: `groups`
   - **Full group path**: Off (so the claim contains `portal-users`, not `/portal-users`)
   - **Add to ID token**: On
   - **Add to access token**: On
5. Save.

After this the decoded JWT will contain:

```json
{
  "groups": ["portal-users", "another-group"]
}
```

#### Restrict API Access by Group

Set `KEYCLOAK_ALLOWED_GROUPS` in your `.env` to a comma-separated list of group names:

```env
KEYCLOAK_ALLOWED_GROUPS=portal-users,beta-testers
```

Every authenticated request is checked by `get_current_user` in `shared/dependencies.py` (adjust the path if your app organizes this differently). If the user's JWT groups don't intersect with the allowed list, the request is rejected with HTTP 403. Leave `KEYCLOAK_ALLOWED_GROUPS` empty to allow all authenticated users regardless of group.

### 6. Token Verification

The app verifies Bearer JWTs by fetching the realm's RS256 public key from:

```
{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}
```

No additional config is needed — this is automatic. If Keycloak uses a self-signed certificate, point `KEYCLOAK_CERT_FILEPATH` at the cert file.

### Client Types

| Client type | `KEYCLOAK_CLIENT_SECRET` needed | What works |
|---|---|---|
| Public | No | Token verification (`verify_user_token`) |
| Confidential | Yes | All endpoints incl. `get_token`, `refresh_token`, `logout` |

> An admin adapter for Keycloak admin operations (e.g. `KeycloakAdminAdapter`) is intended for **development/testing only** and should not be used in production.

---

## S3 / MinIO Setup

MinIO is an S3-compatible object store you can run locally instead of connecting to AWS — the app talks to both through the same boto3-based client, so only `.env` values change between them, not code.

### Local Development (MinIO)

**1. Start MinIO (Docker, recommended):**

```bash
docker run -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  quay.io/minio/minio server /data --console-address ":9001"
```

| Port | Purpose |
|---|---|
| `9000` | S3 API (what the app talks to) |
| `9001` | MinIO web console |

Open the console at `http://localhost:9001` and log in with `minioadmin / minioadmin`.

**2. Create a bucket:** **Buckets → Create Bucket**, name it (e.g. `my-bucket`) — this becomes `S3_BUCKET`.

**3. Create an access key:** **Access Keys → Create access key**. Copy the **Access Key** and **Secret Key** shown — you won't see the secret again.

**4. Configure `.env`:**

```env
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=<your-access-key>
S3_SECRET_KEY=<your-secret-key>
S3_BUCKET=my-bucket
S3_SSL_CERT=
```

> `S3_ENDPOINT` must point to port `9000`, not the console port `9001`. Leave `S3_SSL_CERT` blank — MinIO runs over plain HTTP in dev mode.

**5. Create the bucket from code (optional):** the S3 client typically exposes a helper that creates the bucket if it doesn't already exist, callable once on startup or from a script:

```python
from infrastructure.adapters.s3_adapter import S3BucketClient

client = S3BucketClient()
client.create_bucket_if_not_exists("my-bucket")
```

### Production (Real AWS S3)

The same code path works against real S3 — only the `.env` values change:

```env
S3_ENDPOINT=https://s3.amazonaws.com
S3_ACCESS_KEY=<IAM access key>
S3_SECRET_KEY=<IAM secret key>
S3_BUCKET=<your-bucket-name>
S3_SSL_CERT=
```

Create the bucket and IAM access key from the AWS console (or CLI) instead of the MinIO console — the app-facing steps are otherwise identical. Use an IAM user/role scoped to just that bucket rather than root credentials.

### URL Format

When the app uploads a file it returns a URL in the form:

```
{S3_ENDPOINT}/{bucket}/{object-key}
```

e.g. `http://localhost:9000/my-bucket/object-key` locally, or the equivalent `https://s3.amazonaws.com/...` (or bucket-subdomain form) in production — served directly by the object store and accessible in the browser for public objects.

---

## `.env` Reference

| Variable | Required | Notes |
|---|---|---|
| `KEYCLOAK_URL` | Yes | Base URL of your Keycloak server |
| `KEYCLOAK_REALM` | Yes | Name of the realm the app belongs to |
| `KEYCLOAK_CLIENT_ID` | Yes | Client ID registered in the realm |
| `KEYCLOAK_CLIENT_SECRET` | Yes (confidential client) | Required for token/refresh/logout endpoints |
| `KEYCLOAK_CERT_FILEPATH` | No | SSL cert for self-signed Keycloak instances |
| `KEYCLOAK_ALLOWED_GROUPS` | No | Comma-separated group names to allow; empty = allow all authenticated users |
| `KEYCLOAK_ADMIN_USERNAME` / `KEYCLOAK_ADMIN_PASSWORD` | No | Dev/test only — never use in production |
| `S3_ENDPOINT` | Yes | MinIO (`http://localhost:9000`) or real S3 (`https://s3.amazonaws.com`) |
| `S3_ACCESS_KEY` / `S3_SECRET_KEY` | Yes | From the MinIO console or your IAM user |
| `S3_BUCKET` | Yes | Bucket name |
| `S3_SSL_CERT` | No | Leave blank for MinIO in dev mode |
