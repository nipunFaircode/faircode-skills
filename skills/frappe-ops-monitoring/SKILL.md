---
name: frappe-ops-monitoring
description: >-
  Use when setting up or checking production server health for a Frappe/ERPNext
  deployment. Triggers on "server monitoring", "site is slow", "workers down",
  "disk full", "error log", "bench doctor", "supervisor", "production health
  check". Covers log locations, process monitoring, DB slow queries, disk
  alerts, and monitoring tool options.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
---

# Frappe Production Monitoring

The most common production incidents: disk full, worker crash, scheduler
stopped, slow MariaDB query. All are detectable before they affect users if
monitoring is in place.

## First response - what to check when something is wrong

Run in order:
```bash
# 1. Check all processes
supervisorctl status

# 2. Check Frappe's own health check
bench doctor

# 3. Check scheduler is running
bench execute frappe.utils.scheduler.is_scheduler_inactive

# 4. Check disk space
df -h

# 5. Check recent errors in the application log
tail -100 ~/frappe-bench/logs/web.error.log

# 6. Check worker errors
tail -100 ~/frappe-bench/logs/worker.error.log
```

## Key log files

All logs under `~/frappe-bench/logs/`:

| File | What it contains |
| --- | --- |
| `web.error.log` | Python exceptions from web requests |
| `web.log` | Web server stdout (gunicorn) |
| `worker.error.log` | Background job exceptions |
| `worker.log` | Background job stdout |
| `scheduler.log` | Scheduled job execution log |
| `monitor.json.log` | Request performance log (response time, query count) |

ERPNext application-level errors: desk → Menu → Error Log (or search "Error Log").
This is the first place to check for user-reported errors - it captures Python
tracebacks with the triggering user and document.

## Supervisor process monitoring

```bash
# Check all process statuses
supervisorctl status

# Expected: all processes RUNNING
# If any show FATAL or STOPPED:
supervisorctl restart frappe-web:
supervisorctl restart frappe-worker:
supervisorctl restart frappe-schedule:
```

Supervisor config: `/etc/supervisor/conf.d/frappe*.conf`
If processes restart repeatedly: check the error log for the crash reason - 
don't just keep restarting.

## Nginx monitoring

```bash
# Check Nginx is running
systemctl status nginx

# Check Nginx error log
tail -50 /var/log/nginx/error.log

# Test config before reload
nginx -t && systemctl reload nginx
```

## MariaDB slow query log

Enable in `/etc/mysql/mariadb.conf.d/50-server.cnf`:
```ini
[mysqld]
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2          # log queries taking > 2 seconds
log_queries_not_using_indexes = 1
```

Restart MariaDB: `systemctl restart mariadb`

Analyse slow queries:
```bash
mysqldumpslow -s t -t 20 /var/log/mysql/slow.log
```

From within Frappe, slow queries also appear in `monitor.json.log` if
`enable_monitor = 1` is set in `site_config.json`.

## Redis monitoring

```bash
# Check Redis memory usage
redis-cli -p 13000 info memory | grep used_memory_human

# Check Redis is accepting connections
redis-cli -p 13000 ping  # should return PONG

# Cache Redis port 13000 (cache), Queue Redis port 11000 (jobs)
redis-cli -p 11000 ping
```

Alert threshold: if `used_memory_human` exceeds 80% of `maxmemory`, flush
the cache: `bench execute frappe.cache.redis_cache.clear_cache`

## Disk space alert

Set a cron job to email when disk > 80%:
```bash
# Add to root's crontab: crontab -e
0 8 * * * df -h / | awk '$5+0 > 80 {print "Disk usage critical: "$5" on "$6}' | mail -s "ALERT: Disk on erp.company.com" ops@company.com
```

Or use ERPNext's built-in: desk → System Health Report (shows disk, CPU, memory).

## Monitoring tool options

| Tool | Effort | What it covers |
| --- | --- | --- |
| ERPNext System Health Report | None (built-in) | Disk, CPU, RAM, scheduler status |
| UptimeRobot (free tier) | 10 min setup | External HTTP uptime check, email/SMS alert |
| Netdata | 30 min setup on VPS | CPU, RAM, disk, nginx, MariaDB, Redis - live dashboard |
| Frappe Cloud | Managed | All of the above included |
| Grafana + Prometheus | High effort | Full metrics stack, custom dashboards |

For most VPS deployments: UptimeRobot (external uptime) + Netdata (server metrics)
covers 90% of incidents with minimal setup.

## Log rotation

Ensure logrotate is configured for Frappe logs - without it, logs fill the disk.
Check: `cat /etc/logrotate.d/frappe` (bench setup production creates this).
If missing, create:
```
/home/frappe/frappe-bench/logs/*.log {
    daily
    rotate 14
    compress
    missingok
    notifempty
    sharedscripts
    postrotate
        supervisorctl restart frappe-web: frappe-worker: > /dev/null 2>&1 || true
    endscript
}
```

## Anti-patterns

| Do NOT | Do Instead |
| --- | --- |
| Restart supervisor without reading the error | Check logs first - repeated restarts without fixing the cause waste time |
| Ignore disk usage until it's full | Alert at 80%; act at 85%; 100% takes the site down immediately |
| Leave slow query log disabled in production | Enable it - you won't know about DB performance problems until they're critical |
| Monitor only from inside the server | Use an external uptime monitor (UptimeRobot) - server-side monitoring misses network/DNS failures |

## Definition of Done
- `supervisorctl status` shows all processes RUNNING.
- `bench doctor` reports no issues.
- MariaDB slow query log enabled and verified.
- Disk space cron alert or Netdata configured.
- External uptime monitor (UptimeRobot or equivalent) set up and alerting.
- Log rotation confirmed in place.

## Related Skills
`frappe-ops-deployment`, `frappe-ops-bench`, `frappe-ops-performance`
