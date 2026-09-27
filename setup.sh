#!/usr/bin/env bash
#
# setup.sh - Provision the "Nimbus Logistics" CTF on any Ubuntu/Debian Linux host.
#
# Works on any server: a local VM, a Raspberry Pi, or a cloud instance from any
# provider. Requires a systemd-based Linux with sudo access.
#
# Usage (as a user with sudo):
#   git clone https://github.com/wolney-fo/ctf-beginner.git
#   cd ctf-beginner
#   sudo bash setup.sh
#
# This script does NOT print the flag values. They live only in app/flags.json on
# the host, so whoever provisions the box can play without spoilers.
#
set -euo pipefail

APP_USER="ctf"
APP_HOME="/opt/ctf-nimbus"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE="/etc/systemd/system/ctf-nimbus.service"
PORT="${PORT:-80}"

if [[ $EUID -ne 0 ]]; then
  echo "Please run with sudo: sudo bash setup.sh" >&2
  exit 1
fi

echo "[*] Installing system dependencies..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3 python3-venv python3-pip

echo "[*] Creating service user and application directory..."
id -u "$APP_USER" &>/dev/null || useradd --system --create-home --home-dir "/home/$APP_USER" --shell /usr/sbin/nologin "$APP_USER"
mkdir -p "$APP_HOME"
cp -r "$REPO_DIR/app/." "$APP_HOME/"

echo "[*] Generating random flags (values are not printed)..."
gen() { head -c 18 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9' | head -c 12; }
cat > "$APP_HOME/flags.json" <<EOF
{
  "recon":    "FLAG{recon_$(gen)}",
  "backup":   "FLAG{bkp_$(gen)}",
  "auth":     "FLAG{auth_$(gen)}",
  "idor":     "FLAG{idor_$(gen)}",
  "privesc":  "FLAG{priv_$(gen)}",
  "devnotes": "FLAG{note_$(gen)}"
}
EOF

echo "[*] Generating the exposed backup file with the flag injected..."
BACKUP_FLAG=$(python3 -c "import json;print(json.load(open('$APP_HOME/flags.json'))['backup'])")
sed "s|__BACKUP_FLAG__|$BACKUP_FLAG|" \
  "$APP_HOME/static/old_backups/app.py.bak.template" \
  > "$APP_HOME/static/old_backups/app.py.bak"
rm -f "$APP_HOME/static/old_backups/app.py.bak.template"

echo "[*] Creating virtualenv and installing Python packages..."
python3 -m venv "$APP_HOME/venv"
"$APP_HOME/venv/bin/pip" install --upgrade pip >/dev/null
"$APP_HOME/venv/bin/pip" install -r "$APP_HOME/requirements.txt" >/dev/null

echo "[*] Seeding the database..."
"$APP_HOME/venv/bin/python" "$APP_HOME/seed_db.py"

echo "[*] Fixing permissions..."
chown -R "$APP_USER:$APP_USER" "$APP_HOME"
chmod 600 "$APP_HOME/flags.json"

echo "[*] Installing systemd service..."
cat > "$SERVICE" <<EOF
[Unit]
Description=CTF Nimbus Logistics
After=network.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$APP_HOME
ExecStart=$APP_HOME/venv/bin/gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
AmbientCapabilities=CAP_NET_BIND_SERVICE
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ctf-nimbus >/dev/null 2>&1
systemctl restart ctf-nimbus

sleep 2
if systemctl is-active --quiet ctf-nimbus; then
  IP=$(curl -s --max-time 5 ifconfig.me || echo "YOUR_SERVER_IP")
  echo ""
  echo "======================================================"
  echo " CTF is up!  Visit:  http://$IP/"
  echo " Service: systemctl status ctf-nimbus"
  echo " (flag values live only in $APP_HOME/flags.json)"
  echo "======================================================"
else
  echo "[!] The service did not start. Check: journalctl -u ctf-nimbus -n 50" >&2
  exit 1
fi
