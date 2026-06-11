# VoiceBridge AI

> Cross-platform mobile app for AI-powered voice calls with real-time, multi-language translation.

**VoiceBridge AI** lets two or more people talk on a voice/video call while an AI pipeline transcribes, translates, and re-speaks each side's audio in the listener's preferred language - in near real time. Think *Star Trek universal translator*, but built on Whisper / GPT / ElevenLabs / WebRTC.

---

## Repository Layout

```
.
├── backend/        Node.js + Express + Socket.io + PostgreSQL + Redis API
├── mobile/         Flutter mobile app (Android + iOS)
├── admin/          Next.js admin dashboard
├── docs/           Architecture, API, install, deployment, security
├── k8s/            Kubernetes manifests
├── scripts/        Bootstrap / helper scripts
├── docker-compose.yml
└── .env.example
```

---

## Tech Stack

| Layer            | Technology                                                                 |
|------------------|----------------------------------------------------------------------------|
| Mobile           | Flutter 3.x, Riverpod, go_router, flutter_webrtc, socket_io_client          |
| Backend          | Node.js 20, Express 4, Socket.io 4, PostgreSQL 16, Redis 7                  |
| Realtime / RTC   | WebRTC (mesh + SFU-ready), Socket.io signaling                              |
| Speech-to-Text   | OpenAI Whisper / Realtime API, Deepgram, Google Speech (pluggable)          |
| Translation      | OpenAI GPT, Google Translate, DeepL, Azure Translator (pluggable)           |
| Text-to-Speech   | ElevenLabs, Azure TTS, Google TTS (pluggable)                               |
| Auth             | JWT + bcrypt, OTP (Twilio/Msg91), Google & Apple Sign-In                    |
| Payments         | Razorpay (INR) + Stripe (global)                                            |
| Storage          | S3 / Cloudflare R2 for recordings & media                                   |
| Deploy           | Docker, docker-compose, Kubernetes                                          |

---

## Core Features

- One-to-one and group voice calls (up to 20 participants)
- Real-time speech-to-text → translate → text-to-speech pipeline
- 100+ languages with pluggable AI providers
- Live captions (original + translated) with downloadable transcripts
- Optional AI voice cloning to preserve speaker tone
- Call recording (original + translated tracks) to cloud storage
- 1:1 + group chat with auto-translated messages, voice notes, files
- AI Meeting Mode with multi-language participants, transcripts, PDF export
- Subscription tiers (Free / Premium / Business) via Razorpay + Stripe
- Admin dashboard for users, calls, analytics, subscriptions
- End-to-end encrypted media, JWT auth, AES-256 at rest, GDPR-ready

---

## Quick Start

```bash
git clone https://github.com/your-org/voicebridge-ai.git
cd voicebridge-ai

cp .env.example .env                  
cp backend/.env.example backend/.env

docker compose up -d                  

cd mobile && flutter pub get && flutter run
```

Backend will be available at `http://localhost:4000`, admin at `http://localhost:3000`, Postgres at `localhost:5432`, Redis at `localhost:6379`.

See [`docs/INSTALL.md`](docs/INSTALL.md) for a full step-by-step setup and [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for production deployment.

---

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) - System architecture and data flow
- [`docs/API.md`](docs/API.md) - REST + Socket.io API reference
- [`docs/INSTALL.md`](docs/INSTALL.md) - Local development setup
- [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) - Production deployment guide
- [`docs/SECURITY.md`](docs/SECURITY.md) - Security model, encryption, compliance

---

## License

Proprietary - © 2026 VoiceBridge AI. All rights reserved.
