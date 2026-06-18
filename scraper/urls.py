from django.urls import path
from .views import scrape_api, scrape_view

urlpatterns = [
    path('', scrape_view, name='scrape'),
    path("api/scrape/", scrape_api, name="scrape_api"),
]


# from django.urls import path
# from .views import scrape_view

# urlpatterns = [
#     path('', scrape_view, name='scrape'),
# ]