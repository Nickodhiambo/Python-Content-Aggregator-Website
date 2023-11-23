from django.test import TestCase
from django.utils import timezone
from .models import Episode
from django.urls.base import reverse
from . import urls

# Create your tests here.

class EpisodeTest(TestCase):
    """Tests my episode model"""
    def setUp(self):
        """Defines an episode example"""
        self.episode = Episode.objects.create(
                title = "My first episode",
                description = "Python intro",
                pub_date = timezone.now(),
                link = "https://episodes.com",
                image = "https://images",
                podcast_name = "My podcast",
                guid = "de194720-7b4c-49e2-a05f-432436d3fetr"
                )

    def test_episode_content(self):
        """Tests the set up above"""
        self.assertEqual(self.episode.title, "My first episode")
        self.assertEqual(self.episode.description, "Python intro")
        self.assertEqual(self.episode.link, "https://episodes.com")

    def test_string_rep(self):
        """Tests model's string representation"""
        self.assertEqual(str(self.episode), "My podcast: My first episode")

    def test_home_page_status_code(self):
        """Tests that the app retrieves homepage successfully"""
        response = self.client.get('/epysodes/home/')
        self.assertEqual(response.status_code, 200)

    def test_podcast_status_code(self):
        """Tests that app retrieves podcast page successfully"""
        response = self.client.get('/epysodes/podcasts/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        """Tests tha correct template for home page is rendered"""
        response = self.client.get(reverse('episodes:index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_podcast_page_uses_correct_template(self):
        """Tests that correct template for podcast page is rendered"""
        response = self.client.get(reverse('episodes:podcasts'))
        self.assertTemplateUsed(response, "episodes.html")

    def test_podcasts_page_list_content(self):
        """Tests that podcasts page displayed retrieved data"""
        response = self.client.get(reverse('episodes:podcasts'))
        self.assertContains(response, 'My first episode')
