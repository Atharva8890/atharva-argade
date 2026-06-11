# VoiceBridge AI - Admin

Next.js 14 (App Router) operations dashboard for VoiceBridge AI.

```bash
cd admin
npm install
NEXT_PUBLIC_API_URL=http://localhost:4000 npm run dev
```

Open <http://localhost:3000>. The dashboard reads `${NEXT_PUBLIC_API_URL}/health` server-side to display backend status, and renders mocked metrics that you can wire to real `/api/v1/...` endpoints next.

Build a production image with the included multi-stage `Dockerfile`.
