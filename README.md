# AegisFleet — Real-Time Fleet Intelligence Platform

AegisFleet is a production-style DevOps and Cloud Engineering portfolio project.

It simulates real-time vehicle telemetry and builds a backend platform step by step using Python, FastAPI, Docker, Prometheus, Grafana, PostgreSQL, Terraform, AWS, and CI/CD.

## Current Status

Completed so far:

* Vehicle simulator
* FastAPI backend
* Telemetry ingestion endpoint
* In-memory latest vehicle state
* Vehicle list endpoint
* Single vehicle lookup endpoint
* Prometheus `/metrics` endpoint
* Basic operational metrics
* Health status normalization
* Basic API logging

## Current API Endpoints

* `GET /health`
* `POST /telemetry`
* `GET /vehicles`
* `GET /vehicles/{vehicle_id}`
* `GET /metrics`

## Current Metrics

* `telemetry_events_received_total`
* `active_vehicles`
* `alerts_count_total`
* `low_battery_vehicles`
* `unhealthy_vehicles`

## Planned Next Steps

* PostgreSQL persistence
* Docker Compose local environment
* Prometheus and Grafana dashboards
* CI/CD pipeline
* Terraform AWS infrastructure
