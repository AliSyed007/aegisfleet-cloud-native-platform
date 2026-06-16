import logging
from datetime import datetime, timezone
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from pydantic import BaseModel, Field, field_validator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("aegisfleet-api")


app = FastAPI(
    title="AegisFleet API",
    description="Real-time fleet intelligence backend API",
    version="0.1.0",
)

telemetry_events_received = Counter(
    "telemetry_events_received_total",
    "Total number of telemetry events received by the API",
)

active_vehicles = Gauge(
    "active_vehicles",
    "Current number of vehicles with latest telemetry state",
)

alerts_count = Counter(
    "alerts_count",
    "Total number of telemetry events where alert is present",
)

LOW_BATTERY_THRESHOLD = 25.0

low_battery_vehicles = Gauge(
    "low_battery_vehicles",
    "Current number of vehicles with battery level below threshold",
)

unhealthy_vehicles = Gauge(
    "unhealthy_vehicles",
    "Current number of vehicles whose latest health status is not healthy",
)


class TelemetryPayload(BaseModel):
    vehicle_id: str = Field(..., min_length=1, max_length=100)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    battery_level: float = Field(..., ge=0, le=100)
    temperature: float = Field(..., ge=-50, le=120)
    speed_kmh: float = Field(..., ge=0, le=300)
    health_status: str = Field(..., min_length=1, max_length=50)
    alert: Optional[str] = Field(default=None, max_length=200)

    @field_validator("health_status", mode="before")
    @classmethod
    def normalize_health_status(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value


latest_vehicle_state: Dict[str, dict] = {}


def update_operational_metrics():
    active_vehicles.set(len(latest_vehicle_state))
    low_battery_vehicles.set(
        sum(
            1
            for vehicle in latest_vehicle_state.values()
            if vehicle["battery_level"] < LOW_BATTERY_THRESHOLD
        )
    )
    unhealthy_vehicles.set(
        sum(
            1
            for vehicle in latest_vehicle_state.values()
            if vehicle["health_status"].lower() != "healthy"
        )
    )


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "aegisfleet-api",
        "version": "0.1.0",
    }


@app.post("/telemetry")
def receive_telemetry(payload: TelemetryPayload):
    received_at = datetime.now(timezone.utc).isoformat()

    vehicle_data = payload.model_dump()
    vehicle_data["received_at"] = received_at

    latest_vehicle_state[payload.vehicle_id] = vehicle_data
    telemetry_events_received.inc()
    update_operational_metrics()

    if payload.alert:
        alerts_count.inc()

    logger.info(
        "telemetry accepted | vehicle_id=%s | battery_level=%.1f | health_status=%s | alert=%s",
        payload.vehicle_id,
        payload.battery_level,
        payload.health_status,
        payload.alert,
    )

    return {
        "status": "accepted",
        "message": "Telemetry received",
        "vehicle_id": payload.vehicle_id,
        "received_at": received_at,
    }


@app.get("/vehicles")
def get_vehicles():
    return {
        "count": len(latest_vehicle_state),
        "vehicles": list(latest_vehicle_state.values()),
    }



@app.get("/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id: str):
    vehicle = latest_vehicle_state.get(vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vehicle '{vehicle_id}' not found",
        )

    return vehicle


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
