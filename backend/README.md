# VoiceBridge AI - Backend

Node.js 20 + Express + Socket.io + PostgreSQL 16 + Redis 7 API powering the VoiceBridge AI mobile and web clients.

## Run locally

```bash
cd backend
cp .env.example .env
npm install
npm run dev
```

Or via Docker Compose from the repo root: `docker compose up -d`.

## Scripts

| Command          | Purpose                                                   |
|------------------|-----------------------------------------------------------|
| `npm run dev`    | Hot-reloading dev server with `nodemon`                   |
| `npm start`      | Production start                                          |
| `npm run migrate`| Apply SQL migrations from `./migrations`                  |
| `npm run lint`   | ESLint                                                    |
| `npm test`       | Jest                                                      |

## Layout

```
src/
├── app.js                  Express app composition
├── index.js                Bootstrap + graceful shutdown
├── config/                 env, pg pool, redis client
├── middleware/             auth, validation, rate-limit, error
├── modules/                Feature modules (HTTP routes + services)
│   ├── auth/
│   ├── users/
│   ├── calls/
│   ├── translations/
│   ├── ai/                 STT / Translate / TTS provider abstraction
│   ├── chat/
│   ├── meetings/
│   └── subscriptions/
├── realtime/               Socket.io: WebRTC signaling + live translation
└── utils/                  jwt, crypto, otp, logger, languages
migrations/                 SQL migrations + seed
```

## Realtime protocol (Socket.io)

Authenticate by sending `{ auth: { token } }` on connection. Then:

| Event (in)            | Payload                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `call:invite`         | `{ callId, peerIds: string[] }`                                         |
| `call:join`           | `{ callId }` → ack `{ iceServers }`                                     |
| `call:leave`          | `{ callId }`                                                            |
| `call:end`            | `{ callId }`                                                            |
| `webrtc:offer/answer` | `{ callId, to, sdp }`                                                   |
| `webrtc:ice`          | `{ callId, to, candidate }`                                             |
| `translate:chunk`     | `{ callId, chunk(base64), mimeType, sourceLanguage, targets: [...] }`   |
| `translate:text`      | `{ callId, text, sourceLanguage, targets: [...] }`                      |

| Event (out)           | Payload                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `call:incoming`       | `{ callId, from, startedAt }`                                           |
| `call:ended`          | `{ callId, durationSec }`                                               |
| `peer:joined/left`    | `{ userId }`                                                            |
| `peer:muted`          | `{ userId, muted }`                                                     |
| `caption:original`    | `{ callId, speakerId, text, language, ts }`                             |
| `caption:translated`  | `{ callId, speakerId, text, language, ts }`                             |
| `audio:translated`    | `{ callId, speakerId, audio (base64), mimeType, language }`             |
