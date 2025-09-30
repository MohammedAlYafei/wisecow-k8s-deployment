# Wisecow Kubernetes Deployment

A containerized deployment of the Wisecow application on Kubernetes with CI/CD automation.

## 🚀 Features

- Dockerized Wisecow application
- Kubernetes deployment with 2 replicas
- NodePort service for external access
- Automated CI/CD pipeline using GitHub Actions
- Docker image auto-build and push to Docker Hub

## 📋 Prerequisites

- Docker
- Kubernetes (Minikube/Kind)
- kubectl
- Docker Hub account

## 🏗️ Project Structure

.
├── .github/
│   └── workflows/
│       └── ci-cd.yaml          # CI/CD pipeline
├── k8s/
│   ├── namespace.yaml          # Kubernetes namespace
│   ├── deployment.yaml         # Application deployment
│   └── service.yaml            # NodePort service
├── Dockerfile                  # Container image definition
├── wisecow.sh                  # Application script
└── README.md

## 🐳 Docker Build
```bash
docker build -t wisecow-app:latest .
docker run -d -p 4499:4499 wisecow-app:latest

Access: http://localhost:4499

☸️ Kubernetes Deployment

start Minikube

    minikube start

deploy application

    # Apply all manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check deployment
kubectl get pods -n wisecow
kubectl get svc -n wisecow

Access Application
bash# Get service URL
minikube service wisecow-service -n wisecow --url

# Access in browser
# http://127.0.0.1:<port>
🔄 CI/CD Pipeline
The GitHub Actions workflow automatically:

Triggers on push to main branch
Builds Docker image
Pushes to Docker Hub
Tags with commit SHA and latest

Setup Secrets
Add these secrets in GitHub repository settings:

DOCKERHUB_USERNAME: Your Docker Hub username
DOCKERHUB_TOKEN: Your Docker Hub access token

🧹 Cleanup
bash# Delete Kubernetes resources
kubectl delete -f k8s/

# Stop Minikube
minikube stop
📝 License
See LICENSE file.
👤 Author
[Your Name]

---

### **6. Git add & commit (local):**
```bash
# Status check
git status

# Add all files
git add .

# Commit
git commit -m "Add Wisecow K8s deployment with CI/CD pipeline"

# Check karo (push ABHI MAT karo)
git log --oneline
