# AI-HR Recruitment Platform — Backend

FastAPI backend for the AI-HR recruitment platform. Provides authentication, candidate management, job postings, AI-powered resume analysis, interview scheduling, and analytics APIs.

## Prerequisites

- Python 3.11+
- pip

## Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your environment file
cp .env.example .env
```

## Configuration

Edit `.env` to customize settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./dev.db` | Database connection string |
| `SECRET_KEY` | (placeholder) | JWT signing key — **change in production** |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` (24h) | Token expiry duration |
| `FRONTEND_URL` | `http://localhost:5173` | Allowed CORS origin |

### Switching to PostgreSQL

1. Install the async Postgres driver:
   ```bash
   pip install asyncpg
   ```
2. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ai_hr_db
   ```
3. Restart the server — tables are auto-created on startup.

## Running the Server

```bash
# Development (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The server starts at **http://localhost:8000**.

## API Documentation

Once running, interactive docs are available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Quick Smoke Test

Run these commands in order to verify the backend is working:

```bash
# 1. Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234!","full_name":"Test User","role":"hr"}'

# 2. Login (save the token)
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234!"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")

# 3. Get profile (authenticated)
curl http://localhost:8000/api/v1/auth/profile \
  -H "Authorization: Bearer $TOKEN"

# 4. Get HR jobs (authenticated)
curl http://localhost:8000/api/v1/hr/jobs \
  -H "Authorization: Bearer $TOKEN"
```

## API Endpoints

### Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login, returns JWT + user |
| POST | `/api/v1/auth/logout` | Logout (invalidate client-side) |
| GET | `/api/v1/auth/profile` | Get current user profile |
| POST | `/api/v1/auth/forgot-password` | Request password reset |
| POST | `/api/v1/auth/reset-password` | Reset password with token |

### Candidate
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/candidate/profile` | Get candidate profile |
| PUT | `/api/v1/candidate/profile` | Update candidate profile |
| GET | `/api/v1/candidate/resumes` | List uploaded resumes |
| POST | `/api/v1/candidate/resumes/upload` | Upload a resume |
| GET | `/api/v1/candidate/resumes/{id}/analysis` | Get resume analysis |
| GET | `/api/v1/candidate/applications` | List applications |
| POST | `/api/v1/candidate/applications` | Submit application |
| GET | `/api/v1/candidate/saved-jobs` | List saved jobs |
| POST | `/api/v1/candidate/saved-jobs/{jobId}` | Save a job |
| DELETE | `/api/v1/candidate/saved-jobs/{jobId}` | Unsave a job |

### HR
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/hr/jobs` | List all jobs |
| GET | `/api/v1/hr/jobs/{id}` | Get job details |
| POST | `/api/v1/hr/jobs` | Create a job |
| PUT | `/api/v1/hr/jobs/{id}` | Update a job |
| DELETE | `/api/v1/hr/jobs/{id}` | Delete a job |
| GET | `/api/v1/hr/candidates` | List all candidates |
| GET | `/api/v1/hr/candidates/{id}` | Get candidate details |
| PATCH | `/api/v1/hr/candidates/{id}/status` | Update candidate status |
| GET | `/api/v1/hr/metrics` | Get dashboard metrics |
| GET | `/api/v1/hr/analytics` | Get hiring analytics |
| POST | `/api/v1/hr/reports` | Generate a report |

### AI
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/ai/resume/analyze/{resumeId}` | Analyze a resume |
| GET | `/api/v1/ai/resume/score/{resumeId}` | Get resume score |
| GET | `/api/v1/ai/match/{candidateId}/{jobId}` | Get candidate-job match |
| GET | `/api/v1/ai/recommendations/jobs/{candidateId}` | Job recommendations |
| GET | `/api/v1/ai/recommendations/candidates/{jobId}` | Candidate recommendations |
| GET | `/api/v1/ai/skill-gap/{candidateId}` | Skill gap analysis |
| GET | `/api/v1/ai/rank-candidates/{jobId}` | Rank candidates for job |
| GET | `/api/v1/ai/interview-feedback/{interviewId}` | AI interview feedback |

### Interviews
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/interviews/schedule` | Get interview schedule |
| GET | `/api/v1/interviews/{id}` | Get interview details |
| POST | `/api/v1/interviews` | Schedule an interview |
| PUT | `/api/v1/interviews/{id}` | Update an interview |
| DELETE | `/api/v1/interviews/{id}` | Cancel an interview |
| POST | `/api/v1/interviews/{id}/feedback` | Submit feedback |
| GET | `/api/v1/interviews/results` | Get interview results |

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, lifespan
│   ├── config.py            # Settings via pydantic-settings
│   ├── dependencies.py      # Auth dependency (get_current_user)
│   ├── core/                # Security, exceptions, permissions
│   ├── db/                  # SQLAlchemy engine, base, migrations
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── api/v1/             # Route handlers
│   ├── services/            # Business logic (future)
│   ├── ai_integration/      # AI/ML services (future)
│   ├── integrations/        # S3, email clients (future)
│   ├── websockets/          # WebSocket handlers
│   └── middleware/          # Audit, rate limiting
├── tests/
├── requirements.txt
├── .env.example
└── Dockerfile
```

## Frontend Integration

The frontend (React + Vite) expects:

- Backend at `http://localhost:8000`
- All API routes prefixed with `/api/v1`
- JWT sent as `Authorization: Bearer <token>` header
- Login response shape: `{ token: string, user: { id, email, full_name, role } }`
- On 401 response, frontend clears localStorage and redirects to `/login`

Ensure your frontend's environment variable (e.g., `VITE_API_URL`) is set to `http://localhost:8000/api/v1`.
