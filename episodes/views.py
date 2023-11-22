from django.shortcuts import render
from django.views.generic import ListView
from .models import Episode

# Create your views here.

def index(request):
    """Home page view"""
    template_name = 'index.html'
    return render(request, template_name)

class PodcastsPageView(ListView):
    """Retrieves episodes from the database"""
    template_name = 'episodes.html'
    model = Episode

    def get_context_data(self, **kwargs):
        """Retrieves podcast episodes"""
        context = super().get_context_data(**kwargs)
        context['episodes'] = Episode.objects.filter().order_by('-pub_date')[:10]
        return (context)
