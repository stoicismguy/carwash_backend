# Запуск
1. Создать файл .env по примеру .env.example
2. ```docker compose up -d```
3. ```docker exec -it <container_name> poetry run src/manage.py createsuperuser```

# Команды Poetry
```poetry add <package-name>``` - добавить библиотеку в сбоорку\
```poetry run <command>``` - выполнить команду из под venv