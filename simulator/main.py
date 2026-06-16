import asyncio
import logging
import os
import random
import signal
from dataclasses import dataclass, field
from typing import Optional

import httpx


DEFAULT_API_URL = "http://api:8000/telemetry"
DEFAULT_VEHICLE_COUNT = 50
DEFAULT_SEND_INTERVAL_SECONDS = 2.0

BASE_LAT = 52.5200
BASE_LON = 13.4050

ALERT_MESSAGES = [
    "High battery drain detected",
    "Temperature threshold warning",
    "Unexpected speed spike",
    "Vehicle health degraded",
    "Critical telemetry anomaly detected",
]


def get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)

    if not value:
        return default

    try:
        parsed_value = int(value)
        if parsed_value <= 0:
            raise ValueError

        return parsed_value

    except ValueError:
        logging.warning(
            "Invalid value for %s=%s. Falling back to default: %s",
            name,
            value,
            default,
        )
        return default


def get_float_env(name: str, default: float) -> float:
    value = os.getenv(name)

    if not value:
        return default

    try:
        parsed_value = float(value)
        if parsed_value <= 0:
            raise ValueError

        return parsed_value

    except ValueError:
        logging.warning(
            "Invalid value for %s=%s. Falling back to default: %s",
            name,
            value,
            default,
        )
        return default


@dataclass
class Vehicle:
    vehicle_id: str
    lat: float
    lon: float
    battery_level: float = field(default_factory=lambda: random.uniform(70.0, 100.0))
    temperature: float = field(default_factory=lambda: random.uniform(24.0, 42.0))
    speed_kmh: float = field(default_factory=lambda: random.uniform(0.0, 90.0))
    health_status: str = "ok"
    alert: Optional[str] = None

    def update_state(self) -> None:
        self._move_vehicle()
        self._drain_battery()
        self._update_temperature()
        self._update_health_status()
        self._maybe_create_alert()

    def _move_vehicle(self) -> None:
        speed_change = random.uniform(-8.0, 10.0)
        self.speed_kmh = min(max(self.speed_kmh + speed_change, 0.0), 130.0)

        movement_factor = max(self.speed_kmh, 5.0) / 100.0

        lat_delta = random.uniform(-0.00035, 0.00035) * movement_factor
        lon_delta = random.uniform(-0.00035, 0.00035) * movement_factor

        self.lat += lat_delta
        self.lon += lon_delta

    def _drain_battery(self) -> None:
        base_drain = random.uniform(0.01, 0.06)
        speed_drain = self.speed_kmh / 5000
        temperature_drain = max(self.temperature - 45.0, 0.0) / 10000

        total_drain = base_drain + speed_drain + temperature_drain
        self.battery_level = max(self.battery_level - total_drain, 0.0)

    def _update_temperature(self) -> None:
        temperature_change = random.uniform(-0.5, 0.8)

        if self.speed_kmh > 100:
            temperature_change += random.uniform(0.1, 0.5)

        if self.battery_level < 20:
            temperature_change += random.uniform(0.0, 0.3)

        self.temperature = min(max(self.temperature + temperature_change, 15.0), 95.0)

    def _update_health_status(self) -> None:
        if self.battery_level <= 10 or self.temperature >= 80:
            self.health_status = "critical"
        elif self.battery_level <= 25 or self.temperature >= 65 or self.speed_kmh >= 115:
            self.health_status = "warning"
        else:
            self.health_status = "ok"

    def _maybe_create_alert(self) -> None:
        self.alert = None

        if self.health_status == "critical":
            self.alert = random.choice(ALERT_MESSAGES)
            return

        if self.health_status == "warning" and random.random() < 0.35:
            self.alert = random.choice(ALERT_MESSAGES)
            return

        if random.random() < 0.02:
            self.alert = random.choice(ALERT_MESSAGES)

    def to_payload(self) -> dict:
        return {
            "vehicle_id": self.vehicle_id,
            "lat": round(self.lat, 6),
            "lon": round(self.lon, 6),
            "battery_level": round(self.battery_level, 2),
            "temperature": round(self.temperature, 2),
            "speed_kmh": round(self.speed_kmh, 2),
            "health_status": self.health_status,
            "alert": self.alert,
        }


def create_vehicle(vehicle_number: int) -> Vehicle:
    return Vehicle(
        vehicle_id=f"vehicle-{vehicle_number:03d}",
        lat=BASE_LAT + random.uniform(-0.05, 0.05),
        lon=BASE_LON + random.uniform(-0.05, 0.05),
    )


async def send_telemetry(
    client: httpx.AsyncClient,
    vehicle: Vehicle,
    api_url: str,
    send_interval_seconds: float,
    shutdown_event: asyncio.Event,
) -> None:
    while not shutdown_event.is_set():
        vehicle.update_state()
        payload = vehicle.to_payload()

        try:
            response = await client.post(api_url, json=payload)
            response.raise_for_status()

            logging.info(
                "Sent telemetry | vehicle=%s | health=%s | battery=%s | speed=%s",
                payload["vehicle_id"],
                payload["health_status"],
                payload["battery_level"],
                payload["speed_kmh"],
            )

        except httpx.ConnectError:
            logging.warning(
                "API unavailable | vehicle=%s | api_url=%s",
                vehicle.vehicle_id,
                api_url,
            )

        except httpx.HTTPStatusError as error:
            logging.error(
                "API returned error | vehicle=%s | status_code=%s | response=%s",
                vehicle.vehicle_id,
                error.response.status_code,
                error.response.text,
            )

        except httpx.RequestError as error:
            logging.error(
                "Request failed | vehicle=%s | error=%s",
                vehicle.vehicle_id,
                str(error),
            )

        except Exception as error:
            logging.exception(
                "Unexpected simulator error | vehicle=%s | error=%s",
                vehicle.vehicle_id,
                str(error),
            )

        await asyncio.sleep(send_interval_seconds)


async def run_simulator() -> None:
    api_url = os.getenv("API_URL", DEFAULT_API_URL)
    vehicle_count = get_int_env("VEHICLE_COUNT", DEFAULT_VEHICLE_COUNT)
    send_interval_seconds = get_float_env(
        "SEND_INTERVAL_SECONDS",
        DEFAULT_SEND_INTERVAL_SECONDS,
    )

    logging.info("Starting AegisFleet vehicle simulator")
    logging.info("API_URL=%s", api_url)
    logging.info("VEHICLE_COUNT=%s", vehicle_count)
    logging.info("SEND_INTERVAL_SECONDS=%s", send_interval_seconds)

    shutdown_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, shutdown_event.set)
        except NotImplementedError:
            pass

    vehicles = [create_vehicle(index) for index in range(1, vehicle_count + 1)]

    timeout = httpx.Timeout(connect=3.0, read=5.0, write=5.0, pool=5.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [
            asyncio.create_task(
                send_telemetry(
                    client=client,
                    vehicle=vehicle,
                    api_url=api_url,
                    send_interval_seconds=send_interval_seconds,
                    shutdown_event=shutdown_event,
                )
            )
            for vehicle in vehicles
        ]

        await shutdown_event.wait()

        logging.info("Shutdown signal received. Stopping simulator...")

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

    logging.info("AegisFleet vehicle simulator stopped cleanly")


def configure_logging() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


if __name__ == "__main__":
    configure_logging()

    try:
        asyncio.run(run_simulator())
    except KeyboardInterrupt:
        logging.info("Simulator stopped by user")
