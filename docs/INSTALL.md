# Local installation

## Prerequisites

- Node.js 20+ and npm
- Docker + Docker Compose (recommended)
- Flutter 3.22+ (for the mobile app)
- PostgreSQL 16 + Redis 7 (if running outside Docker)

## 1. Clone & configure

```bash
git clone https://github.com/your-org/voicebridge-ai.git
cd voicebridge-ai

cp .env.example .env
cp backend/.env.example backend/.env

# Open .env and fill at minimum:
#   POSTGRES_PASSWORD, JWT_SECRET, JWT_REFRESH_SECRET
#   At least one AI provider key (OPENAI_API_KEY recommended)
```

## 2. Start backend + admin + Postgres + Redis with Docker

```bash
docker compose up -d
```

The first time Postgres starts, it auto-applies everything under
`backend/migrations/` thanks to `docker-entrypoint-initdb.d`, including
the schema and seed users (password `Password123!`).

Verify:

```bash
curl http://localhost:4000/health
# → { "status": "ok", "ts": "..." }
```

Open the admin dashboard at <http://localhost:3000>.

## 3. Mobile app

```bash
cd mobile
flutter create --platforms=android,ios .   # generate native folders (one-time)
flutter pub get
flutter run \
  --dart-define=API_BASE_URL=http://10.0.2.2:4000 \
  --dart-define=SOCKET_URL=http://10.0.2.2:4000
```

- `10.0.2.2` is the Android emulator's alias for the host machine.
- iOS simulator: use `http://localhost:4000`.
- Physical device: use your machine's LAN IP and make sure the firewall
  allows incoming TCP on port 4000.

## 4. Local backend without Docker

```bash
cd backend
npm install
createdb voicebridge
psql voicebridge -f migrations/001_init.sql
psql voicebridge -f migrations/002_seed.sql
DATABASE_URL=postgres://localhost:5432/voicebridge \
  REDIS_URL=redis://localhost:6379 \
  npm run dev
```

## 5. AI provider keys

The default providers expect these environment variables:

| Provider     | Variable                                            |
|--------------|-----------------------------------------------------|
| OpenAI       | `OPENAI_API_KEY` (used for Whisper STT + GPT translate) |
| Deepgram     | `DEEPGRAM_API_KEY`                                  |
| Google       | `GOOGLE_TRANSLATE_KEY`, `GOOGLE_TTS_KEY`, `GOOGLE_SPEECH_KEY` |
| DeepL        | `DEEPL_API_KEY`                                     |
| Azure        | `AZURE_TRANSLATOR_KEY`, `AZURE_TRANSLATOR_REGION`, `AZURE_TTS_KEY`, `AZURE_TTS_REGION` |
| ElevenLabs   | `ELEVENLABS_API_KEY`                                |

Switch the active provider with:

```
STT_PROVIDER=openai|deepgram
TRANSLATE_PROVIDER=openai|google|deepl|azure
TTS_PROVIDER=elevenlabs|azure|google
```

## 6. Demo accounts

Seeded by `migrations/002_seed.sql`:

| Email                          | Password         | Language | Plan      |
|--------------------------------|------------------|----------|-----------|
| `demo.mr@voicebridge.ai`       | `Password123!`   | Marathi  | premium   |
| `demo.en@voicebridge.ai`       | `Password123!`   | English  | premium   |
| `demo.hi@voicebridge.ai`       | `Password123!`   | Hindi    | free      |
