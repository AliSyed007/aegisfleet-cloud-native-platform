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
