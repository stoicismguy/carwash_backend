# Запуск
1. Создать файл ```.env``` по примеру ```.env.example```
2. ```docker compose up -d``` - собрать и запустить контейнеры
3. ```docker exec -it <container_name> poetry run src/manage.py createsuperuser``` - создать админского пользователя

# Команды Poetry
```poetry add <package-name>``` - добавить библиотеку в сбоорку\
```poetry run <command>``` - выполнить команду из под venv