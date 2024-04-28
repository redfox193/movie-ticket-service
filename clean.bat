docker-compose down
docker rmi iticket-flower:latest
docker rmi iticket-payment:latest
docker rmi iticket-kino:latest
docker rmi iticket-celery:latest
docker rmi redis:alpine
docker rmi postgres:13.3
docker volume rm iticket_kino_db_data
rm payment_service/data/db.sqlite3
