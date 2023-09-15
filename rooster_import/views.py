from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Track, Course
from django.http import JsonResponse
from .helpers import parse_request
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
import json


class CreateFeedView(TemplateView):
    template_name = "rooster_import/create-calendar-form.html"

    @ensure_csrf_cookie
    def get(self, request):
        tracks = Track.objects.all()
        courses = Course.objects.all()

        return render(
            request, self.template_name, {"tracks": tracks, "courses": courses}
        )

    def post(self, request):
        request_body = json.loads(request.body)
        response = parse_request(request_body)
        return JsonResponse(response)
