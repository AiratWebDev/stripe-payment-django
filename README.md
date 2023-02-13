# Подключение платежной системы Stripe

### Описание проекта 

Проект для тестового задания. Представляет собой реализацию подключения к Stripe API с помощью сессий для совершений оплаты выбранного товара.

Ссылка на выложененный проект: https://1255351-cc91283.tw1.ru/

### Стэк разработки:
• Python 3.11  
• Django 4.1.6   
• Docker  
• Nginx latest  

### Запуск

Используя Django:
```python
python manage.py runserver
```
Используя Docker-Compose:
```docker
docker compose -f docker-compose.yaml up -d
```
Используя Docker:
```
docker build -t вашеимяобраза .
docker run -d --name вашеимяконтейнера -p 80:80 вашеимяобраза
```
