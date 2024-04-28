from django.views.generic import FormView, TemplateView

from .forms import TicketForm


class TicketFormView(FormView):
    template_name = "ticket/ticket.html"
    form_class = TicketForm
    success_url = "/success/"

    def form_valid(self, form):
        form.send_ticket()
        return super().form_valid(form)


class SuccessView(TemplateView):
    template_name = "ticket/success.html"
