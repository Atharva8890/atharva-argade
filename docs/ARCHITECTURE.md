# Architecture

## High-level view

```
┌──────────────────┐        WebRTC (mesh/SFU)         ┌──────────────────┐
│  Flutter mobile  │ ◀──────────── audio ───────────▶ │  Flutter mobile  │
│   (User A)       │                                  │   (User B)       │
└────────┬─────────┘                                  └────────┬─────────┘
         │  Socket.io (signaling + captions + audio)           │
         ▼                                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                  Node.js backend (Express + Socket.io)               │
│   ┌──────────────┐  ┌──────────────┐  ┌────────────────────────────┐ │
│   │  REST API    │  │ Realtime hub │  │   AI pipeline orchestrator │ │
│   │ /api/v1/*    │  │  Socket.io   │  │  STT → Translate → TTS     │ │
│   └─────┬────────┘  └──────┬───────┘  └────┬──────────┬────────────┘ │
│         ▼                  ▼               ▼          ▼              │
│   PostgreSQL          Redis (pubsub /  OpenAI / Whisper   ElevenLabs │
│   (durable state)     OTP / queues)    / Deepgram         Azure TTS  │
└──────────────────────────────────────────────────────────────────────┘
```

## Translation pipeline

Each speaker streams short PCM/Opus chunks (≈300–800 ms) over Socket.io
via the `translate:chunk` event. For each chunk the backend runs:

1. **Speech-to-text** (default Whisper-1; fallback Deepgram). The chunk is
   passed with the speaker's source language hint to reduce latency.
2. **Translation** (default GPT-4o-mini; fallback DeepL or Google) per
   listener's preferred target language. We use a short system prompt
   that asks the model to preserve register and named entities, and we
   keep the prior 3-5 utterances as context for terminology stability
   (smart translation context memory).
3. **Text-to-speech** (default ElevenLabs multilingual v2; fallback
   Azure neural TTS) per target language. Optional voice cloning lets
   us preserve the speaker's tone.

The original transcript and the translated audio (base64) are broadcast
back to each peer over the same Socket.io connection. Captions are also
persisted in `translations` so the transcript view, summary, and
analytics can use them.

## Modules

| Module        | Purpose                                                                |
|---------------|------------------------------------------------------------------------|
| `auth`        | JWT issuance, OTP, OAuth (Google/Apple), forgot/reset password         |
| `users`       | Profile CRUD, contact list                                             |
| `calls`       | Initiate, end, history; ICE servers; participants                      |
| `translations`| Per-utterance log; transcript & summary endpoints                      |
| `ai`          | STT, Translate, TTS provider abstraction + REST endpoints              |
| `chat`        | Threads, messages, auto-translation                                    |
| `meetings`    | Multi-language rooms, segments, AI-generated summaries                 |
| `subscriptions`| Plans, Razorpay + Stripe checkout                                     |
| `realtime`    | Socket.io signaling + live-translation stream                          |

## Scaling notes

- **Stateless API:** Backend instances share state via Postgres + Redis,
  so we can scale horizontally behind any L7 load balancer.
- **Realtime fan-out:** For multi-instance Socket.io, plug in the Redis
  adapter (`@socket.io/redis-adapter`) - the connection wiring in
  `src/realtime/socket.js` already speaks to Redis.
- **WebRTC at scale:** The current signaling assumes mesh topology (fine
  for 1:1 and small groups). For meetings with >4 participants, route
  media through a SFU (LiveKit / mediasoup / Janus) and keep our
  Socket.io as the signaling channel - the protocol does not change.
- **AI:** Provider selection per request gives natural support for
  shadow traffic, regional providers (Azure in EU, Google in APAC), and
  bursty workloads.
- **Recording:** Backend writes call mixes to S3-compatible storage
  (`S3_*` env vars). For privacy-first deployments, encrypt with a
  per-user KMS key.

## Security model

- TLS everywhere (terminated at the LB / ingress).
- Passwords hashed with bcrypt (cost 12).
- JWT access (15 m) + refresh (30 d) signed with separate secrets.
- AES-256-GCM helper (`utils/crypto.js`) for any column-level encryption
  (e.g. recording URLs, PII).
- Rate limiting per IP, stricter on `/auth/*`.
- All Socket.io connections authenticate via JWT in the handshake.
- See [`SECURITY.md`](SECURITY.md) for the full threat model.
