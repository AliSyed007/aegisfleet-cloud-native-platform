import os

import psycopg


def get_database_config():
    config = {
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT"),
        "connect_timeout": 5,
    }

    missing_values = [
        key
        for key, value in config.items()
        if value is None and key != "connect_timeout"
    ]

    if missing_values:
        raise RuntimeError(
            "Missing required database environment variables: "
            + ", ".join(missing_values)
        )

    return config


def get_database_connection():
    return psycopg.connect(**get_database_config())


def save_telemetry_event(telemetry_data):
    insert_query = """
        INSERT INTO telemetry_events (
            vehicle_id,
            lat,
            lon,
            battery_level,
            temperature,
            speed_kmh,
            health_status,
            alert,
            received_at
        )
        VALUES (
            %(vehicle_id)s,
            %(lat)s,
            %(lon)s,
            %(battery_level)s,
            %(temperature)s,
            %(speed_kmh)s,
            %(health_status)s,
            %(alert)s,
            %(received_at)s
        )
        RETURNING id;
    """

    with get_database_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(insert_query, telemetry_data)
            telemetry_event_id = cur.fetchone()[0]

    return telemetry_event_id
