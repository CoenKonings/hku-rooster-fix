from .views import CreateFeedView
from django.urls import path


urlpatterns = [path("", CreateFeedView.as_view())]
