#!/bin/bash
echo "Starting FastAPI Backend..."
python -m uvicorn backend.main:app --reload --port 8000

