# Базовый образ с поддержкой NVIDIA
FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

# Установка необходимых системных зависимостей
RUN apt-get update && apt-get install -y \
    python3-pip \
    nginx \
    wget \
    curl \
    gnupg2 \
    ca-certificates \
    lsb-release \
    software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# Установка Node.js для сборки React-приложения
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Установка рабочей директории для приложения
WORKDIR /app

# --- Этап 1: Сборка фронтенда ---
# Копируем файлы фронтенда
COPY frontend/package*.json ./frontend/

# Переходим в директорию фронтенда и устанавливаем зависимости
WORKDIR /app/frontend
RUN npm install

# Копируем исходный код фронтенда и создаем production-сборку
COPY frontend/ ./
RUN npm run build

# --- Этап 2: Установка бэкенда ---
WORKDIR /app/backend

# Копируем файл зависимостей Python
COPY backend/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Копируем исходный код бэкенда
COPY backend/ /app/backend/

# Скачивание моделей (если требуются)
RUN wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1C1smXa0NJNYmg-guKOku6pwqEgMVGm3x' -O /app/backend/remover.onnx && \
    wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Zj-NoVVt88kdiIPbeeaDkdZbUF4ilkjQ' -O /app/backend/clip.onnx

# --- Этап 3: Настройка Nginx и финальные действия ---
WORKDIR /app

# Копируем конфигурационный файл Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем собранные статические файлы фронтенда в директорию для Nginx
RUN mkdir -p /usr/share/nginx/html
COPY --from=frontend-build /app/frontend/build /usr/share/nginx/html

# Копируем скрипт для запуска всех сервисов
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Экспонирование порта 80
EXPOSE 80

# Запуск сервиса
CMD ["/app/entrypoint.sh"]
