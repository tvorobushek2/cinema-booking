-- ==========================================
-- СХЕМА БАЗЫ ДАННЫХ CINEMA BOOKING
-- PostgreSQL
-- ==========================================

-- 1. Залы
CREATE TABLE halls (
    id SERIAL PRIMARY KEY,
    number INTEGER NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL
);

-- 2. Ряды
CREATE TABLE rows (
    id SERIAL PRIMARY KEY,
    hall_id INTEGER NOT NULL REFERENCES halls(id) ON DELETE CASCADE,
    number INTEGER NOT NULL,
    UNIQUE (hall_id, number)
);

-- 3. Места
CREATE TABLE seats (
    id SERIAL PRIMARY KEY,
    row_id INTEGER NOT NULL REFERENCES rows(id) ON DELETE CASCADE,
    number INTEGER NOT NULL,
    type VARCHAR(10) NOT NULL DEFAULT 'standard' CHECK (type IN ('standard', 'vip')),
    price DECIMAL(10,2) NOT NULL,
    UNIQUE (row_id, number)
);

-- 4. Сеансы
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    hall_id INTEGER NOT NULL REFERENCES halls(id) ON DELETE RESTRICT,
    title VARCHAR(200) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    duration INTEGER NOT NULL
);

-- 5. Брони
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    seat_id INTEGER NOT NULL REFERENCES seats(id) ON DELETE CASCADE,
    status VARCHAR(10) NOT NULL CHECK (status IN ('awaiting', 'paid', 'expired')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL
);

-- ==========================================
-- ИНДЕКСЫ
-- ==========================================

CREATE INDEX idx_sessions_hall ON sessions(hall_id);
CREATE INDEX idx_bookings_session ON bookings(session_id);
CREATE INDEX idx_bookings_expires ON bookings(expires_at) WHERE status = 'awaiting';

-- Защита от дублей на уровне БД
CREATE UNIQUE INDEX idx_active_booking 
ON bookings(session_id, seat_id) 
WHERE status IN ('awaiting', 'paid');