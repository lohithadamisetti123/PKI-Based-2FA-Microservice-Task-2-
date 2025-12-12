# PKI-Based 2FA Microservice

## Overview
This project implements a **Two-Factor Authentication (2FA) microservice** using **PKI (Public Key Infrastructure)** for secure communication. The service generates TOTP codes, verifies them, and logs codes periodically using a cron job. It also demonstrates secure handling of cryptographic operations and Dockerized deployment.

---

## Features
- **REST API Endpoints**:
  - `/generate`: Generates TOTP codes.
  - `/verify`: Verifies TOTP codes.
  - `/seed`: Provides encrypted seed management.
- **RSA Encryption & Signature**:
  - Commit proof generated using RSA-PSS and encrypted with instructor's public key.
  - Seed encrypted with student's public key using RSA/OAEP.
- **Cron Job Logging**:
  - TOTP codes logged every minute to `/cron/last_code.txt`.
  - Logs persist using Docker volumes.
- **Dockerized Deployment**:
  - Multi-stage Dockerfile for optimized image.
  - Docker Compose for container orchestration.
- **UTC Timezone Handling**:
  - Ensures TOTP and cron logs are consistent globally.
- **Secure Key Handling**:
  - `student_private.pem`, `student_public.pem`, and `instructor_public.pem` included.
  - Encrypted seed stored safely in `/data`.

---

## Getting Started

### Prerequisites
- Docker
- Docker Compose
- Python 3.x (or Node.js/other runtime depending on your implementation)
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/lohithadamisetti123/PKI-Based-2FA-Microservice-Task-2-.git
   cd PKI-Based-2FA-Microservice-Task-2-

