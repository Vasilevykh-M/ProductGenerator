#!/bin/bash

# Параметры базы данных
DB_NAME="dbname"
DB_USER="user"
DB_PASSWORD="password"

# Функция для ожидания доступности PostgreSQL
wait_for_postgres() {
    until psql -U postgres -c '\q'; do
        echo "Ожидание запуска PostgreSQL..."
        sleep 2
    done
}

# Ожидание доступности PostgreSQL
wait_for_postgres

# Проверка, существует ли база данных
if ! psql -U postgres -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Создание базы данных $DB_NAME..."
    psql -U postgres -c "CREATE DATABASE $DB_NAME;"
    psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    echo "База данных и пользователь успешно созданы."
else
    echo "База данных $DB_NAME уже существует."
fi
