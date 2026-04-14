# 🏦⚡ BankEdge 

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)
![Terraform](https://img.shields.io/badge/Infrastructure-Terraform-purple.svg)
![AWS](https://img.shields.io/badge/Cloud-AWS-orange.svg)
![Flask](https://img.shields.io/badge/Backend-Flask-black?logo=flask)

## 📖 Project Overview
**BankEdge** is an advanced banking demonstration platform designed to showcase the integration of **Edge Computing**, **Machine Learning for Fraud Detection**, and modern **DevOps pipelines**. This project serves as a proof-of-concept for next-generation financial systems requiring high-speed transaction processing at the edge paired with secure cloud synchronization.

It implements a secure architecture deployed on Amazon Web Services (AWS), orchestrated systematically via **Terraform** for reliable and reproducible infrastructure.

---

## 🏗️ System Architecture & Workflow
This document outlines the end-to-end workflow of the BankEdge system, covering Continuous Integration (CI/CD) pipelines, infrastructure provisioning via Terraform, and runtime deployment architecture.

### 🔄 Project Workflow Overview
The deployment strategy relies on:
1.  **Build & Publish** (Docker): Containerizing the Flask application via GitHub Actions.
2.  **Infrastructure as Code** (Terraform): Provisioning AWS Networking, Compute, and Databases.
3.  **Deployment & Sync** (SSM / Docker): Live EC2 updates retrieving secrets from AWS Systems Manager automatically.

### 1. CI/CD & Build Workflow
This phase transforms source code into deployable artifacts accessible anywhere.

```mermaid
graph TD
    subgraph "Development Environment"
        Dev[Developer] -->|Push/Dispatch| Github[GitHub Repository]
    end

    subgraph "CI Pipeline (GitHub Actions - deploy.yml)"
        Github -->|Trigger| Workflow[Build Job]
        Workflow -->|Checkout| Code[Source Code]
        
        subgraph "Docker Build Process"
            Code -->|Dockerfile Context| imgApp[Flask App Image]
        end
        
        imgApp -->|Push latest| DockerHub
    end

    subgraph "Container Registry"
        DockerHub[Docker Hub]
        DockerHub -- Stores --> Tag1[username/bankedge:latest]
    end
```

### 2. Infrastructure Deployment (Terraform)
This phase provisions the secure AWS virtual environment and handles live container refreshes.

```mermaid
graph TD
    subgraph "Terraform Provisioning (main.tf)"
        TF[Terraform Apply] -->|Deploy| VPC[AWS VPC]
        TF -->|Deploy| DB[PostgreSQL RDS]
        TF -->|Deploy| EC2[EC2/ASG in Private Subnet]
        TF -->|Deploy| ALB[Application Load Balancer]
        TF -->|Deploy| SSM[SSM Parameter Store / Secrets]
    end

    subgraph "CD Pipeline (GitHub Actions)"
        GithubDeploy[deploy.yml - Deploy Job] -->|AWS SSM Send-Command| EC2
    end

    subgraph "Instance Update (Via SSM)"
        EC2 -->|1. Fetch Secrets| SSM
        EC2 -->|2. Pull Image| DockerHub[Docker Hub]
        EC2 -->|3. Run Fresh Container| DockerApp[bankedge Container]
    end
```

### 3. Runtime Architecture
How the system operates once successfully deployed:

```mermaid
graph LR
    User[End User] -->|HTTPS| CF[CloudFront CDN]
    CF -->|Requests| WAF[AWS WAF]
    WAF -->|Filtered| ALB[Public ALB]
    
    subgraph "AWS VPC"
        subgraph "Public Subnets"
            ALB -->|Forward Traffic| AppASG[App Server Target Group]
        end
        
        subgraph "Private Subnets"
            AppASG -->|Process Request| FlaskContainer[BankEdge Flask Container]
            FlaskContainer -->|Validate API Key| Stripe[Stripe Payment Gateway]
            FlaskContainer -->|Machine Learning Inference| MLModel[Scikit-Learn Subsystem]
            FlaskContainer -->|Read/Write| RDS[(PostgreSQL RDS Database)]
        end
    end
```

---

## 🛠️ Technology Stack

### Application Layer
-   **Framework**: Python Flask 3.0
-   **Frontend**: HTML, vanilla CSS/JS, Bootstrap
-   **Authentication**: Flask-JWT-Extended (JSON Web Tokens)
-   **Database ORM**: Flask-SQLAlchemy (SQLite / PostgreSQL)
-   **Machine Learning**: Scikit-learn, Pandas, NumPy, Joblib
-   **Payment Gateway**: Stripe API integration

### Infrastructure & DevOps
-   **Cloud Provider**: AWS (Amazon Web Services)
-   **IaC**: Terraform (v1.0+)
-   **Containerization**: Docker
-   **CI/CD Pipeline**: GitHub Actions
-   **AWS Services Used**: VPC, ALB, EC2, RDS (PostgreSQL), Systems Manager (SSM), WAF, CloudFront, GuardDuty, Security Hub.
-   **Load Testing**: Locust

---

## 🌟 Key Features

-   **Hybrid Edge-Cloud Concept**: Demonstrates transaction metrics directly processed at "Edge Nodes" logic versus centralized Cloud logic.
-   **Real-time Machine Learning**: Evaluates every transaction using an embedded ML model to calculate fraud probabilities and intercept threats instantly.
-   **Secure JWT Authentication**: Role-based access control protecting critical dashboards.
-   **Stripe Integration**: Simulates real-life banking movement.
-   **Enterprise Cloud Architecture**: Comprehensive AWS deployment mapping with strict VPC boundaries and AWS Systems Manager for seamless zero-ssh deployments.

---

## 🚀 Prerequisites & Setup

### Prerequisites
-   [Python 3.9+](https://www.python.org/)
-   [Docker](https://www.docker.com/) (Optional)
-   [Terraform CLI](https://www.terraform.io/)
-   [AWS CLI](https://aws.amazon.com/cli/) (Configured)
-   Stripe Account for keys.

### 1. Local Development (Backend/Frontend)
Clone the repository and prepare the virtual environment:
```bash
git clone https://github.com/Junnwan/BankEdge.git
cd BankEdge
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/MacOS:
# source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file at root with your secrets:
```env
FLASK_SECRET=your_flask_secret
JWT_SECRET_KEY=your_jwt_secret
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
# DATABASE_URL=postgresql://user:pass@localhost:5432/bankedge # Defaults to local SQLite
```

Start the application:
```bash
python app.py
```
*The default SQLite database and initial admin user (`admin.kl@bankedge.com` : `Admin@123`) will be seeded automatically. App is accessible on `http://localhost:5000`.*

### 2. Infrastructure Deployment (AWS)
Deploy the full cloud infrastructure using Terraform:
1.  ```bash
    cd terraform
    terraform init
    ```
2.  Define `terraform.tfvars`:
    ```hcl
    db_username = "dbadmin"
    db_password = "StrongPassword!"
    docker_image = "your_dockerhub_username/bankedge:latest"
    stripe_publishable_key = "pk_test_..."
    stripe_secret_key = "sk_test_..."
    ```
3.  ```bash
    terraform plan
    terraform apply
    ```

### 3. Load Testing
Simulate high-traffic transaction operations:
```bash
locust -f scripts/locustfile.py --host=http://127.0.0.1:5000
```
*Open `http://localhost:8089` to adjust the number of simulated concurrent users.*

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.
