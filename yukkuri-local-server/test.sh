#!/usr/bin/env bash
set -euo pipefail
curl -fsS http://127.0.0.1:8765/health
printf '\n'
curl -fsS -X POST http://127.0.0.1:8765/speak -H 'Content-Type: application/json' -d '{"text":"いち に さん よん"}' -o /tmp/yukkuri-test.wav
file /tmp/yukkuri-test.wav
