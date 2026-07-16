import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getSessionSeats, createBooking } from '../services/api';

function SeatSelection() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [seats, setSeats] = useState([]);
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
        user_id: 1, // Заглушка
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

  // Группируем места по рядам
  const rows = {};
  seats.forEach(seat => {
    if (!rows[seat.row]) rows[seat.row] = [];
    rows[seat.row].push(seat);
  });

  return (
    <div className="seat-selection">
      <h1>Выбор мест</h1>
      
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