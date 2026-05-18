# Supabase PostgreSQL Migration Guide

## 📋 Overview

This guide walks you through migrating from Firebase/SQLite to **Supabase PostgreSQL** for your ManageAI backend.

## 🎯 Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click **New Project**
4. Fill in:
   - **Name:** `manage-ai` (or your project name)
   - **Database Password:** Create a strong password (save this!)
   - **Region:** Choose closest to your users
5. Click **Create new project** (wait 2-3 minutes for setup)

## 🔐 Step 2: Get Connection Details

Once your Supabase project is ready:

1. Go to **Project Settings** → **Database**
2. Under **Connection Info**, find:
   - **Host:** `db.[project-id].supabase.co`
   - **Port:** `5432`
   - **Database:** `postgres`
   - **User:** `postgres`
   - **Password:** Your database password

3. Copy the **Connection string** (URI format):
   ```
   postgresql://postgres:[PASSWORD]@db.[project-id].supabase.co:5432/postgres
   ```

## ✅ Step 3: Update Backend Environment Variables

### Local Development

Update `backend/.env`:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.sqerzctpeharotzjtyfi.supabase.co:5432/postgres

# Keep other settings
DJANGO_SECRET_KEY=your-dev-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Redis (local or external)
REDIS_URL=redis://127.0.0.1:6379/0
REDIS_CACHE_URL=redis://127.0.0.1:6379/1
```

### Railway Deployment

In **Railway Dashboard** → **Backend** → **Variables**:

```env
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-railway-domain.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.railway.app
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.railway.app

# Point to Supabase PostgreSQL
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.sqerzctpeharotzjtyfi.supabase.co:5432/postgres

# Use Railway Redis plugin
REDIS_URL=${{Redis.REDIS_URL}}
REDIS_CACHE_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}

USE_INMEMORY_CHANNELS=False
```

**Important:** Replace `[PASSWORD]` with your actual Supabase database password.

## 🚀 Step 4: Run Database Migrations

### Local Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Railway Deployment

The migration runs automatically in the start command:

```bash
python manage.py migrate && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p $PORT manage_ai.asgi:application
```

## 📊 Step 5: Verify Migration

### Check Local Connection

```bash
python manage.py dbshell
```

This should connect to Supabase. You'll see a PostgreSQL prompt:
```
postgres=>
```

Type `\q` to exit.

### Check in Supabase Dashboard

1. Go to **Supabase Dashboard** → Your Project
2. Click **SQL Editor**
3. Run a simple query:
   ```sql
   SELECT * FROM information_schema.tables WHERE table_schema = 'public';
   ```

You should see your Django tables like `accounts_user`, `projects_project`, etc.

## 🔄 Step 6: Backup Existing Data (If Migrating)

If you have data in SQLite that needs to be preserved:

### Export from SQLite

```bash
# Dump SQLite data
python manage.py dumpdata > data_backup.json
```

### Import to Supabase PostgreSQL

```bash
# Load data into Supabase
python manage.py loaddata data_backup.json
```

## 🐛 Troubleshooting

### Connection Failed

**Error:** `psycopg2.OperationalError: could not connect to server`

**Fix:**
1. Verify DATABASE_URL is correct (no typos)
2. Check Supabase project is running (visit supabase.com dashboard)
3. Ensure psycopg2 is installed: `pip install psycopg2-binary`
4. If in Railway, check all environment variables are set

### Authentication Failed

**Error:** `FATAL: password authentication failed for user "postgres"`

**Fix:**
1. Verify password in DATABASE_URL is correct
2. Go to Supabase → Project Settings → Database → Reset password if needed

### SSL Certificate Error

**Error:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Fix:**
1. Add this to CONNECTION_INIT in settings.py (already handled by django):
2. Or disable SSL (not recommended for production):
   ```
   DATABASE_URL=postgresql://...?sslmode=disable
   ```

## 📦 Optional: Supabase Agent Skills

Install Supabase-specific tools for better development:

```bash
npm install -g supabase
npx skills add supabase/agent-skills
```

## ✨ Benefits of Supabase PostgreSQL

✅ **Managed Database** - No infrastructure management  
✅ **Automatic Backups** - Daily backups included  
✅ **Real-time Subscriptions** - Optional real-time features  
✅ **Vector Support** - For AI/ML features  
✅ **Scalable** - Handle production workloads  
✅ **Free Tier** - Start for free, pay-as-you-go  

## 📚 Next Steps

1. ✅ Update environment variables
2. ✅ Run migrations
3. ✅ Test locally
4. ✅ Deploy to Railway
5. ✅ Monitor logs for errors

For more Supabase documentation, visit: https://supabase.com/docs
