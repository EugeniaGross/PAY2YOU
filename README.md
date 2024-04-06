# PAY2YOU API
Pay2you API - это MVP API для мобильного приложения Pay2You, которое позволяет пользователям управлять своими подписками на сервисы. API предоставляет информацию аудентифицированным пользователям о серивисах, подписках пользователя, о расходах и о кэшбеке. Так же аудентифицированный пользователь может подключить, отключить и возобновить подписку.
С документацией можно ознакомиться по адресу <https://pay2you.sytes.net/api/v1/swagger/>.
# Запуск проекта через docker compose на локальной машине
1. Склонировать проект на свой компьютер
   ```
   git clone git@github.com:EugeniaGross/PAY2YOU.git
   ```
2. В папке foodgram_backend создать .env со следующими данными
   ```
   POSTGRES_USER = postgres # пользователь
   POSTGRES_PASSWORD = postgres # пароль
   POSTGRES_DB = postgres # имя базы данных
   DB_HOST = db # название контейнера, отвечающего за базу данных
   DB_PORT = 5432 # порт
   SEKRET_KEY = # секретный ключ Django-проекта
   DEBUG = # режим отладки (True или False)
   ALLOWED_HOSTS = [] # разрешенные хосты
   REDIS_PASSWORD=my-password
   REDIS_PORT=6379
   REDIS_DATABASES=16
   CELERY_BROKER_URL=redis://redis:6379
   CELERY_RESULT_BACKEND=redis://redis:6379
   ```
2. Запустить оркестр контейнеров из корневой папки проекта
   ```
   docker compose up
   ```
4. Cобрать и копировать статику бэкенда, выполнить миграции.
   ```
   docker compose exec backend python manage.py collectstatic

   docker compose exec backend cp -r /app/static/. /backend_static/static/

   docker compose exec backend python manage.py migrate

   ```
# Технологии
Django, Django REST Framework, Celery, Redis, Gunicorn, Nginx, Docker, Docker compose
# Автор бэкенда
[Евгения Гросс!](https://github.com/EugeniaGross/ 'Ссылка на GitHub') и Алексей Тихомиров <https://github.com/sorath2><br>
