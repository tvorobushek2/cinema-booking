import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getSessions } from '../services/api';

function SessionsList() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await getSessions();
      setSessions(response.data);
      setLoading(false);
    } catch (err) {
      setError('Ошибка загрузки сеансов');
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div style={{
      minHeight: '100vh',
      padding: '60px 20px',
      background: 'transparent'
    }}>
      <h1 style={{
        textAlign: 'center',
        fontSize: '3.5rem',
        marginBottom: '60px',
        color: '#ffffff',
        fontWeight: '800'
      }}>
        🎬 Сеансы
      </h1>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(450px, 1fr))',
        gap: '40px',
        maxWidth: '1600px',
        margin: '0 auto'
      }}>
        {sessions.map(session => (
          <div key={session.id} style={{
            background: 'rgba(30, 41, 59, 0.8)',
            backdropFilter: 'blur(15px)',
            borderRadius: '24px',
            padding: '40px',
            boxShadow: '0 15px 50px rgba(220, 38, 38, 0.3)',
            border: '2px solid rgba(220, 38, 38, 0.4)',
            minHeight: '400px',
            transition: 'all 0.4s ease'
          }}>
            <h2 style={{
              color: '#ffffff',
              fontSize: '2rem',
              marginBottom: '25px',
              fontWeight: '700'
            }}>
              {session.title}
            </h2>
            <p style={{
              display: 'flex',
              margin: '15px 0',
              fontSize: '16px',
              color: '#e2e8f0'
            }}>
              <strong style={{
                color: '#dc2626',
                marginRight: '10px',
                minWidth: '120px',
                fontWeight: '600'
              }}>
                🎭 Зал:
              </strong>
              {session.hall_name}
            </p>
            <p style={{
              display: 'flex',
              margin: '15px 0',
              fontSize: '16px',
              color: '#e2e8f0'
            }}>
              <strong style={{
                color: '#dc2626',
                marginRight: '10px',
                minWidth: '120px',
                fontWeight: '600'
              }}>
                ⏰ Время:
              </strong>
              {new Date(session.started_at).toLocaleString('ru-RU')}
            </p>
            <p style={{
              display: 'flex',
              margin: '15px 0',
              fontSize: '16px',
              color: '#e2e8f0'
            }}>
              <strong style={{
                color: '#dc2626',
                marginRight: '10px',
                minWidth: '120px',
                fontWeight: '600'
              }}>
                ⏱ Длительность:
              </strong>
              {session.duration} мин
            </p>
            <Link 
              to={`/sessions/${session.id}/seats`}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '18px 32px',
                background: 'linear-gradient(135deg, #dc2626 0%, #ef4444 100%)',
                color: '#ffffff',
                textDecoration: 'none',
                borderRadius: '14px',
                border: '2px solid rgba(255, 255, 255, 0.3)',
                fontSize: '18px',
                fontWeight: '700',
                marginTop: '25px',
                boxShadow: '0 6px 20px rgba(220, 38, 38, 0.4)'
              }}
            >
              Выбрать места →
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SessionsList;