# Security

## Identity

- Passwords hashed with bcrypt (cost factor 12).
- JWT access tokens (15 min) + refresh tokens (30 days) signed with
  separate secrets (`JWT_SECRET`, `JWT_REFRESH_SECRET`).
- Refresh tokens are persisted only on the client (encrypted storage on
  mobile via Keychain / EncryptedSharedPreferences). Rotate by calling
  `/api/v1/auth/refresh`.
- OTP codes live in Redis with a 5-minute TTL and are single-use.
- OAuth verification (Google, Apple) is wired but stubbed; integrate
  `google-auth-library` / `apple-signin-auth` in production.

## Transport

- TLS 1.2+ everywhere. Terminate at the load balancer / ingress.
- HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy via
  `helmet` (`backend/src/app.js`).
- CORS allow-list driven by `CORS_ORIGINS`.

## Application

- All inputs validated with Joi (`middleware/validate.js`).
- Rate limiting per IP, stricter on `/auth/*` than the rest of `/api/*`.
- WebSocket connections require a valid JWT in the handshake (see
  `realtime/socket.js`). Connections without it are rejected.

## Storage

- AES-256-GCM helper in `utils/crypto.js` for column-level encryption
  (use it for PII and recording URLs in regulated deployments).
- Postgres role used by the backend should have least-privilege on
  application tables only.
- Recordings live in S3-compatible storage. Use bucket policies + KMS
  keys for encryption at rest.

## Media

- WebRTC calls are end-to-end encrypted with DTLS-SRTP between peers in
  the default mesh topology.
- When routing through a SFU (planned for groups > 4), the SFU
  decrypts/re-encrypts media; protect that hop with mutual TLS and
  short-lived TURN credentials.
- Live captions and translated audio flow over our Socket.io connection
  (TLS terminated at the LB). They never persist unless the call is
  explicitly recorded.

## Compliance

- GDPR: `DELETE /api/v1/users/me` cascades all user data through FK
  constraints in the schema.
- HIPAA: not in scope for v1; if needed, sign a BAA with the AI
  providers (OpenAI offers one) and enable per-row encryption.
- Children: enforce a self-attested 13+ age gate on signup.

## Operational

- Secrets in environment variables only - never committed.
- Production deployments should rotate JWT secrets at least quarterly
  (existing tokens continue to validate against the previous secret if
  you implement a two-key window).
- Enable audit logging on AI providers where available (OpenAI
  organization activity, Azure Diagnostic Settings).

## Known gaps to address before public launch

- [ ] OAuth verifier implementation
- [ ] Email/SMS provider integration for OTP (Twilio / Msg91 / SES /
      SendGrid)
- [ ] Razorpay & Stripe webhook handlers
- [ ] CSRF tokens on browser-facing flows
- [ ] Per-organization data isolation for the Business plan
- [ ] Pen-test against `/api/v1/calls/*` for IDOR
