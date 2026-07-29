import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { HEALTH_ENDPOINT, SUPPORTED_GESTURES } from './utils/constants';

/**
 * App Component - Phase 1 Engineering Foundation
 */
export default function App() {
  const [healthStatus, setHealthStatus] = useState({ status: 'checking', service: '', version: '' });

  useEffect(() => {
    // Check backend health endpoint on startup
    axios
      .get(HEALTH_ENDPOINT)
      .then((res) => {
        setHealthStatus(res.data);
      })
      .catch((err) => {
        setHealthStatus({ status: 'error', service: 'Speak-without-voice', version: '1.0.0' });
      });
  }, []);

  return (
    <div style={{ padding: '32px', maxWidth: '1200px', margin: '0 auto', width: '100%' }}>
      {/* Header Container */}
      <header
        className="glass-panel"
        style={{
          padding: '24px',
          marginBottom: '32px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '28px', color: 'var(--text-primary)' }}>
            Speak-without-voice
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginTop: '4px' }}>
            Real-Time AI Sign Language Recognition System
          </p>
        </div>

        {/* Backend Health Badge */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Backend API:</span>
          <span
            style={{
              padding: '6px 16px',
              borderRadius: '9999px',
              fontSize: '13px',
              fontWeight: 600,
              backgroundColor:
                healthStatus.status === 'healthy'
                  ? 'rgba(16, 185, 129, 0.15)'
                  : 'rgba(244, 63, 94, 0.15)',
              color: healthStatus.status === 'healthy' ? 'var(--accent-emerald)' : 'var(--accent-rose)',
              border: `1px solid ${
                healthStatus.status === 'healthy'
                  ? 'rgba(16, 185, 129, 0.3)'
                  : 'rgba(244, 63, 94, 0.3)'
              }`,
            }}
          >
            {healthStatus.status === 'healthy' ? '● Connected (200 OK)' : '○ Offline / Standing By'}
          </span>
        </div>
      </header>

      {/* Main Foundation Banner Card */}
      <main className="glass-panel" style={{ padding: '32px' }}>
        <h2 style={{ fontFamily: 'var(--font-display)', color: 'var(--accent-cyan)', marginBottom: '16px' }}>
          Phase 1 Foundation Active
        </h2>
        <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '24px' }}>
          The engineering infrastructure, environment configurations, structured logging, global exception handling, and FastAPI health check endpoints are fully initialized.
        </p>

        <h3 style={{ fontSize: '16px', color: 'var(--text-primary)', marginBottom: '12px' }}>
          Target Gestures Blueprint (Phase 2-5):
        </h3>
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          {SUPPORTED_GESTURES.map((gesture) => (
            <span
              key={gesture}
              style={{
                padding: '8px 16px',
                borderRadius: '8px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-glass)',
                color: 'var(--text-primary)',
                fontSize: '14px',
              }}
            >
              {gesture}
            </span>
          ))}
        </div>
      </main>
    </div>
  );
}
