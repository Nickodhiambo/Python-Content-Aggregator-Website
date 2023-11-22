from django.urls import path
from . import views

app_name = 'episodes'

urlpatterns = [
        # Home page
        path('home/', views.index, name="index"),

        # Podcasts page
        path('podcasts/', views.PodcastsPageView.as_view(), name="podcasts"),
        ]
