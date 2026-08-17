#!/usr/bin/env bash
set -euo pipefail

REPO="/home/project/Projects/NoorCameraNode"

cd "$REPO"

echo "========== NOOR CAMERA NODE UPDATE =========="
echo "Current: $(git rev-parse --short HEAD)"

git fetch origin main
git pull --ff-only origin main

echo "Updated: $(git rev-parse --short HEAD)"

echo
echo "========== CAMERA RESTART =========="
sudo systemctl restart noor-camera.service
sleep 5
systemctl is-active noor-camera.service

echo
echo "========== AUDIO =========="
if systemctl list-unit-files | grep -q '^noorbrain-pi-audio.service'; then
    sudo systemctl restart noorbrain-pi-audio.service
    sleep 3
    systemctl is-active noorbrain-pi-audio.service
else
    echo "AUDIO_SYSTEMD_NOT_INSTALLED_YET"
fi

echo
echo "========== PORTS =========="
ss -lntp | grep -E ':8000|:8010' || true

echo
echo "========== AUDIO HEALTH =========="
curl -fsS http://127.0.0.1:8010/health || true
echo

echo "========== UPDATE COMPLETE =========="
