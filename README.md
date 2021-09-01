### Тестовое задание. Сервис доски объявлений.  

Установка зависимостей
```shell
pip install -r requirements.txt
```

В базе данных должно быть установлено расширение pg_trgm для поиска по тексту
```sql
CREATE EXTENSION pg_trgm;
```

Запуск
```shell
python manage.py runserver
```

В папке http_requests созданы наборы запросов для проверки работы АПИ
