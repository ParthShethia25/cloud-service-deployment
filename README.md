# Cloud Service with Security, Reliability & Automation

## Overview
This project implements an end-to-end cloud service on AWS with a focus on secure infrastructure, automated deployments, and operational observability.  
The application layer is intentionally minimal so that infrastructure, CI/CD, security, and monitoring practices remain the primary focus.

---

## Architecture

Developer → GitHub → GitHub Actions → AWS EC2 (Dockerized Flask App) → CloudWatch Logs & Metrics → CloudTrail (stored in S3)

---

## Tech Stack

AWS: EC2, VPC (default), IAM, S3, CloudWatch, CloudTrail  
Infrastructure as Code: Terraform  
CI/CD: GitHub Actions  
Containerization: Docker  
Backend: Python (Flask)  
OS: Linux (Amazon Linux 2023)

---

## Repository Structure
```
cloud-service-deployment/
├── app/
│   ├── app.py
│   └── requirements.txt
├── docker/
│   └── Dockerfile
├── terraform/
│   ├── provider.tf
│   ├── variables.tf
│   ├── ec2.tf
│   ├── iam.tf
│   ├── security_groups.tf
│   ├── s3.tf
│   └── cloudtrail.tf
├── .github/
│   └── workflows/
│       └── deploy.yml
├── .gitignore
└── README.md
```
---

## Infrastructure Provisioning (Terraform)

Initialize Terraform:
```
cd terraform
terraform init
```

Configure variables (terraform.tfvars):
key_name = "cloud-service-key"
allowed_ssh_cidr = "<YOUR_PUBLIC_IPV4>/32"

Plan and apply:
```
terraform plan
terraform apply
```
---

## EC2 One-Time Setup

SSH into EC2:
```
ssh -i ~/.ssh/cloud-service-key.pem ec2-user@<EC2_PUBLIC_IP>
```
Install Docker:
```
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user
exit
```

Reconnect and verify:
```
docker ps
```
Create deployment directory:
```
mkdir -p ~/cloud-service
```
---

## Application Endpoints

GET  /health        → Liveness check  
GET  /ready         → Readiness check  
POST /apply-loan    → Simulated workload with controlled failures  

---

## Docker Usage

Build image locally (optional):
```
docker build -t cloud-service -f docker/Dockerfile .
```
Run container locally (optional):
```
docker run -d -p 5000:5000 cloud-service
```
---

## CI/CD Pipeline (GitHub Actions)

Pipeline behavior:
- Triggered on push to main branch
- Secure SSH-based deployment to EC2
- Docker image built on EC2
- Container restarted automatically

Trigger deployment manually:
```
git commit --allow-empty -m "trigger deployment"
git push origin main
```
---

## Service Verification

Health check:
```
curl http://<EC2_PUBLIC_IP>/health
```
Readiness check:
```
curl http://<EC2_PUBLIC_IP>/ready
```
Workload endpoint:
```
curl http://<EC2_PUBLIC_IP>/apply-loan -X POST -H "Content-Type: application/json" -d '{"applicant":"test"}'
```
Intermittent failures are expected due to controlled failure logic.

---

## Observability

CloudWatch:
- Docker container logs streamed to CloudWatch
- Log group: /cloud-service/docker

Verify CloudWatch agent:
sudo systemctl status amazon-cloudwatch-agent

---

## Audit Logging

CloudTrail:
- Enabled via Terraform
- Records AWS API and IAM activity
- Logs stored in S3 bucket created by Terraform

---

## Security Controls

- IAM role attached to EC2
- No hard-coded credentials
- Security groups restrict inbound traffic
- SSH access controlled via CIDR
- Infrastructure fully managed using Terraform

---

## Cleanup

Destroy all infrastructure:
```
cd terraform
terraform destroy
```
---

## Status

Project completed end-to-end with automated infrastructure provisioning, CI/CD deployment, containerized runtime, logging, and audit visibility.

