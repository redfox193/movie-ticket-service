import os

import grpc
from .generated_code.iticket_pb2 import UserRequest, DatesResponse
from .generated_code.iticket_pb2_grpc import ITicketStub

from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from .models import History
from datetime import datetime

kino_service_host = os.getenv("KINO_SERVICE_HOST", "localhost")
kino_service_channel = grpc.insecure_channel('kino:50051')
kino_service_client = ITicketStub(kino_service_channel)


@shared_task()
def send_ticket_email_task(film_id, film, cost, email):
    req = UserRequest(film_id=int(film_id))
    code_response = kino_service_client.genCode(req)
    film_dates_response = kino_service_client.getDates(req)
    sleep(5)
    new_history = History(
        film=film,
        email=email,
        code=code_response.code,
        date=datetime.now()
    )
    new_history.save()
    sleep(5)
    send_mail(
        "Thanks for using iTicket! Your receipt.",
        f"Purchase date\t{new_history.date}\n"
        f"Cost \t\t{cost}\n\n"
        f"Film\t\t{new_history.film}\n"
        f"Code\t\t\t{new_history.code}\n"
        f"Premiere dates\t{', '.join(film_dates_response.dates)}",
        "iticket@ishop.com",
        [new_history.email],
        fail_silently=False,
    )
