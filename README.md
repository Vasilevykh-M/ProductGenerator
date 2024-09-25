# Background generator
- yahoo-inc/photo-background-generation генерация фона
- CLIP генерация промта по исходномуи изображению
- InSPyReNet получения маски обьекта на изображкении



### Минимальные системные требования
NVIDIA GPU с 16gb VRAM и выше

### Сборка докера
docker build --tag app_lerua .

### Запуск докера
docker run -it --gpus='all,"capabilities=compute"' \\
    --ipc=host --ulimit nofile=5000:5000 -p 80:80 app_lerua
### Эндпоинт

http://team-name.shop:61035 - фронт

http://team-name.shop:61035/api - api
