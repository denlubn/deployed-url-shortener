from django.urls import path

from url_shortener.views import RedirectView, UrlViewSet, IndexView

url_list = UrlViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

url_detail = UrlViewSet.as_view({
    'get': 'retrieve',
    'post': 'partial_update',
})

url_delete = UrlViewSet.as_view({
    'post': 'destroy',
})

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("urls/", url_list, name="url-list"),
    path("urls/<int:pk>/", url_detail, name="url-detail"),
    path("urls/<int:pk>/delete/", url_delete, name="url-delete"),
    path("<str:slug>/", RedirectView.as_view(), name="redirect"),
]

app_name = "url_shortener"
