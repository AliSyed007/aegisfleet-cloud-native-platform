# AegisFleet — Real-Time Fleet Intelligence Platform

AegisFleet is a production-style DevOps and Cloud Engineering portfolio project that simulates real-time vehicle telemetry and runs a local observability-focused backend platform using Docker Compose.

The project is intentionally built in phases to show practical system design, infrastructure discipline, observability, persistence, and production-minded engineering decisions.

## Project Goal

The goal of AegisFleet is to demonstrate how a real-world fleet monitoring platform could be designed, containerized, monitored, and later deployed using cloud infrastructure.

Current local platform capabilities include:

* Real-time vehicle telemetry simulation
* FastAPI backend for telemetry ingestion
* PostgreSQL persistence for telemetry events
* Prometheus metrics endpoint
* Prometheus scraping through Docker Compose networking
* Grafana datasource provisioning
* Grafana dashboard provisioning
* Local Docker Compose infrastructure
* Clean phase-based Git history and stable tags

## Current Architecture

```text
+-------------------+
| Vehicle Simulator |
| Python container  |
+---------+---------+
          |
          | HTTP POST /telemetry
          v
+-------------------+          +-------------------+
| FastAPI Backend   |--------->| PostgreSQL        |
| API container     |          | telemetry storage |
+---------+---------+          +-------------------+
          |
          | /metrics
          v
+-------------------+          +-------------------+
| Prometheus        |--------->| Grafana           |
| Metrics scraping  |          | Dashboard UI      |
+-------------------+          +-------------------+
```

## Services

The local platform is managed through Docker Compose.

| Service     | Container Name          | Purpose                                 | Host Port |
| ----------- | ----------------------- | --------------------------------------- | --------- |
| PostgreSQL  | `aegisfleet-postgres`   | Stores telemetry events                 | `5433`    |
| FastAPI API | `aegisfleet-api`        | Receives telemetry and exposes metrics  | `8000`    |
| Simulator   | `aegisfleet-simulator`  | Sends fake vehicle telemetry to the API | none      |
| Prometheus  | `aegisfleet-prometheus` | Scrapes API metrics                     | `9090`    |
| Grafana     | `aegisfleet-grafana`    | Visualizes metrics through dashboards   | `3000`    |

## Technology Stack

| Area                 | Technology           |
| -------------------- | -------------------- |
| Backend API          | Python, FastAPI      |
| Telemetry Simulator  | Python               |
| Database             | PostgreSQL 16 Alpine |
| Metrics              | Prometheus client    |
| Monitoring           | Prometheus           |
| Dashboards           | Grafana              |
| Local Infrastructure | Docker Compose       |
| Version Control      | Git, GitHub          |

## API Endpoints

| Method | Endpoint                 | Purpose                          |
| ------ | ------------------------ | -------------------------------- |
| `GET`  | `/health`                | API health check                 |
| `POST` | `/telemetry`             | Receive vehicle telemetry        |
| `GET`  | `/vehicles`              | List latest known vehicle states |
| `GET`  | `/vehicles/{vehicle_id}` | Get latest state for one vehicle |
| `GET`  | `/metrics`               | Prometheus metrics endpoint      |

## Telemetry Fields

The project currently keeps telemetry intentionally simple and focused:

| Field           | Purpose                   |
| --------------- | ------------------------- |
| `vehicle_id`    | Unique vehicle identifier |
| `lat`           | Vehicle latitude          |
| `lon`           | Vehicle longitude         |
| `battery`       | Battery percentage        |
| `temperature`   | Vehicle temperature       |
| `health_status` | Current health state      |
| `alert`         | Optional alert message    |

## Prometheus Metrics

The API exposes the following operational metrics:

| Metric                            | Type    | Purpose                                                  |
| --------------------------------- | ------- | -------------------------------------------------------- |
| `telemetry_events_received_total` | Counter | Total telemetry events received                          |
| `active_vehicles`                 | Gauge   | Number of vehicles with latest known state               |
| `alerts_count_total`              | Counter | Total telemetry events where an alert is present         |
| `low_battery_vehicles`            | Gauge   | Vehicles below battery threshold                         |
| `unhealthy_vehicles`              | Gauge   | Vehicles whose latest health status is not healthy or ok |

## Grafana Dashboard

Grafana is automatically provisioned through files inside the repository.

Dashboard details:

| Item                      | Value                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------- |
| Dashboard Title           | `AegisFleet Fleet Operations Overview`                                             |
| Dashboard UID             | `aegisfleet-overview`                                                              |
| Folder                    | `AegisFleet`                                                                       |
| Prometheus Datasource UID | `prometheus`                                                                       |
| Local URL                 | `http://localhost:3000/d/aegisfleet-overview/aegisfleet-fleet-operations-overview` |

Default local Grafana login:

| Username | Password            |
| -------- | ------------------- |
| `admin`  | `change_me_locally` |

> This password is for local development only and should be changed for any real deployment.

## Repository Structure

```text
aegisfleet-cloud-native-platform/
├── api/
│   ├── Dockerfile
│   ├── db/
│   │   └── migrations/
│   │       └── 001_create_telemetry_events.sql
│   └── ...
├── simulator/
│   ├── Dockerfile
│   └── ...
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   └── grafana/
│       ├── dashboards/
│       │   └── aegisfleet-overview.json
│       └── provisioning/
│           ├── dashboards/
│           │   └── dashboards.yml
│           └── datasources/
│               └── prometheus.yml
├── docker-compose.yml
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone git@github.com:AliSyed007/aegisfleet-cloud-native-platform.git
cd aegisfleet-cloud-native-platform
```

### 2. Start the full local stack

```bash
docker compose up -d --build
```

This starts:

* PostgreSQL
* FastAPI API
* Simulator
* Prometheus
* Grafana

### 3. Start only infrastructure services

Use this when you want the platform running but do not want the simulator continuously generating telemetry:

```bash
docker compose up -d postgres api prometheus grafana
```

### 4. Stop only the simulator

```bash
docker compose stop simulator
```

This is useful to prevent unnecessary local database growth.

## Local URLs

| Component            | URL                                                                                |
| -------------------- | ---------------------------------------------------------------------------------- |
| API health           | `http://localhost:8000/health`                                                     |
| API metrics          | `http://localhost:8000/metrics`                                                    |
| Prometheus           | `http://localhost:9090`                                                            |
| Grafana              | `http://localhost:3000`                                                            |
| AegisFleet Dashboard | `http://localhost:3000/d/aegisfleet-overview/aegisfleet-fleet-operations-overview` |

## Smoke Test Commands

### Check containers

```bash
docker compose ps -a
```

### Check API health

```bash
curl -s http://localhost:8000/health
```

### Check Prometheus metrics from the API

```bash
curl -s http://localhost:8000/metrics | grep -E "telemetry_events_received_total|active_vehicles|alerts_count_total|low_battery_vehicles|unhealthy_vehicles"
```

### Check Prometheus readiness

```bash
curl -s http://localhost:9090/-/ready
```

### Check Grafana health

```bash
curl -s http://localhost:3000/api/health
```

Expected Grafana health should include:

```json
"database": "ok"
```

## Cold-Start Verification

A full clean local rebuild can be tested with:

```bash
docker compose down -v --remove-orphans
docker compose up -d --build
```

This validates that:

* Containers build successfully
* PostgreSQL starts from a clean volume
* Database migration runs automatically
* API connects to PostgreSQL
* Prometheus starts and scrapes the API
* Grafana starts successfully
* Grafana datasource is provisioned
* Grafana dashboard is provisioned

## Cleanup Commands

### Stop containers but keep volumes

```bash
docker compose down
```

### Stop containers and remove local database volume

```bash
docker compose down -v
```

### Stop containers, remove volumes, and remove orphan containers

```bash
docker compose down -v --remove-orphans
```

Use the last command before a full cold-start smoke test.

## Phase History

| Phase   | Description                               | Status      | Stable Tag                        |
| ------- | ----------------------------------------- | ----------- | --------------------------------- |
| Phase 1 | Vehicle simulator                         | Complete    | pending historical tag            |
| Phase 2 | FastAPI backend and metrics               | Complete    | `v0.2.0-phase2-backend-stable`    |
| Phase 3 | PostgreSQL persistence and Docker Compose | Complete    | `v0.3.0-phase3-compose-stable`    |
| Phase 4 | Prometheus monitoring                     | Complete    | `v0.4.0-phase4-prometheus-stable` |
| Phase 5 | Grafana dashboards and provisioning       | Complete    | `v0.5.0-phase5-grafana-stable`    |
| Phase 6 | README and architecture documentation     | In Progress | pending                           |

## Production-Minded Design Decisions

This project is local-first at the current stage, but it is designed with production habits in mind:

* Services communicate through Docker Compose service names instead of localhost.
* PostgreSQL runs as a dedicated service instead of using in-memory-only storage.
* Database schema setup is handled through a migration file.
* Prometheus scrapes the API through the internal Docker network.
* Grafana datasource and dashboard provisioning are stored as code.
* The simulator can be stopped independently to control local data growth.
* Metrics are intentionally simple, readable, and useful for operations.
* Git branches and stable tags are used to preserve clean phase checkpoints.

## Current Status

The project currently runs successfully as a local Docker Compose platform with:

* API
* PostgreSQL
* Prometheus
* Grafana
* Provisioned Grafana dashboard
* Simulator available but stoppable

Current recommended operating mode during documentation and review:

```bash
docker compose up -d postgres api prometheus grafana
docker compose stop simulator
```

## Next Planned Work

Planned future phases may include:

* CI/CD pipeline
* Automated validation checks
* Security improvements
* Environment variable cleanup
* Production-style secrets handling
* Cloud deployment
* Terraform infrastructure
* Kubernetes deployment

Cloud, Terraform, and Kubernetes are intentionally not part of the current phase.
