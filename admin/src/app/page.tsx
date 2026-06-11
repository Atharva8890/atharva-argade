import styles from './page.module.css';

async function fetchHealth(): Promise<{ status: string; ts?: string } | null> {
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
  try {
    const res = await fetch(`${api}/health`, { cache: 'no-store' });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

const metrics = [
  { label: 'Active calls', value: '124', delta: '+12%', positive: true },
  { label: 'Translations / min', value: '8,420', delta: '+5.4%', positive: true },
  { label: 'Daily active users', value: '34,201', delta: '+2.1%', positive: true },
  { label: 'P95 round-trip', value: '480 ms', delta: '-30 ms', positive: true },
];

const recentCalls = [
  { id: 'c_8a91', caller: 'Priya P.', langs: 'mr → en', duration: '08:14', status: 'completed' },
  { id: 'c_8a90', caller: 'Raj M.', langs: 'hi → en', duration: '03:42', status: 'completed' },
  { id: 'c_8a8f', caller: 'Yuki T.', langs: 'ja → en', duration: '12:09', status: 'completed' },
  { id: 'c_8a8e', caller: 'Anna M.', langs: 'de → en', duration: '00:34', status: 'missed' },
];

export default async function AdminHome() {
  const health = await fetchHealth();
  return (
    <main className={styles.shell}>
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <div className={styles.logo}>VB</div>
          <div>
            <div className={styles.brandName}>VoiceBridge</div>
            <div className={styles.brandSub}>Admin</div>
          </div>
        </div>
        <nav className={styles.nav}>
          <a className={styles.active}>Overview</a>
          <a>Users</a>
          <a>Calls</a>
          <a>Translations</a>
          <a>Meetings</a>
          <a>Subscriptions</a>
          <a>AI providers</a>
          <a>Settings</a>
        </nav>
        <div className={styles.healthBox}>
          <div className={styles.healthLabel}>Backend</div>
          <div className={`${styles.healthValue} ${health?.status === 'ok' ? styles.ok : styles.bad}`}>
            {health?.status === 'ok' ? 'Healthy' : 'Unreachable'}
          </div>
        </div>
      </aside>
      <section className={styles.main}>
        <header className={styles.header}>
          <div>
            <h1>Overview</h1>
            <p>Real-time operations across calls, translations, and infrastructure.</p>
          </div>
          <button className={styles.cta}>Export report</button>
        </header>

        <div className={styles.metrics}>
          {metrics.map((m) => (
            <div className={styles.metric} key={m.label}>
              <div className={styles.metricLabel}>{m.label}</div>
              <div className={styles.metricValue}>{m.value}</div>
              <div className={`${styles.metricDelta} ${m.positive ? styles.up : styles.down}`}>{m.delta}</div>
            </div>
          ))}
        </div>

        <div className={styles.row}>
          <div className={styles.card}>
            <div className={styles.cardHead}>
              <h2>Recent calls</h2>
              <a className={styles.link}>View all</a>
            </div>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Caller</th>
                  <th>Languages</th>
                  <th>Duration</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recentCalls.map((c) => (
                  <tr key={c.id}>
                    <td>{c.id}</td>
                    <td>{c.caller}</td>
                    <td>{c.langs}</td>
                    <td>{c.duration}</td>
                    <td>
                      <span
                        className={`${styles.tag} ${c.status === 'missed' ? styles.tagDanger : styles.tagSuccess}`}
                      >
                        {c.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className={styles.card}>
            <div className={styles.cardHead}>
              <h2>AI providers</h2>
            </div>
            <ul className={styles.providers}>
              <li><span>STT</span><b>OpenAI Whisper</b><i className={styles.dotOk} /></li>
              <li><span>Translate</span><b>OpenAI GPT-4o-mini</b><i className={styles.dotOk} /></li>
              <li><span>TTS</span><b>ElevenLabs Multilingual v2</b><i className={styles.dotOk} /></li>
              <li><span>Fallback STT</span><b>Deepgram nova-2</b><i className={styles.dotWarn} /></li>
              <li><span>Fallback Translate</span><b>DeepL</b><i className={styles.dotOk} /></li>
            </ul>
          </div>
        </div>
      </section>
    </main>
  );
}
