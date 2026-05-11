# ManageAI Internal SaaS Platform

ManageAI is a production-oriented full-stack SaaS platform inspired by ManageEngine. It centralizes project operations, RBAC user management, task tracking, ticketing with screenshot uploads, local/hosted/GitHub project connections, branch deployments, document management, notifications with sound-ready realtime alerts, analytics, audit logging, API monitoring, AI-assisted task suggestions, Kanban workflows, and WebSocket-ready real-time updates.

The dashboard is role-aware:

- Super Admin: platform command center, users, audit logs, API monitoring, governance.
- Admin: project delivery, task assignment, branch deployment control, tickets, documents.
- Developer: assigned work, Day 1/2/3 progress, blockers, tickets, commit activity.
- Client: project progress, approved files, release visibility, ticket raising.

## Stack

- Frontend: React.js, Vite, Tailwind CSS, Framer Motion, Axios
- Backend: Django, Django REST Framework, SQLite, JWT authentication
- Realtime-ready: Django Channels with Redis-ready channel layers
- Integrations: GitHub API via `GITHUB_TOKEN` for branches, commits, developer activity, and branch deployment metadata

## Local Quick Start

1. Create environment files:

```bash
copy backend\.env.sqlite.example backend\.env
copy frontend\.env.example frontend\.env
```

2. Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 8000
```

3. Frontend:

```bash
cd frontend
npm install
npm run dev
```

4. Open `http://localhost:5173`.

Demo users after seeding:

- `super@manageai.local` / `ManageAI@12345`
- `admin@manageai.local` / `ManageAI@12345`
- `dev@manageai.local` / `ManageAI@12345`
- `client@manageai.local` / `ManageAI@12345`

For a fuller Windows local runbook, see [Deployment guide](docs/DEPLOYMENT.md).

## Documentation

- [Folder structure](docs/FOLDER_STRUCTURE.md)
- [Project flow](docs/PROJECT_FLOW.md)
- [Database schema](docs/DATABASE_SCHEMA.md)
- [API endpoints](docs/API_ENDPOINTS.md)
- [Deployment guide](docs/DEPLOYMENT.md)
# manage-ai
