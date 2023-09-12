from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Track, Course


class CreateFeedView(TemplateView):
    template_name = "rooster_import/create-calendar-form.html"

    def get(self, request):
        tracks = Track.objects.all()
        courses = Course.objects.all()

        return render(request, self.template_name, {"tracks": tracks, "courses": courses})
