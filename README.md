# Foodgram - сервис для публикации информации о кошках.
## Описание проекта
Позволяет регистрироваться, добавлять информацию о питомцах (в том числе добавлять фотографию и описание достижений).

## Инструкция по запуску

### Требования:
на сервере должны стоять:
- Настроенный Nginx
- Docker
- Docker Compose

### Запуск:
- Внесите изменения в конфигурацию веб-сервера для перенаправления запросов к ресурсу на порт 9000 приложения, запущенного в Docker:
```
   location / {
         proxy_pass http://127.0.0.1:9000;
   }

```
- Проверьте конфигурацию и перезагрузите Nginx:
```
sudo nginx -t
sudo systemctl reload nginx
```
- Создайте рабочую директорию и перейдите в неё:
```
mkdir foodgram
cd foodgram
```

- Создайте в ней файл *.env* с переменными окружения. Пример содержимого файла:
```
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432
```

- Скачайте оркестрационный файл
```
wget https://github.com/ankor2023/foodgram-project-react/blob/main/docker-compose-production.yml
```

- Запустите контейнеры
```
sudo docker compose -f docker-compose-production.yml up -d

```
- Выполните миграции, соберите статику
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend python cp -r /app/collected_static/. /backend_static/static/
``` 


## Используемые технологии:
- Django
- DRF
- Docker
- Nginx

## Информация об авторе:
[Яндекс Практикум](http://praktikum.yandex.ru)

