from django.shortcuts import render
from django.views.generic import TemplateView


class CreateFeedView(TemplateView):
    template_name = "rooster_import/test.html"
