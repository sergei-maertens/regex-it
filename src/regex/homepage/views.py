from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = "homepage/base.html"


class ContactView(TemplateView):
    template_name = "homepage/contact.html"
