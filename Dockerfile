# ------------------------------
# Stage 1: Builder
# ------------------------------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc libffi-dev libssl-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python packages into /install
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt


# ------------------------------
# Stage 2: Runtime
# ------------------------------
FROM python:3.11-slim

WORKDIR /app

# Install cron + timezone packages
RUN apt-get update && apt-get install -y cron tzdata && apt-get clean

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy project files
COPY . /app

# Ensure scripts folder exists
RUN mkdir -p /app/scripts && chmod -R 755 /app/scripts

# Ensure cron directory exists
RUN mkdir -p /cron && chmod 755 /cron

# Install cron job
COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

EXPOSE 8080

CMD cron && uvicorn main:app --host 0.0.0.0 --port 8080
