---
name: frappe-devenv-setup
description: >-
  Use when setting up a local Frappe development environment from scratch.
  Triggers on "local setup", "bench init", "development environment", "new dev
  machine", "setup frappe locally", "bench new-site fails", "MariaDB setup".
  Covers Ubuntu 22.04/24.04 setup, bench init, site creation, custom app
  install, and VSCode configuration for Frappe v14-v16.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
---

# Frappe Development Environment Setup

Follow in order. Each step depends on the previous. For Faircode projects:
always use a version-specific branch (e.g., `version-15`) - never `develop`
for anything that will go to a client site.

## System requirements (Ubuntu 22.04 / 24.04)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# System packages
sudo apt install -y git python3-pip python3-dev python3-venv \
  libmysqlclient-dev libffi-dev libssl-dev wkhtmltopdf \
  redis-server mariadb-server mariadb-client \
  xvfb libfontconfig fonts-cantarell

# Node.js (use nvm for version management)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
nvm alias default 18
node --version  # should be 18.x

# Yarn (required by bench)
npm install -g yarn

# Python version check - Frappe v15 needs Python 3.11+
python3 --version  # 3.10+ for v14, 3.11+ for v15/v16
```

## MariaDB setup

```bash
# Secure installation
sudo mysql_secure_installation
# Set root password, remove anonymous users, disallow remote root login

# Required MariaDB configuration
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Add under `[mysqld]`:
```ini
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
```

Add at end of file:
```ini
[mysql]
default-character-set = utf8mb4
```

```bash
sudo systemctl restart mariadb
# Verify charset
mysql -u root -p -e "SHOW VARIABLES LIKE 'character_set_server';"
# Should show utf8mb4
```

## Install bench

```bash
pip3 install frappe-bench
# Verify
bench --version
```

## bench init (create a new bench)

```bash
# For Frappe v15 (adjust branch for v14/v16)
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
```

## Install ERPNext (if needed)

```bash
bench get-app erpnext --branch version-15
# Or with a specific repo:
bench get-app https://github.com/frappe/erpnext --branch version-15
```

## Create a new site

```bash
bench new-site site1.local \
  --mariadb-root-password <your-mariadb-root-password> \
  --admin-password admin \
  --install-app erpnext   # omit if ERPNext not needed
```

Add to `/etc/hosts`:
```
127.0.0.1  site1.local
```

## Install a custom app

```bash
# From a Git repo
bench get-app https://github.com/yourorg/myapp --branch main

# Install on the site
bench --site site1.local install-app myapp

# Or from a local path (for development)
bench get-app myapp /path/to/local/myapp
bench --site site1.local install-app myapp
```

## Start the development server

```bash
# From inside the bench directory
bench start
```

Opens at `http://site1.local:8000`. Login with `administrator` / `admin`.

## VSCode setup

Recommended extensions:
- Python (Microsoft)
- Pylance
- ESLint
- Prettier

`.vscode/settings.json` in your app folder:
```json
{
  "python.defaultInterpreterPath": "/path/to/frappe-bench/env/bin/python",
  "python.analysis.extraPaths": [
    "/path/to/frappe-bench/apps/frappe",
    "/path/to/frappe-bench/apps/erpnext"
  ],
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "editor.rulers": [120]
}
```

Get the exact interpreter path:
```bash
which python  # run inside the bench env: cd frappe-bench && source env/bin/activate
```

## Useful development commands

```bash
# Hot-reload JS/CSS changes (run alongside bench start)
bench watch

# Python REPL with Frappe context
bench --site site1.local console

# Run a specific function
bench --site site1.local execute myapp.module.function --args '{"key": "val"}'

# Run tests for an app
bench --site site1.local run-tests --app myapp

# Run tests for a specific module
bench --site site1.local run-tests --module myapp.tests.test_mymodule

# Migrate after DocType changes
bench --site site1.local migrate

# Clear cache
bench --site site1.local clear-cache

# Check bench and app versions
bench version
```

## Common setup errors and fixes

| Error | Fix |
| --- | --- |
| `mysql_secure_installation` fails - no root password | Run `sudo mysql -u root` first, set password with `ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';` |
| `bench init` fails: `node: command not found` | nvm not loaded. Run `source ~/.bashrc` or open a new terminal |
| `bench new-site` fails: `Access denied for user 'root'` | Wrong MariaDB root password. Reset with `sudo mysql -u root -e "ALTER USER..."` |
| `bench start` fails: port 8000 in use | `lsof -i :8000` to find the process; kill it or change the port in `Procfile` |
| `bench get-app` fails: SSH key not set up | Add your SSH key to GitHub: `ssh-keygen -t ed25519 && cat ~/.ssh/id_ed25519.pub` → add to GitHub |
| `ModuleNotFoundError` after installing app | `bench --site sitename migrate` then restart bench |
| `character set` error on `bench new-site` | MariaDB charset not set to utf8mb4. Check the config section above. |

## Faircode project conventions

- Always use a version-specific branch (`version-14`, `version-15`, `version-16`).
  Never use `develop` - it may have unreleased breaking changes.
- One bench per major version. Don't mix v14 and v15 apps in the same bench.
- Use `bench watch` during development - restarting bench for every JS change wastes time.
- Name your site to match the project: `clientname.local` (easier to manage multiple sites).

## Definition of Done
- `bench start` runs without errors.
- Site accessible at `http://sitename.local:8000` and ERPNext desk loads.
- Custom app installed and migrations run.
- VSCode Python interpreter points to the bench virtualenv.
- `bench run-tests --app myapp` runs without import errors.

## Related Skills
`frappe-ops-bench`, `frappe-ops-deployment`, `frappe-testing-unit`
