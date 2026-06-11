-- VoiceBridge AI - Initial schema
-- Run automatically on first container start by docker-entrypoint-initdb.d
-- For local dev: psql $DATABASE_URL -f migrations/001_init.sql

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- USERS
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
  id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name                    TEXT NOT NULL,
  email                   TEXT NOT NULL UNIQUE,
  phone                   TEXT UNIQUE,
  password_hash           TEXT,
  language                CHAR(2) NOT NULL DEFAULT 'en',
  avatar_url              TEXT,
  subscription_plan       TEXT NOT NULL DEFAULT 'free' CHECK (subscription_plan IN ('free','premium','business')),
  subscription_renews_at  TIMESTAMPTZ,
  email_verified          BOOLEAN NOT NULL DEFAULT FALSE,
  phone_verified          BOOLEAN NOT NULL DEFAULT FALSE,
  oauth_google_sub        TEXT,
  oauth_apple_sub         TEXT,
  last_login_at           TIMESTAMPTZ,
  created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_email_lower ON users (lower(email));

-- ============================================================================
-- CONTACTS
-- ============================================================================
CREATE TABLE IF NOT EXISTS contacts (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id           UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  contact_user_id   UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  alias             TEXT,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, contact_user_id),
  CHECK (user_id <> contact_user_id)
);

-- ============================================================================
-- CALLS
-- ============================================================================
CREATE TABLE IF NOT EXISTS calls (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  caller_id       UUID NOT NULL REFERENCES users(id) ON DELETE SET NULL,
  receiver_id     UUID REFERENCES users(id) ON DELETE SET NULL,
  type            TEXT NOT NULL DEFAULT 'voice' CHECK (type IN ('voice','video')),
  is_group        BOOLEAN NOT NULL DEFAULT FALSE,
  status          TEXT NOT NULL DEFAULT 'ringing'
                    CHECK (status IN ('ringing','active','ended','missed','rejected','failed')),
  start_time      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  end_time        TIMESTAMPTZ,
  duration_sec    INTEGER,
  recording_url   TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_calls_start_time ON calls (start_time DESC);
CREATE INDEX IF NOT EXISTS idx_calls_caller ON calls (caller_id);
CREATE INDEX IF NOT EXISTS idx_calls_receiver ON calls (receiver_id);

CREATE TABLE IF NOT EXISTS call_participants (
  call_id     UUID NOT NULL REFERENCES calls(id) ON DELETE CASCADE,
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  joined_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  left_at     TIMESTAMPTZ,
  language    CHAR(2),
  PRIMARY KEY (call_id, user_id)
);

-- ============================================================================
-- TRANSLATIONS (per-utterance log for live captions / transcripts)
-- ============================================================================
CREATE TABLE IF NOT EXISTS translations (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  call_id           UUID REFERENCES calls(id) ON DELETE CASCADE,
  meeting_id        UUID,
  speaker_id        UUID REFERENCES users(id) ON DELETE SET NULL,
  source_language   CHAR(2) NOT NULL,
  target_language   CHAR(2) NOT NULL,
  original_text     TEXT NOT NULL,
  translated_text   TEXT NOT NULL,
  audio_url         TEXT,
  provider          TEXT,
  latency_ms        INTEGER,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_translations_call ON translations (call_id, created_at);
CREATE INDEX IF NOT EXISTS idx_translations_meeting ON translations (meeting_id, created_at);

-- ============================================================================
-- CHAT
-- ============================================================================
CREATE TABLE IF NOT EXISTS chat_threads (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_a      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  user_b      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (user_a, user_b),
  CHECK (user_a < user_b)
);

CREATE TABLE IF NOT EXISTS chat_messages (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  thread_id         UUID NOT NULL REFERENCES chat_threads(id) ON DELETE CASCADE,
  sender_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type              TEXT NOT NULL DEFAULT 'text' CHECK (type IN ('text','voice','image','document')),
  text_original     TEXT,
  text_translated   TEXT,
  source_language   CHAR(2),
  target_language   CHAR(2),
  media_url         TEXT,
  delivered_at      TIMESTAMPTZ,
  read_at           TIMESTAMPTZ,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_chat_messages_thread ON chat_messages (thread_id, created_at);

-- ============================================================================
-- MEETINGS
-- ============================================================================
CREATE TABLE IF NOT EXISTS meetings (
  id                     UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  host_id                UUID NOT NULL REFERENCES users(id) ON DELETE SET NULL,
  title                  TEXT NOT NULL,
  scheduled_at           TIMESTAMPTZ,
  default_language       CHAR(2) NOT NULL DEFAULT 'en',
  join_code              TEXT UNIQUE,
  summary                TEXT,
  summary_generated_at   TIMESTAMPTZ,
  created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at             TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS meeting_participants (
  meeting_id   UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
  user_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  language     CHAR(2) NOT NULL DEFAULT 'en',
  joined_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  left_at      TIMESTAMPTZ,
  PRIMARY KEY (meeting_id, user_id)
);

CREATE TABLE IF NOT EXISTS meeting_segments (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  meeting_id        UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
  speaker_id        UUID REFERENCES users(id) ON DELETE SET NULL,
  speaker_name      TEXT,
  source_language   CHAR(2) NOT NULL,
  text_original     TEXT NOT NULL,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_meeting_segments_meeting ON meeting_segments (meeting_id, created_at);

-- ============================================================================
-- SUBSCRIPTIONS / BILLING
-- ============================================================================
CREATE TABLE IF NOT EXISTS subscription_events (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id           UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plan              TEXT NOT NULL,
  gateway           TEXT NOT NULL,
  gateway_event_id  TEXT,
  status            TEXT NOT NULL,
  amount_minor      INTEGER,
  currency          TEXT,
  raw_payload       JSONB,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_subscription_events_user ON subscription_events (user_id, created_at DESC);

-- ============================================================================
-- USAGE / ANALYTICS
-- ============================================================================
CREATE TABLE IF NOT EXISTS usage_daily (
  user_id          UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  day              DATE NOT NULL,
  call_seconds     INTEGER NOT NULL DEFAULT 0,
  translations     INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, day)
);
