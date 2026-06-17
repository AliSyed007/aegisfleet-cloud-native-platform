.DEFAULT_GOAL := help
.RECIPEPREFIX := >

COMPOSE := docker compose

.PHONY: help init-env build up up-infra stop-simulator down clean ps logs logs-api logs-simulator logs-prometheus logs-grafana health metrics prometheus-ready grafana-health wait-api wait-prometheus wait-grafana smoke cold-start

help:
> @echo "AegisFleet local operations"
> @echo ""
> @echo "Setup:"
> @echo "  make init-env           Create .env from .env.example if missing"
> @echo ""
> @echo "Docker Compose:"
> @echo "  make build              Build local Docker images"
> @echo "  make up                 Start full local stack including simulator"
> @echo "  make up-infra           Start postgres, api, prometheus, and grafana only"
> @echo "  make stop-simulator     Stop simulator to prevent local DB growth"
> @echo "  make down               Stop containers but keep volumes"
> @echo "  make clean              Stop containers and remove volumes/orphans"
> @echo "  make ps                 Show container status"
> @echo ""
> @echo "Logs:"
> @echo "  make logs               Follow logs for all services"
> @echo "  make logs-api           Follow API logs"
> @echo "  make logs-simulator     Follow simulator logs"
> @echo "  make logs-prometheus    Follow Prometheus logs"
> @echo "  make logs-grafana       Follow Grafana logs"
> @echo ""
> @echo "Checks:"
> @echo "  make health             Check API health"
> @echo "  make metrics            Show key API Prometheus metrics"
> @echo "  make prometheus-ready   Check Prometheus readiness"
> @echo "  make grafana-health     Check Grafana health"
> @echo "  make wait-api           Wait until API is ready"
> @echo "  make wait-prometheus    Wait until Prometheus is ready"
> @echo "  make wait-grafana       Wait until Grafana is healthy"
> @echo "  make smoke              Run local smoke checks with readiness waits"
> @echo "  make cold-start         Rebuild from clean local volumes"

init-env:
> @if [ -f .env ]; then \
>   echo ".env already exists"; \
> else \
>   cp .env.example .env; \
>   echo "Created .env from .env.example"; \
> fi

build:
> $(COMPOSE) build

up:
> $(COMPOSE) up -d --build

up-infra:
> $(COMPOSE) up -d postgres api prometheus grafana

stop-simulator:
> $(COMPOSE) stop simulator

down:
> $(COMPOSE) down

clean:
> $(COMPOSE) down -v --remove-orphans

ps:
> $(COMPOSE) ps -a

logs:
> $(COMPOSE) logs -f

logs-api:
> $(COMPOSE) logs -f api

logs-simulator:
> $(COMPOSE) logs -f simulator

logs-prometheus:
> $(COMPOSE) logs -f prometheus

logs-grafana:
> $(COMPOSE) logs -f grafana

health:
> curl -fsS http://localhost:8000/health

metrics:
> curl -fsS http://localhost:8000/metrics | grep -E "telemetry_events_received_total|active_vehicles|alerts_count_total|low_battery_vehicles|unhealthy_vehicles"

prometheus-ready:
> curl -fsS http://localhost:9090/-/ready

grafana-health:
> curl -fsS http://localhost:3000/api/health

wait-api:
> @echo "Waiting for API..."
> @for i in $$(seq 1 30); do \
>   if curl -fsS http://localhost:8000/health >/dev/null 2>&1; then \
>     echo "API is ready"; \
>     exit 0; \
>   fi; \
>   echo "API not ready yet ($$i/30)"; \
>   sleep 2; \
> done; \
> echo "ERROR: API did not become ready"; \
> exit 1

wait-prometheus:
> @echo "Waiting for Prometheus..."
> @for i in $$(seq 1 30); do \
>   if curl -fsS http://localhost:9090/-/ready >/dev/null 2>&1; then \
>     echo "Prometheus is ready"; \
>     exit 0; \
>   fi; \
>   echo "Prometheus not ready yet ($$i/30)"; \
>   sleep 2; \
> done; \
> echo "ERROR: Prometheus did not become ready"; \
> exit 1

wait-grafana:
> @echo "Waiting for Grafana..."
> @for i in $$(seq 1 30); do \
>   if curl -fsS http://localhost:3000/api/health | grep -q '"database": "ok"'; then \
>     echo "Grafana is healthy"; \
>     exit 0; \
>   fi; \
>   echo "Grafana not ready yet ($$i/30)"; \
>   sleep 2; \
> done; \
> echo "ERROR: Grafana did not become healthy"; \
> exit 1

smoke: wait-api wait-prometheus wait-grafana
> @echo "== Docker Compose status =="
> $(COMPOSE) ps -a
> @echo ""
> @echo "== API health =="
> curl -fsS http://localhost:8000/health
> @echo ""
> @echo ""
> @echo "== API metrics =="
> curl -fsS http://localhost:8000/metrics | grep -E "telemetry_events_received_total|active_vehicles|alerts_count_total|low_battery_vehicles|unhealthy_vehicles"
> @echo ""
> @echo "== Prometheus readiness =="
> curl -fsS http://localhost:9090/-/ready
> @echo ""
> @echo ""
> @echo "== Grafana health =="
> curl -fsS http://localhost:3000/api/health
> @echo ""

cold-start:
> $(COMPOSE) down -v --remove-orphans
> $(COMPOSE) up -d --build
> $(MAKE) smoke
