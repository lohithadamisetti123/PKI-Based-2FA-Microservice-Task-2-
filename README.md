# PKI-Based 2FA Microservice

## Overview
This project implements a **Two-Factor Authentication (2FA) microservice** using **Public Key Infrastructure (PKI)** for secure communication.  
It generates TOTP codes, verifies them, encrypts sensitive data using RSA keys, and logs codes periodically using a cron job.  
The entire service is fully containerized using Docker and Docker Compose.

------------------------------------------------------------

## 🚀 Features

### 🔐 REST API Endpoints
• `/generate` — Generates TOTP codes  
• `/verify` — Verifies TOTP codes  
• `/seed` — Returns encrypted TOTP seed  

### 🔒 RSA Encryption & Signature
• Commit proof uses **RSA-PSS** signing (SHA256)  
• Seed encrypted using **RSA-OAEP** (SHA256)  
• Uses:
  - `student_private.pem`
  - `student_public.pem`
  - `instructor_public.pem`

### 📝 Cron Job Logging
• Logs latest TOTP code every minute → `/cron/last_code.txt`  
• Logs persist using Docker volumes  

### 🐳 Dockerized Deployment
• Multi-stage Dockerfile  
• Docker Compose orchestration  

### 🌍 UTC Handling
• TOTP generation and cron logs use UTC for consistency  

### 🔐 Secure Key Handling
• Encrypted seed stored in `/data`  
• Private keys **never exposed**, only referenced  

------------------------------------------------------------

## 🧰 Getting Started

### ✔ Prerequisites
• Docker  
• Docker Compose  
• Python 3.x  
• Git  

------------------------------------------------------------

## 📥 Installation

### 1️⃣ Clone the repository
git clone https://github.com/lohithadamisetti123/PKI-Based-2FA-Microservice-Task-2-.git
cd PKI-Based-2FA-Microservice-Task-2-

### 2️⃣ Build the Docker image
docker-compose build --no-cache

### 3️⃣ Start the microservice
docker-compose up

Service will be live at:
http://localhost:8080

------------------------------------------------------------

## 📡 API Endpoints

### 1️⃣ Generate TOTP Code  
POST /generate  
→ Returns a newly generated TOTP code.

### 2️⃣ Verify TOTP Code  
POST /verify  
Request body:
{
  "code": "123456"
}

→ Returns verification result.

### 3️⃣ Get Encrypted Seed  
GET /seed  
→ Returns encrypted TOTP seed.

------------------------------------------------------------

## ⏱ Cron Job Logging

A cron job runs **every minute** and stores the most recent TOTP code at:

/cron/last_code.txt

### View the latest log:
docker exec -it pki_2fa_service cat /cron/last_code.txt

(Volume ensures logs persist even if the container restarts.)

------------------------------------------------------------

## 🧾 Commit Proof Generation

Generate your encrypted commit proof:

python scripts/generate_commit_proof.py \
  --private-key scripts/student_private.pem \
  --instructor-pub scripts/instructor_public.pem

Output:
commit_proof.b64

### Requirements
• Commit hash = output of:
  git log -1 --format=%H  
• Signature = RSA-PSS SHA256  
• Encryption = RSA-OAEP SHA256  

------------------------------------------------------------

## 📦 Submission Payload Format

Your **proof_payload.json** should look like:

{
  "github_repo_url": "https://github.com/lohithadamisetti123/PKI-Based-2FA-Microservice-Task-2-",
  "commit_hash": "YOUR_COMMIT_HASH",
  "encrypted_commit_signature": "BASE64_STRING",
  "student_public_key": "-----BEGIN PUBLIC KEY-----\\n...\\n-----END PUBLIC KEY-----",
  "encrypted_seed": "BASE64_STRING"
}

------------------------------------------------------------

## ⚠️ Notes

• Always operate in **UTC timezone**  
• Never commit private keys to GitHub  
• Project intended for **educational** purposes  

------------------------------------------------------------

## 👤 Author
• *LOHITHA (23MH1A4413)*

Lohitha Damisetti
