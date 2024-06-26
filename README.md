# movie-ticket-service
A project which represents a service for buying online tickets for movies. It uses such technologies as gRPC and async integration with Celery.

## Requirements
_[Docker](https://docs.docker.com/get-docker/)_ and a tool to work with databases (optional, if you want to see the data stored)

## Usage

#### Run
Create ```.env``` at the root as ```.env.example```.

Tu run services use: 
```shell
docker-compose up -d
```
After that go to http://localhost:8000 to test service.
Additionally following endpoints are available:

http://localhost:5555 - here you can monitor tasks using _[flower](https://pypi.org/project/flower/)_

http://localhost:5432 - kino service database.

Postgres database is in volume ```iticket_kino_db_data``` and sqlite database
is mounted in ```payment_service/data```.

#### Stop

Use ```clean.bat``` to stop application and clean data. Or ```docker-compose down``` to stop all containers.

## Architecture
An application consists of two microservices, ```kino_service``` and ```payment_service```.

```kino_service``` represents a service which stores information about movies (cost, streaming dates)
and iticket codes, which you can use to watch certain movie. It uses _gRPC_ architecture to provide an API,
_PostgreSQL_ to store data.

```payment_service``` represents a service based on _Django_, which provides a form for buying itickets (unique code which can be used to
watch certain movie one time). Additionally, it stores history of all purchases in _SQLite_
database. The process of buying consist of:

1. User chooses film, inputs card information and sends form.
2. Service sends a new task into _Redis_ task queue and a success window to user. 
3. Celery worker processes this task 
   - makes a grpc call to get a unique code, which is generated and stored in ```kino_service``` database
   - saves a record of a new purchase into ```payment_service``` database
   - sends email (actually prints it in celery worker's container logs)
   - ends task

To see if email was sent run this command in terminal (email is not sent instantly to emulate background task):

```shell
docker logs iticket-celery-1 # iticket-celery-1 is the container with celery worker
```
