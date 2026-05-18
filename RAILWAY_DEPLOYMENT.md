# Railway Deployment

This project has two deployable services: `backend` for Django and `frontend` for Vite.

## Backend service

Set the Railway root directory to `backend`.

Build command:

```bash
pip install -r requirements.txt
```

Start command (recommended, from `backend/Procfile`):

```bash
web: sh -c 'set -e; : "${PORT:=8000}"; python manage.py migrate --check --noinput || python manage.py migrate --noinput; python manage.py collectstatic --noinput; exec daphne -b 0.0.0.0 -p "$PORT" manage_ai.asgi:application'
```

Gunicorn fallback process type (if ASGI/WebSocket startup fails):

```bash
web-gunicorn: sh -c 'set -e; : "${PORT:=8000}"; python manage.py migrate --check --noinput || python manage.py migrate --noinput; python manage.py collectstatic --noinput; exec gunicorn manage_ai.wsgi:application --bind 0.0.0.0:"$PORT" --workers "${WEB_CONCURRENCY:-2}" --timeout "${GUNICORN_TIMEOUT:-120}" --access-logfile - --error-logfile -'
```

Healthcheck endpoint:

```text
/health/
```

Required variables:

```env
DJANGO_SECRET_KEY=change-this-to-a-long-random-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.railway.app,your-backend-domain.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.railway.app
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.railway.app
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
REDIS_CACHE_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}
USE_INMEMORY_CHANNELS=False
```

Optional variables:

```env
RAILWAY_PUBLIC_DOMAIN=your-backend-domain.railway.app
WEB_CONCURRENCY=2
GUNICORN_TIMEOUT=120
```

Add Railway PostgreSQL and Redis plugins before deploying the backend.

## Frontend service

Set the Railway root directory to `frontend`.

Build command:

```bash
npm ci && npm run build
```

Start command:

```bash
npm run preview -- --host 0.0.0.0 --port $PORT
```

Required variables:

```env
VITE_API_BASE_URL=https://your-backend-domain.railway.app/api
VITE_WS_URL=wss://your-backend-domain.railway.app/ws/events/
VITE_WS_BASE_URL=wss://your-backend-domain.railway.app/ws
VITE_FIREBASE_API_KEY=AIzaSyCiuXcEM9RuFBM1nEHBCpn19hShaeJ1Wyo
VITE_FIREBASE_AUTH_DOMAIN=manage-d7841.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=manage-d7841
VITE_FIREBASE_STORAGE_BUCKET=manage-d7841.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=185772558814
VITE_FIREBASE_APP_ID=1:185772558814:web:419b5844779d6cf09af54f
VITE_FIREBASE_MEASUREMENT_ID=G-N3YH8PVSYH
```

The Firebase SDK is initialized in `frontend/src/lib/firebase.js`; Firestore is exported as `firestore` for new database-backed frontend features.
