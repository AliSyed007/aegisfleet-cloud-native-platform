# AegisFleet — Real-Time Fleet Intelligence Platform

[![AegisFleet CI](https://github.com/AliSyed007/aegisfleet-cloud-native-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/AliSyed007/aegisfleet-cloud-native-platform/actions/workflows/ci.yml)

AegisFleet is a production-style DevOps and Cloud Engineering portfolio project that simulates real-time vehicle telemetry and runs a local observability-focused backend platform using Docker Compose.

The project is intentionally built in phases to show practical system design, infrastructure discipline, observability, persistence, local operational hygiene, and production-minded engineering decisions.

## Project Goal

The goal of AegisFleet is to demonstrate how a real-world fleet monitoring platform could be designed, containerized, monitored, operated locally, and later deployed using cloud infrastructure.

Current local platform capabilities include:

* Real-time vehicle telemetry simulation
* FastAPI backend for telemetry ingestion
* PostgreSQL persistence for telemetry events
* Prometheus metrics endpoint
* Prometheus scraping through Docker Compose networking
* Grafana datasource provisioning
* Grafana dashboard provisioning
* Local Docker Compose infrastructure
* Local operations Makefile
* Readiness-aware smoke checks
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
| Local Operations     | Makefile             |
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
├── Makefile
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone git@github.com:AliSyed007/aegisfleet-cloud-native-platform.git
cd aegisfleet-cloud-native-platform
```

### 2. Create local environment file

```bash
cp .env.example .env
```

Or use the Makefile helper:

```bash
make init-env
```

### 3. Start the full local stack

```bash
docker compose up -d --build
```

This starts:

* PostgreSQL
* FastAPI API
* Simulator
* Prometheus
* Grafana

### 4. Start only infrastructure services

Use this when you want the platform running but do not want the simulator continuously generating telemetry:

```bash
docker compose up -d postgres api prometheus grafana
```

### 5. Stop only the simulator

```bash
docker compose stop simulator
```

This is useful to prevent unnecessary local database growth.

## Local Operations with Make

AegisFleet includes a `Makefile` to simplify common local development and operational commands.

Useful commands:

| Command               | Purpose                                               |
| --------------------- | ----------------------------------------------------- |
| `make help`           | Show available local operations                       |
| `make init-env`       | Create `.env` from `.env.example` if missing          |
| `make build`          | Build local Docker images                             |
| `make up`             | Start the full stack including simulator              |
| `make up-infra`       | Start PostgreSQL, API, Prometheus, and Grafana only   |
| `make stop-simulator` | Stop simulator to prevent local database growth       |
| `make down`           | Stop containers but keep volumes                      |
| `make clean`          | Stop containers and remove volumes/orphans            |
| `make ps`             | Show container status                                 |
| `make quality`        | Run local non-runtime quality gates                   |
| `make test`           | Alias for `make quality`                              |
| `make smoke`          | Run readiness-aware local smoke checks                |
| `make cold-start`     | Rebuild from clean local volumes and run smoke checks |

Recommended local review workflow:

```bash
make quality
make up-infra
make smoke
```

Use the full stack only when telemetry generation is needed:

```bash
make up
```

Stop the simulator when continuous telemetry is not required:

```bash
make stop-simulator
```

## Local URLs

| Component            | URL                                                                                |
| -------------------- | ---------------------------------------------------------------------------------- |
| API health           | `http://localhost:8000/health`                                                     |
| API metrics          | `http://localhost:8000/metrics`                                                    |
| Prometheus           | `http://localhost:9090`                                                            |
| Grafana              | `http://localhost:3000`                                                            |
| AegisFleet Dashboard | `http://localhost:3000/d/aegisfleet-overview/aegisfleet-fleet-operations-overview` |

## Smoke Test Commands

### Preferred smoke test

```bash
make smoke
```

The Makefile smoke test waits for API, Prometheus, and Grafana readiness before checking service health.

### Manual check containers

```bash
docker compose ps -a
```

### Manual check API health

```bash
curl -s http://localhost:8000/health
```

### Manual check Prometheus metrics from the API

```bash
curl -s http://localhost:8000/metrics | grep -E "telemetry_events_received_total|active_vehicles|alerts_count_total|low_battery_vehicles|unhealthy_vehicles"
```

### Manual check Prometheus readiness

```bash
curl -s http://localhost:9090/-/ready
```

### Manual check Grafana health

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
make cold-start
```

Or manually:

```bash
docker compose down -v --remove-orphans
docker compose up -d --build
make smoke
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
* Local smoke checks pass after readiness waits

## Cleanup Commands

### Stop containers but keep volumes

```bash
make down
```

Manual equivalent:

```bash
docker compose down
```

### Stop containers and remove local database volume

```bash
docker compose down -v
```

### Stop containers, remove volumes, and remove orphan containers

```bash
make clean
```

Manual equivalent:

```bash
docker compose down -v --remove-orphans
```

Use the clean command before a full cold-start smoke test.

## Phase History

| Phase   | Description                                      | Status      | Stable Tag                                 |
| ------- | ------------------------------------------------ | ----------- | ------------------------------------------ |
| Phase 1 | Vehicle simulator                                | Complete    | pending historical tag                     |
| Phase 2 | FastAPI backend and metrics                      | Complete    | `v0.2.0-phase2-backend-stable`             |
| Phase 3 | PostgreSQL persistence and Docker Compose        | Complete    | `v0.3.0-phase3-compose-stable`             |
| Phase 4 | Prometheus monitoring                            | Complete    | `v0.4.0-phase4-prometheus-stable`          |
| Phase 5 | Grafana dashboards and provisioning              | Complete    | `v0.5.0-phase5-grafana-stable`             |
| Phase 6 | README and architecture documentation            | Complete    | `v0.6.0-phase6-readme-architecture-stable` |
| Phase 7 | Local operational hygiene and developer workflow | Complete    | local Makefile workflow and smoke checks  |
| Phase 8 | Local quality gates and CI readiness              | Complete    | local quality checks and test alias       |
| Phase 9 | GitHub Actions CI baseline                        | Complete    | quality gate workflow on GitHub Actions   |
| Phase 10 | CI Docker build validation                       | Complete    | API and simulator image builds in CI      |
| Phase 11 | CI Docker Compose smoke test                     | Complete    | infrastructure stack smoke test in CI     |
| Phase 12 | Release polish and reviewer experience            | Complete    | CI badge and reviewer-facing main branch  |
| Phase 13 | Container hardening and runtime hygiene           | Complete    | API container runs as non-root user       |

## Continuous Integration

AegisFleet includes a GitHub Actions workflow for baseline CI validation.

Workflow file: `.github/workflows/ci.yml`

The CI workflow runs on pushes and pull requests. It performs the same local quality gate used during development: `make quality`.

The workflow currently validates Git whitespace checks, Python syntax checks, Docker Compose configuration, README markdown code fence balance, Docker image builds for the API and simulator, and a Docker Compose smoke test for the local infrastructure stack.

This keeps local development and CI behavior aligned before adding heavier test stages.

## Cloud Deployment and Demo Proof

AegisFleet has been validated beyond local development through a temporary AWS deployment.

The cloud deployment used:

* Terraform for AWS infrastructure provisioning.
* Ansible for EC2 bootstrap and application startup.
* Docker Compose on the EC2 host for running the application stack.
* Prometheus and Grafana for live operational visibility.
* GitHub Actions for CI validation before deployment.

The live AWS demo verified:

* API health endpoint reachable on port `8000`.
* Prometheus reachable on port `9090`.
* Grafana reachable on port `3000`.
* Prometheus successfully scraping the API target.
* Grafana dashboard showing live telemetry metrics.
* Infrastructure folder containing Terraform, Ansible, and Kubernetes-ready manifests.

After the demo and LinkedIn proof, the AWS resources were intentionally destroyed to avoid unnecessary cost.

Current AWS status:

* No EC2 instance is currently running for this project.
* No public demo endpoint is currently live.
* Terraform state was verified empty after destroy.
* Any future AWS demo must be recreated deliberately using Terraform and Ansible.

## Infrastructure as Code

AegisFleet includes production-minded infrastructure automation under `infra/`.

Terraform baseline:

* Custom VPC.
* Public subnet.
* Internet gateway.
* Route table and association.
* Security group for SSH, API, Prometheus, and Grafana access.
* Ubuntu EC2 instance.
* Elastic IP.
* Public outputs for SSH and service URLs.

Ansible baseline:

* Installs required system packages.
* Installs Docker and Docker Compose v2.
* Enables Docker service.
* Clones the project repository.
* Creates the runtime environment file.
* Starts the stack using Docker Compose.
* Verifies the API health endpoint on the EC2 host.

Kubernetes baseline:

* Kubernetes-ready manifests are available under `infra/kubernetes`.
* The manifests can be rendered locally with `make k8s-validate`.
* Validation uses `kubectl kustomize` and does not deploy resources.
* Kubernetes was not deployed in the completed demo phase.

## Production-Minded Design Decisions

This project is local-first at the current stage, but it is designed with production habits in mind:

* Application containers are designed to avoid running as root where practical.
* Services communicate through Docker Compose service names instead of localhost.
* PostgreSQL runs as a dedicated service instead of using in-memory-only storage.
* Database schema setup is handled through a migration file.
* Prometheus scrapes the API through the internal Docker network.
* Grafana datasource and dashboard provisioning are stored as code.
* The simulator can be stopped independently to control local data growth.
* The Makefile documents repeatable local operations.
* Smoke checks include readiness waits to avoid false failures immediately after container startup.
* Metrics are intentionally simple, readable, and useful for operations.
* Git branches and stable tags are used to preserve clean phase checkpoints.


## Current Status

The project currently has a stable local-first platform with:

* FastAPI telemetry API.
* PostgreSQL persistence.
* Prometheus metrics.
* Grafana dashboard provisioning.
* Docker Compose orchestration.
* Makefile-based local operations.
* Readiness-aware smoke checks.
* Local quality gates.
* GitHub Actions CI.
* Docker image build validation in CI.
* Docker Compose smoke validation in CI.
* Non-root API container runtime.
* Compose healthchecks.
* Terraform AWS baseline.
* Ansible EC2 bootstrap.
* Kubernetes-ready manifests.
* Kubernetes manifest render validation with `make k8s-validate`.

Current recommended local operating mode during documentation and review:

```bash
make up-infra
make smoke
```

Current cloud status:

* AWS demo was completed successfully.
* AWS resources were destroyed after proof collection.
* No public AWS endpoint is currently live.

## Next Planned Work

Planned future phases may include:

* Improve README demo proof section with non-sensitive screenshots.
* Add GitHub repository topics and description.
* Optionally test Kubernetes manifests with `kind` or `minikube`.
* Improve production-style secrets handling.
* Add lightweight security checks.
* Recreate AWS demo only when needed, then destroy resources again.

Amazon EKS is intentionally not part of the current phase because it can add unnecessary cost for this portfolio stage.
