from django.urls import path

from .views import TicketFormView, SuccessView

app_name = "fast_ticket"

urlpatterns = [
    path('', TicketFormView.as_view(), name='buy_ticket'),
    path('success/', SuccessView.as_view(), name='success'),
]
