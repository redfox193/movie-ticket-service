docker-compose down
docker rmi iticket-flower:latest
docker rmi iticket-payment:latest
docker rmi iticket-kino:latest
docker rmi iticket-celery:latest
docler rmi iticket-payment_db_migration:latest
docker rmi iticket-kino_db_migration:latest
docker rmi redis:alpine
docker rmi postgres:13.3
docker volume rm iticket_kino_db_data
del payment_service\data\db.sqlite3
