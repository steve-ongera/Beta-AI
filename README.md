# Beta AI — AI App Platform

> An OpenAI-Platform-style interface for building and running AI applications — not a coding tool, but a platform for AI-powered *apps*. Launching with a Mental Health module: direct, doctor-reviewed conversational support, built for scale into future domains.

---

## Important Disclaimer

This platform is **not a replacement for professional medical or psychiatric care**. The mental-health module:
- Clearly states it is not a licensed therapist/doctor and cannot diagnose or prescribe.
- Shows crisis resources (suicide/self-harm hotlines) whenever a message is flagged high-risk.
- Logs every high-risk message as a `CrisisEscalation` record for human review.
- Should be reviewed by licensed mental health professionals before any public/beta release.

---

## 1. Vision

Beta AI is designed like a **platform**, not a single app:

- **Today**: One flagship module — a mental health assistant, with chat, image upload, and image generation.
- **Tomorrow**: A general framework where new "API modules" (nutrition, legal, education, etc.) register themselves via the `chat` app's module registry, with no core rearchitecting.

---

## 2. Core Features (V1)

| Feature | Guest User | Logged-in User |
|---|---|---|
| Chat with AI | limited / generic responses | full, personalized responses |
| Chat history | not saved | saved per user, shown in sidenav |
| Image upload → AI response | limited | full |
| Image generation | not available | available |
| Login | — | Username/Password + Google OAuth |
| Multi-module support | scaffolded for future modules | scaffolded for future modules |

---

## 3. Tech Stack

**Backend** — Django + Django REST Framework, SQLite (dev), JWT auth (SimpleJWT + dj-rest-auth), `django-allauth` for Google OAuth, Celery + Redis (async tasks, not yet wired to a task).

**Frontend** — React (JSX) via Vite, React Router, Bootstrap Icons (CDN), custom CSS design system ("Quiet Harbor").

**AI Engine** — A separate local FastAPI service (`ai-engine/`), no third-party AI API calls. Currently rule-based (pattern matching + keyword knowledge base); see `ai-engine/TRAINING_GUIDE.md` for the path to retrieval (RAG) and a real fine-tuned local model.

---

## 4. Project Structure (as actually built)

```
Beta-AI/
├── backend/
│   ├── config/                 # settings.py, urls.py, wsgi.py, asgi.py
│   │                            # NOTE: your ROOT_URLCONF may say "backend.urls"
│   │                            # if you renamed the project package — keep
│   │                            # settings.py's INSTALLED_APPS/urls.py in sync
│   │                            # with whatever you named this folder.
│   ├── users/                  # auth: username/password + Google OAuth, profile
│   ├── chat/                   # AI-module registry (GET /api/modules/)
│   ├── media_ai/               # image upload analysis + image generation
│   ├── mentalhealth/           # first AI app module (flat app, not nested)
│   │   └── management/commands/seed_mentalhealth.py
│   ├── users/management/commands/seed_users.py
│   ├── chat/management/commands/{seed_modules.py, seed_all.py}
│   ├── media_ai/management/commands/seed_media.py
│   ├── requirements.txt
│   ├── .env.example
│   └── manage.py
│
├── frontend/
│   ├── index.html
│   ├── .env.example
│   ├── src/
│   │   ├── main.jsx / App.jsx
│   │   ├── services/api.js     # every backend endpoint, JWT refresh handling
│   │   ├── hooks/               # useAuth, useChat, useModules
│   │   ├── components/          # SideNav, SideFooter, GuestBanner,
│   │   │                        # ModuleSwitcher, GoogleLoginButton,
│   │   │                        # ImageGeneratorModal, ProtectedRoute,
│   │   │                        # PasswordField
│   │   ├── pages/               # ChatPage, LoginPage, RegisterPage,
│   │   │                        # SettingsPage, NotFoundPage
│   │   └── styles/main.css
│   └── vite.config.js
│
└── ai-engine/                   # local inference service — no external AI APIs
    ├── main.py                  # FastAPI app, POST /v1/infer
    ├── responder.py             # the actual response logic (Stage 0: rules)
    ├── requirements.txt
    ├── README.md
    └── TRAINING_GUIDE.md        # Stage 0 → RAG → fine-tuned model roadmap
```

---

## 5. API Overview (as actually built)

```
Auth (users app + dj-rest-auth)
POST   /api/auth/registration/          register
POST   /api/auth/login/                 username/password login → JWT
POST   /api/auth/logout/
POST   /api/auth/google/                exchange Google ID token → JWT
GET    /api/auth/user/                  current user profile
PATCH  /api/auth/user/                  update preferences (theme, etc.)
POST   /api/auth/token/refresh/         refresh access token

Module registry (chat app)
GET    /api/modules/                    list active AI-app modules

Mental health module (mentalhealth app)
GET    /api/modules/mental-health/sessions/         chat history (auth only)
GET    /api/modules/mental-health/sessions/<id>/
DELETE /api/modules/mental-health/sessions/<id>/
POST   /api/modules/mental-health/message/          send a message (guest or auth)

Media (media_ai app)
POST   /api/media/upload/               image → AI analysis
POST   /api/media/generate/             prompt → generated image (auth only)
```

---

## 6. How to Run the Server (all 3 services)

You need **three terminals** running at once: the AI engine, the Django
backend, and the React frontend. Start them in this order.

### 6.1 First-time setup

```bash
# --- AI engine ---
cd ai-engine
python -m venv venv && venv\Scripts\activate        # Windows
# source venv/bin/activate                           # macOS/Linux
pip install -r requirements.txt

# --- Backend ---
cd ../backend
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env                               # Windows: copy, macOS/Linux: cp
# edit .env — at minimum leave defaults as-is for local dev

python manage.py makemigrations
python manage.py migrate
python manage.py seed_all                             # creates demo users + demo data
# admin / admin12345, demo_user / demopass123

# --- Frontend ---
cd ../frontend
npm install
copy .env.example .env
```

### 6.2 Every time you develop

**Terminal 1 — AI engine (start first):**
```bash
cd ai-engine
venv\Scripts\activate
uvicorn main:app --port 9000 --reload
```
Verify it's up: `http://localhost:9000/healthz` should return `{"status": "ok"}`.

**Terminal 2 — Backend:**
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```
Runs at `http://localhost:8000`. Admin panel: `http://localhost:8000/admin/`
(log in with the `admin` user seed_all created).

**Terminal 3 — Frontend:**
```bash
cd frontend
npm run dev
```
Runs at `http://localhost:5173` — open this in your browser.

### 6.3 Sanity check

1. Open `http://localhost:5173`, log in as `demo_user` / `demopass123`.
2. Send the message `hi` in chat.
3. You should get back a personalized greeting from the AI engine
   (`"Hi demo_user! I'm here and ready to listen..."`) — if you instead see
   *"I'm having trouble reaching the assistant right now"*, the AI engine
   (Terminal 1) isn't running or isn't reachable at `AI_ENGINE_URL`.

---

## 7. Guest vs. Authenticated Behavior

- **Guests** can chat and upload images; responses use a lighter/generic
  profile and are labeled "general guidance — log in for personalized responses."
- **Authenticated users** get full model access, saved chat history, image
  generation, and personalized responses (their name is passed to the AI
  engine — see `ai-engine/responder.py`).
- Guest sessions are never shown in the saved chat-history sidenav.

---

## 8. Scalability Plan

1. **V1** (current): Django monolith with 4 apps + one decoupled AI engine.
2. **V2**: New modules register in the `chat` app's `AIModule` registry
   (see `chat/management/commands/seed_modules.py` for the pattern) — no
   core changes needed to add one.
3. **V3**: Each module + its inference needs becomes independently
   deployable/scalable behind a shared gateway.

---

## 9. Roadmap

- [x] Auth (username/password + Google OAuth), JWT
- [x] Mental health module: chat, sessions, crisis-flagging + escalation log
- [x] Image upload + image generation endpoints
- [x] Local AI engine (Stage 0: rule-based, no external API)
- [ ] AI engine Stage 1: RAG over doctor-reviewed content
- [ ] AI engine Stage 2: fine-tuned local model
- [ ] Clinical review process for the mental-health module before any public release
- [ ] Additional modules (nutrition, general wellness)

---

## 10. Contributing

Solo/early-stage build. Keep the codebase clean enough to onboard
contributors once the mental-health module is clinically reviewed.