from django.urls import path
from . import views

app_name = 'episodes'

urlpatterns = [
        # Home page
        path('home/', views.index, name="index"),

        # Podcasts page
        path('podcasts/', views.PodcastsPageView.as_view(), name="podcasts"),

        # About page
        path('about/', views.about, name="about"),

        # Page Not Found
        path('Page_Not_Found/', views.Not_Found_404, name="Not_Found")
        ]
