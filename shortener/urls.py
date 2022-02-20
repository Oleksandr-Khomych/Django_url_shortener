from django.urls.conf import path
from shortener.views import RedirectHandler, ListCreateShortUrl, RetrieveUpdateDestroyShortUrl


urlpatterns = [
    path('api/short_url/', ListCreateShortUrl.as_view(), name='list_create_short_url'),
    path('api/short_url/<int:pk>/', RetrieveUpdateDestroyShortUrl.as_view(), name='retrieve_update_destroy_short_url'),
    path('<str:url_hash>/', RedirectHandler.as_view(), name='redirect'),
]
