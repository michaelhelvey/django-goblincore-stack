from django.views.generic import TemplateView


class UserProfileView(TemplateView):
    template_name = "accounts/profile.html"
