import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getSessionSeats, createBooking, getSessions } from '../services/api';
import './SessionsList.css';

function SeatSelection() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [seats, setSeats] = useState([]);
  const [sessionInfo, setSessionInfo] = useState(null);
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSeats();
  }, [sessionId]);

const fetchSeats = async () => {
  try {
    const response = await getSessionSeats(sessionId);
    setSeats(response.data);
    
    // Получаем информацию о сеансе
    const sessionsResponse = await getSessions();
    const session = sessionsResponse.data.find(s => s.id === parseInt(sessionId));
    setSessionInfo(session);
    
    setLoading(false);
  } catch (err) {
    setError('Ошибка загрузки мест');
    setLoading(false);
  }
};

  const toggleSeat = (seat) => {
    if (seat.status === 'taken') return;

    setSelectedSeats(prev => {
      const isSelected = prev.find(s => s.seat_id === seat.seat_id);
      if (isSelected) {
        return prev.filter(s => s.seat_id !== seat.seat_id);
      } else {
        return [...prev, seat];
      }
    });
  };

  const handleBooking = async () => {
    if (selectedSeats.length === 0) {
      alert('Выберите хотя бы одно место');
      return;
    }

    try {
      const response = await createBooking({
        user_id: 1,
        session_id: parseInt(sessionId),
        seat_ids: selectedSeats.map(s => s.seat_id)
      });

      alert(`Бронь создана! ID: ${response.data.booking_ids.join(', ')}`);
      navigate('/');
    } catch (err) {
      alert('Ошибка создания брони');
    }
  };

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;

  const rows = {};
  seats.forEach(seat => {
    if (!rows[seat.row]) rows[seat.row] = [];
    rows[seat.row].push(seat);
  });

  return (
    <div className="seat-selection">
      <h1>Выбор мест</h1>
      {/* Постер фильма */}
{sessionInfo && (
  <div className="movie-poster">
    {sessionInfo.poster ? (
      <img src={sessionInfo.poster} alt={sessionInfo.title} />
    ) : (
      <div className="poster-placeholder"></div>
    )}
    <div className="movie-info">
      <h2>{sessionInfo.title}</h2>
      <p>{sessionInfo.hall_name} • {sessionInfo.duration} мин</p>
      <p>{new Date(sessionInfo.started_at).toLocaleString('ru-RU', {
        day: 'numeric',
        month: 'long',
        hour: '2-digit',
        minute: '2-digit'
      })}</p>
    </div>
  </div>
)}
      <div className="screen">ЭКРАН</div>

      <div className="seats-container">
        {Object.keys(rows).sort((a, b) => a - b).map(rowNum => (
          <div key={rowNum} className="seat-row">
            <span className="row-number">Ряд {rowNum}</span>
            <div className="seats">
              {rows[rowNum].map(seat => (
                <button
                  key={seat.seat_id}
                  className={`seat ${seat.type} ${seat.status} ${
                    selectedSeats.find(s => s.seat_id === seat.seat_id) ? 'selected' : ''
                  }`}
                  onClick={() => toggleSeat(seat)}
                  disabled={seat.status === 'taken'}
                  title={`Место ${seat.number} - ${seat.price}₽`}
                >
                  {seat.number}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="seat-legend">
        <div className="legend-item">
          <div className="legend-seat free"></div>
          <span>Свободно</span>
        </div>
        <div className="legend-item">
          <div className="legend-seat vip"></div>
          <span>VIP</span>
        </div>
        <div className="legend-item">
          <div className="legend-seat taken"></div>
          <span>Занято</span>
        </div>
        <div className="legend-item">
          <div className="legend-seat selected"></div>
          <span>Выбрано</span>
        </div>
      </div>

      <div className="booking-summary">
        <h3>Выбрано мест: {selectedSeats.length}</h3>
        <p className="total-price">
          Итого: {selectedSeats.reduce((sum, seat) => sum + parseFloat(seat.price), 0)}₽
        </p>
        <button className="btn btn-primary" onClick={handleBooking}>
          Забронировать
        </button>
      </div>
    </div>
  );
}

export default SeatSelection;