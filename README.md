# SecureCode Vault 🔒

A secure, self-hosted platform for developers to store, encrypt, and share code snippets with fine-grained access control and full audit trail.

## 🛡️ Security & Quality

![Tests](https://github.com/yourusername/securecode-vault/actions/workflows/ci-cd.yml/badge.svg)
![Security Scan](https://github.com/yourusername/securecode-vault/actions/workflows/ci-cd.yml/badge.svg?label=security)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)

## 🚀 Features

- **End-to-end encryption** for code snippets
- **Secure sharing** with expiration & password protection
- **JWT authentication** with bcrypt password hashing
- **Comprehensive audit logging**
- **RESTful API** with FastAPI
- **React frontend**
- **Docker containerization**

## 🛠️ Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL, Redis, JWT, bcrypt  
**Frontend:** React, Vite  
**DevOps:** Docker, GitHub Actions, Pytest, Pre-commit  
**Security:** Bandit, Safety, Trivy, Black, Ruff

## 📋 CI/CD Pipeline

Our automated pipeline includes:

- ✅ Security scanning (SAST/DAST)
- ✅ Code quality checks
- ✅ Automated testing
- ✅ Container security scanning
- ✅ Pre-commit hooks

## 🏃‍♂️ Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/securecode-vault
cd securecode-vault

# Run with Docker
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```
