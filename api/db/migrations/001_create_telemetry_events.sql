CREATE TABLE IF NOT EXISTS telemetry_events (
    id BIGSERIAL PRIMARY KEY,

    vehicle_id VARCHAR(100) NOT NULL,

    lat DOUBLE PRECISION NOT NULL CHECK (lat >= -90 AND lat <= 90),
    lon DOUBLE PRECISION NOT NULL CHECK (lon >= -180 AND lon <= 180),

    battery_level DOUBLE PRECISION NOT NULL CHECK (battery_level >= 0 AND battery_level <= 100),
    temperature DOUBLE PRECISION NOT NULL CHECK (temperature >= -50 AND temperature <= 120),
    speed_kmh DOUBLE PRECISION NOT NULL CHECK (speed_kmh >= 0 AND speed_kmh <= 300),

    health_status VARCHAR(50) NOT NULL,
    alert VARCHAR(200),

    received_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_telemetry_events_vehicle_id
ON telemetry_events (vehicle_id);

CREATE INDEX IF NOT EXISTS idx_telemetry_events_received_at
ON telemetry_events (received_at DESC);

CREATE INDEX IF NOT EXISTS idx_telemetry_events_vehicle_received_at
ON telemetry_events (vehicle_id, received_at DESC);
