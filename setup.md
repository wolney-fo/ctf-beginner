# Deployment

The app is intentionally lightweight and runs on any Linux host with `systemd`
and `sudo` — a local VM, a spare box, or a cloud instance from any provider
(AWS, GCP, Azure, DigitalOcean, Hetzner, ...). Nothing here is tied to a specific
cloud.

## Requirements

- A Linux host with **Ubuntu 22.04/24.04** (or any Debian-based, systemd distro).
- **Inbound TCP 80** open to whoever will play (and **22** for your own SSH).
- `sudo` access.

## One-command setup (recommended)

SSH into the host and run:

```bash
sudo apt-get update -y && sudo apt-get install -y git
git clone https://github.com/wolney-fo/ctf-beginner.git
cd ctf-beginner
sudo bash setup.sh
```

The script installs dependencies, generates **random flags** (without printing
them), seeds the database, and starts the app as a systemd service. It prints the
URL when it finishes.

Then open `http://<SERVER_IP>/` and share the link with your participants.

> Want it on a different port? Run `sudo PORT=8080 bash setup.sh`.

## Service management

```bash
systemctl status ctf-nimbus       # is it running?
sudo systemctl restart ctf-nimbus # restart (resets sessions, not the flags)
journalctl -u ctf-nimbus -n 50    # logs, if something goes wrong
```

To **regenerate the flags** from scratch, run `sudo bash setup.sh` again.

## Local development (no service)

```bash
cd app
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# provide flags for local runs:
cat > flags.json <<'JSON'
{"recon":"FLAG{recon_dev}","backup":"FLAG{bkp_dev}","auth":"FLAG{auth_dev}",
 "idor":"FLAG{idor_dev}","privesc":"FLAG{priv_dev}","devnotes":"FLAG{note_dev}"}
JSON
python seed_db.py
python app.py            # serves on http://localhost:8080
```

## Teardown

Stop and remove the service and app directory:

```bash
sudo systemctl disable --now ctf-nimbus
sudo rm -f /etc/systemd/system/ctf-nimbus.service
sudo rm -rf /opt/ctf-nimbus
sudo systemctl daemon-reload
```

On a cloud provider, simply deleting/terminating the instance is enough.
