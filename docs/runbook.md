# Runbook: DevOps Platform Lab

## Architecture

```text
Client -> Nginx :80 -> Python application :8000
```

The Python application listens only on `127.0.0.1:8000`.
Nginx is the public HTTP entry point.

## Check service status

```bash
sudo systemctl status devops-platform-app --no-pager
sudo systemctl status nginx --no-pager
```

## View application logs

```bash
sudo journalctl -u devops-platform-app -n 50 --no-pager
sudo journalctl -u devops-platform-app -f
```

Use `Ctrl+C` to stop following logs.

## Restart the application

```bash
sudo systemctl restart devops-platform-app
sudo systemctl status devops-platform-app --no-pager
```

## Check HTTP endpoints

```bash
curl -i http://127.0.0.1/health
curl -i http://127.0.0.1:8000/health
```

Expected: HTTP 200 and `{"status": "ok"}`.

## Check listening ports

```bash
sudo ss -tlnp | grep -E ':80|:8000'
```

Expected listeners:

- Nginx: `0.0.0.0:80`
- Python application: `127.0.0.1:8000`

## Diagnose 502 Bad Gateway

1. Check application status:

   ```bash
   sudo systemctl status devops-platform-app --no-pager
   ```

2. Check application logs:

   ```bash
   sudo journalctl -u devops-platform-app -n 50 --no-pager
   ```

3. Check port 8000:

   ```bash
   sudo ss -tlnp | grep ':8000'
   ```

4. Test the application directly:

   ```bash
   curl -i http://127.0.0.1:8000/health
   ```

5. Check Nginx:

   ```bash
   sudo tail -n 50 /var/log/nginx/devops-platform-app.error.log
   sudo nginx -t
   ```

6. Restart the application if needed:

   ```bash
   sudo systemctl restart devops-platform-app
   ```