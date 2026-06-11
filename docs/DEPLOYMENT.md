# Production deployment

VoiceBridge AI ships with Docker images for the backend and the admin
dashboard, and Kubernetes manifests in `k8s/`. Pick whichever fits your
environment.

## Option 1 - Single VPS with docker compose

For a quick production pilot on a single Linux host:

```bash
git clone <repo> /opt/voicebridge && cd /opt/voicebridge
cp .env.example .env             
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

Place an Nginx or Caddy reverse proxy in front of the backend on port
443. Terminate TLS at the proxy and forward to `backend:4000`.

> Note: A `docker-compose.prod.yml` overlay is not included; recommended
> additions are: pin image versions, add `restart: always`, mount a
> letsencrypt volume on the proxy.

## Option 2 - Kubernetes

See [`k8s/`](../k8s) for example manifests:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/admin.yaml
kubectl apply -f k8s/ingress.yaml
```

Recommended cluster setup:
- 3 backend replicas behind a Service of type ClusterIP.
- Postgres as a managed offering (RDS / Cloud SQL) - the in-cluster
  manifest is for dev only.
- Redis as a managed offering or a Bitnami chart with persistence.
- Horizontal Pod Autoscaler on the backend keyed off CPU and the
  `socket_io_connected_total` metric.
- For Socket.io across replicas, install
  `@socket.io/redis-adapter` and wire it in `src/realtime/socket.js`.

## TURN server

Calls behind symmetric NAT (corporate / cellular) require a TURN server.
Use a managed offering like Twilio NTS, Cloudflare TURN, or self-host
`coturn`. Then set:

```
TURN_URL=turn:turn.example.com:3478?transport=udp
TURN_USERNAME=...
TURN_PASSWORD=...
```

These are returned by `/api/v1/calls/ice-servers` and used by every
client.

## Object storage

Set the `S3_*` variables (works with AWS S3, Cloudflare R2, Backblaze
B2, MinIO). The backend stores call recordings and chat media there.

## Mobile distribution

- **Android:** `flutter build appbundle --release`, upload to Play
  Console.
- **iOS:** `flutter build ipa --release`, upload via Xcode / Transporter.

Set release values at build time:

```bash
flutter build appbundle --release \
  --dart-define=API_BASE_URL=https://api.voicebridge.ai \
  --dart-define=SOCKET_URL=https://api.voicebridge.ai
```

## Observability

- Backend logs structured JSON via Pino. Forward stdout to your log
  aggregator (Loki, Datadog, CloudWatch).
- Add `prom-client` and expose `/metrics` for Prometheus when you scale
  beyond two replicas.
- Sentry / Bugsnag integration is a small addition - hook into Pino's
  error path in `middleware/error.js`.

## Backups

- Postgres: nightly `pg_dump` to cold storage; retain 30 days.
- Redis: persistence is enabled (`--appendonly yes`); back up
  `appendonly.aof` if you treat any data as durable.
- Recordings: lifecycle-rule to Glacier-class storage after 30 days.

## Compliance

- The codebase is GDPR-aware: `DELETE /api/v1/users/me` cascades all
  user data. Add export endpoints if you need DSARs.
- Configure your DPA with each AI provider you enable (OpenAI BAA,
  Azure DPA, etc).
