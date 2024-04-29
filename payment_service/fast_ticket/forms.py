import os
from django import forms
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
from .task import send_ticket_email_task

import grpc
from .generated_code.iticket_pb2 import UserRequest, google_dot_protobuf_dot_empty__pb2
from .generated_code.iticket_pb2_grpc import ITicketStub


kino_service_host = os.getenv("KINO_SERVICE_HOST", "localhost")
kino_service_channel = grpc.insecure_channel(f"{kino_service_host}:50051")
kino_service_client = ITicketStub(kino_service_channel)


class TicketForm(forms.Form):
    film = forms.ChoiceField(label='Choose a Film')
    email = forms.EmailField(label='Почта')
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        kino_service_response = kino_service_client.getPremieres(google_dot_protobuf_dot_empty__pb2.Empty())

        self.films = {}
        dynamic_choices = []
        for film in kino_service_response.premieres:
            self.films[str(film.id)] = {
                'cost': film.cost,
                'name': film.name
            }
            dynamic_choices.append((film.id, f"{film.name} ({film.cost} $)"))
        self.fields['film'].choices = dynamic_choices

    def send_ticket(self):
        send_ticket_email_task.delay(
            self.cleaned_data["film"],
            self.films[self.cleaned_data["film"]]['name'],
            self.films[self.cleaned_data["film"]]['cost'],
            self.cleaned_data["email"]
        )
