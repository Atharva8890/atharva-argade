# API Reference

Base URL: `http://localhost:4000` (dev), `https://api.voicebridge.ai` (prod).

All authenticated endpoints expect `Authorization: Bearer <accessToken>`.

---

## Health

| Method | Path        | Description     |
|--------|-------------|-----------------|
| GET    | `/health`   | Health probe    |

---

## Auth (`/api/v1/auth`)

| Method | Path                  | Body / Notes                                                                                |
|--------|-----------------------|---------------------------------------------------------------------------------------------|
| POST   | `/signup`             | `{ name, email, password, language?, phone? }` → `{ user, tokens }`                         |
| POST   | `/login`              | `{ email, password }` → `{ user, tokens }`                                                  |
| POST   | `/refresh`            | `{ refreshToken }` → `{ user, tokens }`                                                     |
| POST   | `/oauth`              | `{ provider: 'google'\|'apple', idToken }` (verifier stubbed)                              |
| POST   | `/otp/request`        | `{ channel: 'sms'\|'email', target }` → `{ ttl }` (dev returns `devCode`)                   |
| POST   | `/otp/verify`         | `{ channel, target, code }` → `{ verified: true }`                                          |
| POST   | `/forgot-password`    | `{ email }` → `{ ok: true }`                                                                |
| POST   | `/reset-password`     | `{ token, password }` → `{ ok: true }`                                                      |
| GET    | `/me`                 | Returns the current user                                                                    |

---

## Users (`/api/v1/users`)

| Method | Path                              | Description                            |
|--------|-----------------------------------|----------------------------------------|
| PATCH  | `/me`                             | Update profile fields                  |
| DELETE | `/me`                             | Delete account                         |
| GET    | `/contacts`                       | List contacts                          |
| POST   | `/contacts`                       | Add a contact `{ email, alias? }`      |
| DELETE | `/contacts/:contactUserId`        | Remove a contact                       |

---

## Calls (`/api/v1/calls`)

| Method | Path                  | Body                                                                       |
|--------|-----------------------|----------------------------------------------------------------------------|
| GET    | `/ice-servers`        | STUN/TURN config for WebRTC                                                |
| POST   | `/`                   | `{ receiverId, type?, isGroup?, participants? }` → `{ call }`              |
| POST   | `/:id/end`            | Marks the call ended; auto-computes `duration_sec`                         |
| GET    | `/`                   | `?limit=&offset=` paginated history with participants                      |
| GET    | `/:id`                | Single call (must be a participant)                                        |

---

## Translations (`/api/v1/translations`)

| Method | Path                              | Description                                |
|--------|-----------------------------------|--------------------------------------------|
| GET    | `/languages`                      | Public list of 30+ supported languages     |
| GET    | `/calls/:callId/transcript`       | Ordered transcript for a call              |
| GET    | `/calls/:callId/summary`          | Aggregate stats: segments, languages, avg latency |

---

## AI (`/api/v1/ai`)

| Method | Path           | Body                                                                                 |
|--------|----------------|--------------------------------------------------------------------------------------|
| POST   | `/transcribe`  | multipart with `audio` file + form fields `language`, `provider?`                    |
| POST   | `/translate`   | `{ text, source, target, provider? }` → `{ text, provider, latencyMs }`              |
| POST   | `/tts`         | `{ text, language, voice?, provider? }` → `{ audio: { data (base64), mimeType } }`   |
| POST   | `/pipeline`    | multipart `audio` + form `sourceLanguage`, `targetLanguage` — runs STT→Translate→TTS |

---

## Chat (`/api/v1/chat`)

| Method | Path                                  | Description                                |
|--------|---------------------------------------|--------------------------------------------|
| GET    | `/threads`                            | Threads for the current user               |
| POST   | `/threads`                            | `{ peerId }` → idempotently open a thread  |
| GET    | `/threads/:id/messages`               | Paged messages                             |
| POST   | `/threads/:id/messages`               | Send message (auto-translation supported)  |

---

## Meetings (`/api/v1/meetings`)

| Method | Path                  | Body                                                                |
|--------|-----------------------|---------------------------------------------------------------------|
| POST   | `/`                   | `{ title, scheduledAt?, defaultLanguage? }`                         |
| POST   | `/join`               | `{ meetingId?, joinCode?, language? }`                              |
| GET    | `/:id/transcript`     | Ordered segments                                                    |
| POST   | `/:id/summary`        | Generates an AI summary via GPT-4o-mini                             |

---

## Subscriptions (`/api/v1/subscriptions`)

| Method | Path           | Body                                                       |
|--------|----------------|------------------------------------------------------------|
| GET    | `/plans`       | Public plan catalog                                        |
| GET    | `/me`          | Current user's plan                                        |
| POST   | `/checkout`    | `{ plan: 'premium'\|'business', gateway: 'razorpay'\|'stripe' }` |

---

## Socket.io protocol

See [`backend/README.md`](../backend/README.md#realtime-protocol-socketio) for the full event reference.
