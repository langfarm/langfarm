#!/bin/sh

source .venv/bin/activate

uvicorn langfarm_tracing.main:app --host 0.0.0.0 --port 3080 --env-file .env
