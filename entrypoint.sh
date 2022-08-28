#!/bin/bash

set -e

python -m todo.create_db

exec uvicorn todo.api:app --host 0.0.0.0 --port 8000 --reload