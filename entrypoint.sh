#!/bin/sh

# Запуск Nginx для обслуживания фронтенда
nginx &

# Запуск FastAPI (Uvicorn) с поддержкой GPU
uvicorn app.backend.main:app --host 0.0.0.0 --port 8500 --reload
