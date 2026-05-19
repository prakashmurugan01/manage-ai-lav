# Railway Deployment

This project has two deployable services: `backend` for Django and `frontend` for Vite.

Railway references used for this guide:

- Variables: https://docs.railway.com/reference/variables
- Volumes: https://docs.railway.com/volumes
- Data and storage: https://docs.railway.com/data-storage

## Backend service

Set the Railway root directory to `backend`.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
sh scripts/start.sh
```

Required variables:

```env
DJANGO_SECRET_KEY=change-this-to-a-long-random-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.railway.app,.up.railway.app,your-backend-domain.railway.app
FRONTEND_URL=https://your-frontend-domain.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.railway.app
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.railway.app
DATABASE_URL=${{Postgres.DATABASE_URL}}
DB_CONN_MAX_AGE=60
DB_SSLMODE=require
REDIS_URL=${{Redis.REDIS_URL}}
REDIS_CACHE_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}
USE_INMEMORY_CHANNELS=False
MEDIA_ROOT=${{RAILWAY_VOLUME_MOUNT_PATH}}/media
SERVE_MEDIA_FILES=True
```

Add Railway PostgreSQL and Redis plugins before deploying the backend. Add a Railway Volume to the backend service for uploaded avatars, documents, remote-transfer chunks, and other `/media/` files. Railway exposes `RAILWAY_VOLUME_MOUNT_PATH` when a volume is attached.

The backend has these health endpoints:

- `/healthz/`: liveness check for Railway.
- `/readyz/`: checks database readiness with `SELECT 1`.

The backend startup script runs:

```bash
python manage.py check
python manage.py migrate --noinput
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p $PORT manage_ai.asgi:application
```

Use Daphne, not Gunicorn, because the app uses Django Channels and WebSockets for realtime and remote access.

## Optional worker services

For scheduled hosting checks, notifications, server monitoring, and other background tasks, create two extra Railway services from the same repo with root directory `backend`.

Celery worker start command:

```bash
celery -A manage_ai worker -l info
```

Celery beat start command:

```bash
celery -A manage_ai beat -l info
```

Use the same backend variables for both worker services, especially `DATABASE_URL`, `REDIS_URL`, `CELERY_BROKER_URL`, and `CELERY_RESULT_BACKEND`.

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

## Deployment order

1. Create Railway project.
2. Add PostgreSQL.
3. Add Redis.
4. Create backend service from GitHub with root directory `backend`.
5. Add a volume to the backend service.
6. Add backend variables listed above.
7. Deploy backend and wait for `/healthz/` to pass.
8. Open `/readyz/`; it should return database `ok`.
9. Create frontend service with root directory `frontend`.
10. Add frontend variables with the backend public URL.
11. Deploy frontend.
12. Create optional Celery worker and beat services if background jobs are required.

## Useful Railway CLI commands

```bash
railway login
railway link
railway status
railway variables
railway logs
railway run python manage.py check
railway run python manage.py showmigrations
railway run python manage.py migrate --noinput
railway run python manage.py collectstatic --noinput
railway run python manage.py createsuperuser
```

## Troubleshooting

Only `/healthz/` works, APIs fail:

- Check `/readyz/`. If database is not `ok`, verify `DATABASE_URL=${{Postgres.DATABASE_URL}}`.
- Run `railway run python manage.py migrate --noinput`.
- Confirm `DJANGO_ALLOWED_HOSTS` includes `.railway.app` and your exact backend domain.

Authentication fails or browser shows CORS errors:

- Set `FRONTEND_URL`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` to the frontend HTTPS URL.
- Rebuild the frontend after changing `VITE_API_BASE_URL`.

WebSockets or remote access fail:

- Use `wss://your-backend-domain.railway.app/ws/...` in frontend variables.
- Keep Daphne as the backend server.
- Use Redis and set `USE_INMEMORY_CHANNELS=False`; in-memory channels do not work reliably across processes.

Uploaded files disappear:

- Attach a Railway Volume.
- Set `MEDIA_ROOT=${{RAILWAY_VOLUME_MOUNT_PATH}}/media`.
- Keep `SERVE_MEDIA_FILES=True` unless you move media to S3-compatible storage.

Static files fail:

- Confirm startup logs show `collectstatic`.
- Run `railway run python manage.py collectstatic --noinput`.

Deployment loops or crashes before listening:

- Check `railway logs`.
- Verify `DJANGO_SECRET_KEY` is set and long/random.
- Verify `DATABASE_URL` and `REDIS_URL` are present.
- Confirm the service root directory is `backend`.

Provider warnings:

- `hosting.W001` means AWS keys are missing. It does not stop core APIs. Add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` only if AWS hosting integration is needed.
