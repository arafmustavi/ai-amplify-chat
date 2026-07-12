# Homelab Deployment (arafhomelab)

## 1. Prepare the host

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```

## 2. Clone + configure

```bash
git clone https://github.com/arafmustavi/amplify.git
cd amplify
cp .env.example .env
```

## 3. Protect the dashboard (optional)

```bash
sudo apt install -y apache2-utils
htpasswd -c docker/.htpasswd admin
```

## 4. Bring it up

```bash
docker compose up -d --build
docker compose ps
```

## 5. Expose to the internet

**Option A — Cloudflare Tunnel (recommended)**

```bash
cloudflared tunnel create amplify
cloudflared tunnel route dns amplify chat.example.com
cloudflared tunnel run amplify
```

**Option B — router port-forward:** forward 80/443 → homelab IP.
