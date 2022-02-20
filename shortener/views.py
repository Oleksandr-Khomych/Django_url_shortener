from typing import Union

from django.http import HttpResponseRedirect
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from shortener.serializers import ShortUrlSerializer
from shortener.models import ShortUrl
from shortener.permissions import IsOwnerOrSuperUser


class ListCreateShortUrl(ListCreateAPIView):
    queryset = ShortUrl.objects.all()
    serializer_class = ShortUrlSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            queryset = queryset.filter(creator=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveUpdateDestroyShortUrl(RetrieveUpdateDestroyAPIView):
    queryset = ShortUrl.objects.all()
    serializer_class = ShortUrlSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrSuperUser)


class RedirectHandler(APIView):
    def get(self, request: Request, url_hash: str) -> Union[HttpResponseRedirect, Response]:
        short_url = get_object_or_404(ShortUrl, url_hash=url_hash)
        short_url.redirect_count += 1
        short_url.save()
        return HttpResponseRedirect(redirect_to=short_url.full_url)
