# Beta AI — AI App Platform

> An OpenAI-Platform-style interface for building and running AI applications — not a coding tool, but a platform for AI-powered *apps*. Launching with a Mental Health module: direct, doctor-trained conversational support, built for scale into future domains.

---

##  Important Disclaimer

This platform is **not a replacement for professional medical or psychiatric care**. Any mental-health module built on this platform must:
- Clearly state it is not a licensed therapist/doctor and cannot diagnose or prescribe.
- Provide crisis resources (suicide/self-harm hotlines) prominently and always-visible.
- Be reviewed by licensed mental health professionals before any public/beta release.
- Log and escalate (to a human or crisis resource) any conversation indicating risk of self-harm or harm to others.

This must be built into the product from day one, not added later.

---

## 1. Vision

MindBridge AI is designed like a **platform**, not a single app:

- **Today**: One flagship module — a mental health assistant trained on doctor-reviewed data, with chat, image upload, and image generation.
- **Tomorrow**: A general framework where new "API modules" (legal, nutrition, education, etc.) can be plugged in without rearchitecting the core.

The core product experience mirrors the familiar OpenAI Platform / ChatGPT-style UI: a central chat interface, a collapsible side navigation with chat history, and a clean, minimal, professional aesthetic — but purpose-built around structured "AI App" modules instead of raw code/dev tooling.

---

## 2. Core Features (V1)

| Feature | Guest User | Logged-in User |
|---|---|---|
| Chat with AI |  (limited / generic responses) |  (full, personalized, accurate) |
| Chat history | x |  (saved per user, shown in sidenav) |
| Image upload → AI response |  (limited) |  (full) |
| Image generation | x or limited | v |
| Login | — | Username/Password + Google OAuth |
| Multi-module support | Scaffolded for future modules | Scaffolded for future modules |

---

## 3. Tech Stack

**Backend**
- Django + Django REST Framework (API layer)
- PostgreSQL (primary database)
- Django Channels / WebSockets (optional, for streaming chat responses)
- Celery + Redis (async tasks: image generation, model inference queueing)
- `django-allauth` or `social-auth-app-django` (Google OAuth)
- JWT (SimpleJWT) for session/API auth

**Frontend**
- React (JSX, not TSX for V1) via Vite
- Bootstrap Icons for iconography
- Custom CSS / Bootstrap grid for layout
- React Router for navigation
- Context API or Redux (chat state, auth state)

**AI / ML**
- Custom-trained model/engine (domain-specific — mental health corpus, doctor-reviewed)
- Model serving via a dedicated inference service (FastAPI/Django microservice) — decoupled from the main backend so it can scale/swap independently
- Image generation via a separate pluggable image-gen service

**Infra (future-facing)**
- Dockerized services (web, api, inference, worker, redis, db)
- Designed so each "module" (mental health today, others later) can be deployed as its own service behind a shared gateway

---

## 4. High-Level Architecture

```
                        ┌─────────────────────┐
                        │   React Frontend     │
                        │  (Vite + JSX + BS)    │
                        └──────────┬───────────┘
                                   │ REST / WS
                        ┌──────────▼───────────┐
                        │   Django API Gateway  │
                        │ (auth, routing, users)│
                        └──────────┬───────────┘
                     ┌─────────────┼──────────────┐
                     │             │              │
           ┌─────────▼───┐ ┌───────▼──────┐ ┌─────▼──────┐
           │ Mental Health│ │ Image Gen /  │ │ Future      │
           │ Module (API) │ │ Vision Module│ │ Modules...  │
           └─────────┬────┘ └───────┬──────┘ └─────────────┘
                     │              │
           ┌─────────▼──────────────▼─────┐
           │   Custom AI Engine / Models    │
           │ (trained, doctor-reviewed data)│
           └────────────────────────────────┘
```

The Django API Gateway is deliberately kept "thin" — auth, user/chat data, routing — so new modules register as pluggable Django apps + their own model-serving service, without touching core logic.

---

## 5. Project Structure

```
mindbridge-ai/
├── backend/
│   ├── config/                # Django project settings (settings, urls, wsgi/asgi)
│   ├── users/                 # Auth: username/password + Google OAuth, profiles
│   ├── chat/                  # Chat sessions, messages, history
│   ├── modules/
│   │   └── mental_health/     # First API module app
│   ├── media_ai/              # Image upload handling + image generation requests
│   ├── core/                  # Shared utilities, permissions, base models
│   └── manage.py
│
├── frontend/
│   ├── public/
│   │   └── index.html         # SEO meta tags, Bootstrap Icons CDN
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── services/
│   │   │   └── api.js         # Centralized API endpoint definitions
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useChat.js
│   │   │   └── useChatHistory.js
│   │   ├── components/
│   │   │   ├── SideNav.jsx
│   │   │   ├── SideNavToggle.jsx
│   │   │   ├── SideFooter.jsx
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── ChatInput.jsx
│   │   │   ├── ChatHistoryList.jsx
│   │   │   ├── ImageUpload.jsx
│   │   │   ├── LoginModal.jsx
│   │   │   └── GuestBanner.jsx
│   │   ├── pages/
│   │   │   ├── ChatPage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   └── RegisterPage.jsx
│   │   └── styles/
│   └── vite.config.js
│
├── ai-engine/                 # Model training / inference service (decoupled)
│   ├── training/
│   ├── inference_api/
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 6. API Overview (V1 endpoints)

```
Auth
POST   /api/auth/register/
POST   /api/auth/login/
POST   /api/auth/google/
POST   /api/auth/refresh/
POST   /api/auth/logout/

Chat
GET    /api/chat/sessions/            # list chat history (auth only)
POST   /api/chat/sessions/            # create new session
GET    /api/chat/sessions/:id/
POST   /api/chat/sessions/:id/message/
DELETE /api/chat/sessions/:id/

Media / AI
POST   /api/media/upload/             # upload image, get AI response
POST   /api/media/generate/           # generate image (auth only)

Modules
GET    /api/modules/                  # list available AI app modules
POST   /api/modules/mental-health/message/
```

`frontend/src/services/api.js` will centralize all of the above as a single exported client so components/hooks never hardcode URLs.

---

## 7. Guest vs. Authenticated Behavior

- **Guests** can chat and upload images, but responses are served from a lighter/generic model path and are explicitly labeled as "general guidance — log in for personalized responses."
- **Authenticated users** get: full model access, saved chat history in the sidenav, image generation, and personalized context carried across sessions.
- No guest chat data is persisted as chat history — only ephemeral session state.

---

## 8. Scalability Plan

1. **V1**: Single Django monolith + one module (mental health) + one inference service.
2. **V2**: Extract each module into its own Django app with isolated routes/models; shared auth/chat core stays central.
3. **V3**: Move to separate deployable services per module (microservices) behind an API gateway; inference services scale independently (GPU-backed) from the web tier.
4. Chat history, user data, and media stored in a way that's module-agnostic from day one (generic `Session` / `Message` models with a `module` foreign key), so adding a new module never requires a schema rewrite.

---

## 9. Setup (planned)

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev

# Full stack (later)
docker-compose up --build
```

Environment variables (`.env`): `SECRET_KEY`, `DATABASE_URL`, `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `AI_ENGINE_URL`, `REDIS_URL`.

---

## 10. Roadmap

- [ ] V1: Auth (username/password + Google OAuth), chat UI, mental health module, chat history, image upload
- [ ] V1.1: Image generation
- [ ] V1.2: Crisis-detection safety layer + human escalation path
- [ ] V2: Module plugin architecture formalized
- [ ] V2.1: Additional health-adjacent modules (nutrition, general wellness)
- [ ] V3: Multi-tenant / module marketplace

---

## 11. Contributing

This is currently a solo/early-stage build. Structure above is intended to keep the codebase clean enough to onboard contributors once the core mental-health module is stable and clinically reviewed.