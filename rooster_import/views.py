from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from .models import Track, Course
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json


class CreateFeedView(TemplateView):
    template_name = "rooster_import/create-calendar-form.html"

    def get(self, request):
        tracks = Track.objects.all()
        courses = Course.objects.all()

        return render(request, self.template_name, {"tracks": tracks, "courses": courses})


    def post(self, request):
        print("GOT POST")
        print(request)
        response = {"icalUrl": "succes!"}
        return JsonResponse(response)
