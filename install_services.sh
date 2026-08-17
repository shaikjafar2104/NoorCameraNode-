#!/usr/bin/env bash
# ============================================================
# NoorCameraNode installer — safely installs and enables
# camera + Pi audio systemd services.
# ============================================================
set -euo pipefail

REPO="/home/project/Projects/NoorCameraNode"
AUDIO_SERVICE="noorbrain-pi-audio.service"
CAMERA_SERVICE="noor-camera.service"
TOKEN_FILE="/home/project/.config/noorbrain/pi-audio-node.token"

echo "========== NOORCAMERA INSTALLER =========="

# --- Verify token exists and is non-empty ---
if [ ! -f "$TOKEN_FILE" ]; then
    echo "ERROR: Token file not found at $TOKEN_FILE" >&2
    exit 1
fi
TOKEN_LEN=$(wc -c < "$TOKEN_FILE")
if [ "$TOKEN_LEN" -lt 10 ]; then
    echo "ERROR: Token file appears empty or too short" >&2
    exit 1
fi
echo "Token file verified (length: ${TOKEN_LEN} bytes) — token NOT displayed."

# --- Install audio service ---
echo "Installing Pi audio service..."
sudo cp "$REPO/$AUDIO_SERVICE" "/etc/systemd/system/$AUDIO_SERVICE"
sudo systemctl daemon-reload
sudo systemctl enable "$AUDIO_SERVICE"

# Verify trusted=true from the audio node health
echo "Starting Pi audio service..."
sudo systemctl start "$AUDIO_SERVICE"
sleep 3

if ! systemctl is-active --quiet "$AUDIO_SERVICE"; then
    echo "ERROR: $AUDIO_SERVICE failed to start" >&2
    sudo journalctl -u "$AUDIO_SERVICE" -n 20 --no-pager
    exit 1
fi

# Verify port 8010
if ss -lntp | grep -q ':8010'; then
    echo "Port 8010: LISTENING"
else
    echo "ERROR: Port 8010 not listening" >&2
    exit 1
fi

# Verify /health endpoint
HEALTH=$(curl -fsS http://127.0.0.1:8010/health 2>/dev/null || echo "")
if echo "$HEALTH" | python3 -c "import sys,json; d=json.load(sys.stdin); assert d.get('trusted') is True" 2>/dev/null; then
    echo "Audio health: trusted=true ✓"
else
    echo "ERROR: Audio health check failed or trusted != true" >&2
    echo "$HEALTH"
    exit 1
fi

# --- Restart camera service ---
echo "Restarting camera service..."
if systemctl list-unit-files | grep -q "^$CAMERA_SERVICE"; then
    sudo systemctl restart "$CAMERA_SERVICE"
    sleep 2
    if systemctl is-active --quiet "$CAMERA_SERVICE"; then
        echo "Camera service: active ✓"
    else
        echo "WARNING: Camera service failed to start" >&2
    fi
else
    echo "WARNING: $CAMERA_SERVICE not installed yet — skipping"
fi

# --- Verify camera health ---
CAMERA_HEALTH=$(curl -fsS http://127.0.0.1:8000/health 2>/dev/null || echo "")
if [ -n "$CAMERA_HEALTH" ]; then
    echo "Camera health: $CAMERA_HEALTH"
else
    echo "WARNING: Camera health endpoint returned error"
fi

echo
echo "========== INSTALL COMPLETE =========="
