# AegisFleet Kubernetes Manifests

This folder contains baseline Kubernetes manifests for AegisFleet.

## Current scope

These manifests define:

- Namespace
- ConfigMap
- Secret example
- PostgreSQL Deployment, PVC, and Service
- FastAPI Deployment and Service
- Simulator Deployment
- Prometheus Deployment and Service
- Grafana Deployment and Service

## Important note

These manifests are prepared as a portfolio-ready Kubernetes baseline.

They are not deployed yet.

The API and simulator images use local placeholder image names:

- aegisfleet-api:local
- aegisfleet-simulator:local

Before deploying to a real Kubernetes cluster, publish these images to a registry or load them into a local cluster.

## Apply order

Suggested order:

kubectl apply -f namespace.yaml
kubectl apply -f secret.example.yaml
kubectl apply -f configmap.yaml
kubectl apply -f postgres.yaml
kubectl apply -f api.yaml
kubectl apply -f simulator.yaml
kubectl apply -f prometheus.yaml
kubectl apply -f grafana.yaml

## Not included yet

This baseline intentionally does not include:

- Ingress
- TLS
- Helm
- HPA
- EKS
- production secrets management
- managed database

Those can be added later if the project needs a deeper Kubernetes phase.

## Kustomize option

If kubectl with kustomize support is available, the full baseline can be rendered with:

kubectl kustomize infra/kubernetes

Or applied later with:

kubectl apply -k infra/kubernetes
