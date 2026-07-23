# DeployLab — a practice project for learning Django deployment

This is a tiny, complete Django app (a note-taking app with images) built
specifically so you can practice **every** part of deploying to Render:
database migrations, static files, media uploads, environment variables,
and debugging real errors.

Don't just deploy it once and move on — work through all three stages
below. Stage 3 (breaking things on purpose) is where the real learning
happens.

---

## Stage 1: Run it locally on Windows

Open PowerShell or Git Bash in this folder.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` — you should see the notes list page.
Visit `http://127.0.0.1:8000/admin/` — log in and add a note from there too.

Create a note through the normal form, with an image. Confirm it displays
on the list page. This proves the app works before you touch deployment
at all — always verify locally first.

---

## Stage 2: Deploy to Render

1. **Push this project to a new GitHub repo:**
   ```bash
   git init
   git add .
   git commit -m "initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/deploylab.git
   git push -u origin main
   ```

2. **Create a Postgres database on Render:**
   Dashboard → New + → PostgreSQL → create it → copy the **Internal
   Database URL**.

3. **Create a Web Service on Render:**
   Dashboard → New + → Web Service → connect your GitHub repo, then set:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn deploylab.wsgi:application`

4. **Set environment variables** (Environment tab), using `.env.example`
   in this repo as your checklist:
   - `SECRET_KEY` — generate a new random string, don't reuse the dev one
   - `DEBUG` → `False`
   - `ALLOWED_HOSTS` → `your-app-name.onrender.com` (the URL Render gives you)
   - `DATABASE_URL` → paste the Internal Database URL from step 2

5. **Deploy**, then watch the **Logs** tab while it builds.

6. Once live, open the **Shell** tab and run:
   ```bash
   python manage.py createsuperuser
   ```
   so you have an admin login on the live site too.

Visit your `.onrender.com` URL. Add a note with an image. This confirms
migrations, static files, and the database all work in production.

---

## Stage 3: Break it on purpose (do this — it's the actual point)

Each of these teaches you to recognize and fix a real, common deployment
error. For each one: break it, redeploy, read the error in Logs, form a
hypothesis, fix it, redeploy again.

1. **Wrong ALLOWED_HOSTS** — change the env var to some other domain,
   redeploy, and see Django's `DisallowedHost` error. Fix it back.

2. **Missing SECRET_KEY** — delete that env var, redeploy, see what
   error Django throws when a required setting is missing.

3. **Broken DATABASE_URL** — change one character in the value,
   redeploy, and read the connection error in the logs.

4. **Static files not loading** — comment out the `WhiteNoiseMiddleware`
   line in `settings.py`, push, and see the CSS disappear on the live
   site even though it still works locally. This is the classic
   "works on my machine" bug. Uncomment it to fix.

5. **The ephemeral filesystem gotcha** — upload a note with an image on
   the live site, confirm it shows up, then trigger a new deploy (push
   any small change). Check if the image is still there. (On Render's
   free tier, it likely won't be — the filesystem resets on every
   deploy.) This is intentional: it's the reason real production apps
   use cloud storage like Cloudinary or S3 for user uploads instead of
   local disk. Research one of those and try wiring it in as a stretch
   goal.

6. **DEBUG=True in production (understand why this is dangerous)** —
   temporarily set `DEBUG=True`, visit a broken URL like
   `/this-page-does-not-exist/`, and see the full Django debug page
   with your source code and settings exposed. Set it back to `False`
   immediately and understand why this must never ship to real users.

---

## What this project is intentionally missing

Once Stage 3 feels comfortable, extend this project yourself as further
practice:

- User authentication (only logged-in users can add/delete notes)
- Cloud storage for images (`django-storages` + S3 or Cloudinary)
- A custom domain instead of the `.onrender.com` URL
- A GitHub Actions workflow that runs `python manage.py test` before
  every deploy (real CI, not just CD)

---

## Quick reference: file purpose

| File | Purpose |
|---|---|
| `build.sh` | Runs on Render during every deploy: installs deps, collects static files, runs migrations |
| `requirements.txt` | Python packages Render installs |
| `deploylab/settings.py` | Reads all production config from environment variables |
| `.env.example` | Checklist of env vars to set in Render's dashboard (not read by Django directly) |
| `notes/` | The actual app: model, views, templates, admin |
