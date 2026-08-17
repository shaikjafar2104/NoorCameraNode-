from __future__ import annotations

import array
import base64
import io
import json
import math
import os
import signal
import subprocess
import tempfile
import time
import urllib.request
import wave


BRAIN_URL = os.getenv("NOORBRAIN_URL", "http://192.168.2.94:8001").rstrip("/")
CAPTURE_DEVICE = os.getenv("NOORBRAIN_CAPTURE_DEVICE", "hw:CARD=C920,DEV=0")
PLAYBACK_DEVICE = os.getenv("NOORBRAIN_PLAYBACK_DEVICE", "plughw:CARD=Headphones,DEV=0")
RATE = 16000
CHANNELS = 2
CHUNK_SECONDS = 1
MIN_RMS = int(os.getenv("NOORBRAIN_VOICE_RMS", "350"))
NOISE_SAMPLES_REQUIRED = 2
MAX_SPEECH_CHUNKS = 4
RUNNING = True


def stop(*_):
    global RUNNING
    RUNNING = False


signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)


def capture_chunk() -> bytes:
    completed = subprocess.run(
        ["arecord", "-q", "-D", CAPTURE_DEVICE, "-t", "raw", "-f", "S16_LE", "-r", str(RATE), "-c", str(CHANNELS), "-d", str(CHUNK_SECONDS)],
        capture_output=True,
        timeout=CHUNK_SECONDS + 4,
        check=False,
    )
    return completed.stdout if completed.returncode == 0 else b""


def stereo_to_mono(raw: bytes) -> bytes:
    samples = array.array("h")
    samples.frombytes(raw[: len(raw) - len(raw) % 4])

    mono = array.array("h")

    for i in range(0, len(samples) - 1, 2):
        value = int((samples[i] + samples[i + 1]) / 2)
        mono.append(max(-32768, min(32767, value)))

    return mono.tobytes()


def rms(raw: bytes) -> int:
    if len(raw) < 4:
        return 0

    mono = stereo_to_mono(raw)
    samples = array.array("h")
    samples.frombytes(mono)

    return int(math.sqrt(
        sum(value * value for value in samples)
        / max(1, len(samples))
    ))


def wav_bytes(raw: bytes) -> bytes:
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(RATE)
        wav.writeframes(raw)
    return output.getvalue()


def post_audio(raw: bytes) -> dict:
    payload = json.dumps({"audio_base64": base64.b64encode(wav_bytes(stereo_to_mono(raw))).decode("ascii")}).encode()
    request = urllib.request.Request(
        BRAIN_URL + "/api/pi-wake-v16/process",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode())


def chime() -> None:
    frames = bytearray()
    for frequency in (660, 880):
        for index in range(int(RATE * 0.10)):
            value = int(7000 * math.sin(2 * math.pi * frequency * index / RATE))
            frames.extend(int(value).to_bytes(2, "little", signed=True))
    play(wav_bytes(bytes(frames)))


def play(audio: bytes) -> None:
    with tempfile.NamedTemporaryFile(suffix=".wav") as file:
        file.write(audio)
        file.flush()
        subprocess.run(["aplay", "-q", "-D", PLAYBACK_DEVICE, file.name], timeout=120, check=False)


def main() -> None:
    print(
        f"HALO LISTENER READY brain={BRAIN_URL} "
        f"mic={CAPTURE_DEVICE} speaker={PLAYBACK_DEVICE}",
        flush=True,
    )

    # Keep previous audio so wake word is never cut off.
    preroll = []
    noise_samples = []
    ignore_until = 0.0

    while RUNNING:
        raw = capture_chunk()

        if not raw:
            continue

        if time.time() < ignore_until:
            preroll.clear()
            continue

        level = rms(raw)

        if len(noise_samples) < 3:
            noise_samples.append(level)
            preroll.append(raw)
            preroll = preroll[-2:]
            continue

        noise = sum(noise_samples[-10:]) / len(noise_samples[-10:])
        threshold = max(MIN_RMS, int(noise * 2.0))

        if level < threshold:
            noise_samples.append(level)
            noise_samples = noise_samples[-10:]

            preroll.append(raw)
            preroll = preroll[-2:]
            continue

        # Speech detected.
        # Include up to 2 seconds BEFORE trigger.
        speech = list(preroll)
        speech.append(raw)
        preroll.clear()

        # Capture remainder of command.
        silent = 0

        for _ in range(4):
            next_chunk = capture_chunk()

            if not next_chunk:
                break

            speech.append(next_chunk)

            if rms(next_chunk) < threshold:
                silent += 1
                if silent >= 1:
                    break
            else:
                silent = 0

        try:
            started = time.time()

            result = post_audio(b"".join(speech))

            print(
                json.dumps(
                    {
                        k: result.get(k)
                        for k in (
                            "status",
                            "text",
                            "command",
                            "reply",
                        )
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

            print(
                f"ROUND_TRIP={time.time() - started:.2f}s",
                flush=True,
            )

            status = result.get("status")

            if status in {"awake", "handled"}:
                response_audio = result.get("response_audio") or {}
                encoded = response_audio.get("audio_base64")

                if encoded:
                    play(base64.b64decode(encoded))
                else:
                    chime()

                ignore_until = time.time() + 1.5
                preroll.clear()

        except Exception as error:
            print(
                f"WAKE REQUEST ERROR: "
                f"{type(error).__name__}: {error}",
                flush=True,
            )
            time.sleep(0.5)

if __name__ == "__main__":
    main()
