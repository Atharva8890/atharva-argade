-- Seed data for local development.
-- Default password for all seed users: "Password123!" (bcrypt hash below).

INSERT INTO users (id, name, email, language, subscription_plan, password_hash, email_verified)
VALUES
  (uuid_generate_v4(), 'Demo Marathi User', 'demo.mr@voicebridge.ai', 'mr', 'premium',
    '$2b$12$NMcCwbFnxLgY9w8GMYpUW.GdVXMpcw43O8ZL7sFNcXt6BLLLYL8EW', TRUE),
  (uuid_generate_v4(), 'Demo English User', 'demo.en@voicebridge.ai', 'en', 'premium',
    '$2b$12$NMcCwbFnxLgY9w8GMYpUW.GdVXMpcw43O8ZL7sFNcXt6BLLLYL8EW', TRUE),
  (uuid_generate_v4(), 'Demo Hindi User', 'demo.hi@voicebridge.ai', 'hi', 'free',
    '$2b$12$NMcCwbFnxLgY9w8GMYpUW.GdVXMpcw43O8ZL7sFNcXt6BLLLYL8EW', TRUE)
ON CONFLICT (email) DO NOTHING;
