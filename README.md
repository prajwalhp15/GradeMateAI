# AI Grader — quick start

Prereqs:
- Python 3.10+
- MongoDB running (local or Atlas)
- (Recommended) Create SMTP app password if you want emails

1) Backend
$ cd backend
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
# copy .env.example -> .env and edit
$ python -m backend.app

2) Frontend
Open frontend/index.html in browser (or serve via simple HTTP server)
$ cd frontend
$ python -m http.server 8000

3) Create assignment
POST /api/assignments with JSON:
{
  "title": "Add",
  "description": "...",
  "tests": [{"input":"2\n3\n","expected":"5\n"}],
  "deadline": "2025-10-10T15:00:00"
}

Security & Production:
- Do NOT execute untrusted code without sandboxing. Use Docker / nsjail / Firecracker to isolate runs.
- Implement authentication (JWT), role-based access, rate-limits, input sanitization.
- Store secrets in a secure store (Vault).
