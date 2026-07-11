# DevOps Platform Lab

A hands-on DevOps learning project that deploys a minimal Python HTTP service on Ubuntu Server using `systemd` and Nginx.

## Architecture

```text
Client
  |
  v
Nginx :80
  |
  v
Python application :8000 (127.0.0.1 only)
```

Nginx is the public HTTP entry point and reverse proxy.
The Python application is managed by systemd and runs as an unprivileged `app` system user.

## Features

- Python HTTP service with `/` and `/health` endpoints
- Application managed by `systemd`
- Least-privilege application user (`app`)
- Nginx reverse proxy
- Separate Nginx access and error logs
- Operational runbook for common checks and `502 Bad Gateway` troubleshooting

## Stack

- Ubuntu Server
- Python
- systemd
- Nginx
- Git

## Endpoints

| Endpoint | Expected response |
|---|---|
| `/` | `{"name": "my-minimal-http-service"}` |
| `/health` | `{"status": "ok"}` |

## Project structure

```text
.
├── app/
│   └── app.py
├── deploy/
│   ├── devops-platform-app.service
│   └── nginx.conf
├── docs/
│   └── runbook.md
└── README.md
```

## Verification

Check the application through Nginx:

```bash
curl -i http://127.0.0.1/health
```

Check services:

```bash
sudo systemctl status devops-platform-app --no-pager
sudo systemctl status nginx --no-pager
```

Check listening ports:

```bash
sudo ss -tlnp | grep -E ':80|:8000'
```

Expected result:

- Nginx listens on port `80`
- Python application listens on `127.0.0.1:8000`

## Operations

See [runbook.md](docs/runbook.md) for service operations and `502 Bad Gateway` troubleshooting.

## Next steps

- Automate deployment with Ansible
- Containerize the application with Docker
- Add CI/CD
- Add monitoring, logging, and alerting
- Deploy the application to Kubernetes

## Run with Docker Compose

The Compose stack contains two containers:

    Client -> Nginx container :80 -> app container :8000

Only Nginx is published on the host:

    Host port 8080 -> Nginx container port 80

The application port is available only inside the Docker Compose network.

### Start the stack

    docker compose up --build -d

### Verify the application

    curl -i http://127.0.0.1:8080/health
    docker compose ps

Expected response:

    HTTP/1.1 200 OK
    {"status": "ok"}

### View logs

View logs from all services:

    docker compose logs

Follow logs in real time:

    docker compose logs -f

View logs from one service:

    docker compose logs app
    docker compose logs nginx

### Diagnose 502 Bad Gateway

A 502 response means that Nginx cannot reach the application upstream.

    docker compose ps
    docker compose logs --tail=50 nginx
    docker compose logs --tail=50 app

Check the Nginx upstream configuration:

    proxy_pass http://app:8000;

Restart the application service if needed:

    docker compose restart app

### Stop the stack

    docker compose down