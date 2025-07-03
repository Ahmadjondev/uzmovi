from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from movies.sitemaps import (
    StaticViewSitemap,
    CategorySitemap,
    VideoSitemap,
    EpisodeSitemap,
)

sitemaps_dict = {
    "static": StaticViewSitemap,
    "categories": CategorySitemap,
    "videos": VideoSitemap,
    "episodes": EpisodeSitemap,
}

urlpatterns = [
    path("manager/", admin.site.urls),
    path("", include("movies.urls")),
    path("users/", include("users.urls")),
    path("accounts/", include("allauth.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps_dict},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_txt",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
