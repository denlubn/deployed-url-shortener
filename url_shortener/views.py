import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from url_shortener.models import URL
from url_shortener.serializers import URLSerializer, URLDetailSerializer


class IndexView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "url_shortener/index.html"

    def get(self, request):
        return Response()


class UrlViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "url_shortener/url_list.html"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def get_template_names(self):
        if self.action in ["list", "create"]:
            template_name = self.template_name
        else:
            template_name = "url_shortener/url_detail.html"
        return [template_name]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = URLSerializer()
        return Response({'url_list': queryset, 'serializer': serializer})

    def create(self, request, *args, **kwargs):
        serializer = URLSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        short_url = "localhost:8000/" + str(uuid.uuid4())[:5]
        serializer.save(short_url=short_url, user=request.user)
        return redirect('url_shortener:url-list')

    def retrieve(self, request, *args, **kwargs):
        url = self.get_object()
        serializer = URLDetailSerializer(url)
        return Response({'serializer': serializer, 'url': url})

    def partial_update(self, request, *args, **kwargs):
        url = self.get_object()
        serializer = URLDetailSerializer(url, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('url_shortener:url-detail', pk=url.pk)

    def destroy(self, request, *args, **kwargs):
        url = self.get_object()
        url.delete()
        return redirect('url_shortener:url-list')


class RedirectView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def redirect(request, slug):
        url = URL.objects.get(short_url=f"localhost:8000/{slug}")
        url.num_visits += 1
        url.save()
        return HttpResponseRedirect(redirect_to=url.original_link)

    def get(self, request, slug):
        return self.redirect(request, slug)
