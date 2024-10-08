# Документация к приложению ProductGenerator

## Описание приложения

**ProductGenerator** — это мощное веб-приложение, использующее современные технологии машинного обучения для генерации и обработки изображений и текстов. Основные функции приложения включают:

1. **Удаление фона** — использование модели ONNX для высококачественного удаления фона с изображений, InSPyReNet .
2. **Генерация фона** — интеграция модели от Yahoo для автоматического создания фонов, что позволяет улучшить визуальное представление изображений, yahoo-inc/photo-background-generation.
3. **Генерация описаний продуктов** — использование модели GPT-2 для создания текстовых описаний на основе изображений, что упрощает процесс создания контента для маркетинга, GPT-2 Product Description Generator.

### Используемые модели

1. **[https://github.com/plemeri/InSPyReNet](Remover.onnx)**: Модель для удаления фона с изображений, обеспечивающая высокую точность.
2. **[https://github.com/openai/CLIP](CLIP (clip.onnx))**: Модель для связывания изображений с текстовыми описаниями.
3. **[yahoo-inc/photo-background-generation](https://huggingface.co/yahoo-inc/photo-background-generation)**: Генерация фонов для изображений.
4. **[HamidRezaAttar/gpt2-product-description-generator](https://huggingface.co/HamidRezaAttar/gpt2-product-description-generator)**: Автоматическое создание описаний для продуктов.

### Архитектура

Приложение состоит из двух основных компонентов:

- **Фронтенд**: Создан на React для интерактивного пользовательского интерфейса.
- **Бэкенд**: Реализован с использованием FastAPI, который обеспечивает API для обработки запросов и выполнения необходимых операций с моделями.

## Инструкция по развертыванию

### Требования

- Установленный Docker версии 19.03+ с поддержкой NVIDIA (nvidia-docker2).
- NVIDIA драйвера версии CUDA 11.7+ на хосте.

### Шаги по развертыванию

1. **Клонируйте репозиторий**:

   ```bash
   git clone https://github.com/Vasilevykh-M/ProductGenerator.git
   cd ProductGenerator

2. **Соберите и запустите контейнеры**:

   ```bash
   docker-compose up --build

3. **Выполнение миграций базы данных**:


   ``` bash

   docker-compose exec web alembic upgrade head

4. **Доступ к приложению**:

После успешного запуска откройте браузер и перейдите по адресу: http://localhost. Приложение будет доступно через Nginx, обслуживающий React-фронтенд и FastAPI бэкенд.
