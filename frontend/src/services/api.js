import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Получить список сеансов
export const getSessions = () => api.get('/sessions/');

// Получить схему зала
export const getSessionSeats = (sessionId) => api.get(`/sessions/${sessionId}/seats/`);

// Создать бронь
export const createBooking = (data) => api.post('/bookings/', data);

// Оплатить бронь
export const payBooking = (bookingId) => api.post(`/bookings/${bookingId}/pay/`);

// Продлить бронь
export const extendBooking = (bookingId) => api.post(`/bookings/${bookingId}/extend/`);

export default api;