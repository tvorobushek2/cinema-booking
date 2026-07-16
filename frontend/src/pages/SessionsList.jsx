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
    <div className="sessions-list">
      <h1>Сеансы</h1>
      <div className="sessions-grid">
        {sessions.map(session => (
          <div key={session.id} className="session-card">
            <h2>{session.title}</h2>
            <p className="session-info">
              <strong>Зал:</strong> {session.hall_name}
            </p>
            <p className="session-info">
              <strong>Время:</strong> {new Date(session.started_at).toLocaleString('ru-RU')}
            </p>
            <p className="session-info">
              <strong>Длительность:</strong> {session.duration} мин
            </p>
            <Link to={`/sessions/${session.id}/seats`} className="btn">
              Выбрать места
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SessionsList;