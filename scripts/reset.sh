docker compose down
docker volume rm multitenant_postgres_data
docker compose build && docker compose up -d --force-recreate &&
sleep 5 &&
docker compose exec web python manage.py makemigrations users app tenants &&
docker compose exec web python manage.py migrate
