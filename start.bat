docker-compose up -d payment
docker-compose exec payment python manage.py migrate
docker-compose up -d kino
docker-compose exec kino alembic upgrade head
docker-compose up -d