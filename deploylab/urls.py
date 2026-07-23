from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from notes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.note_list, name="note_list"),
    path("new/", views.note_create, name="note_create"),
    path("<int:pk>/delete/", views.note_delete, name="note_delete"),
]

# Only serve media files this way during local development.
# In production, WhiteNoise/your host handles this differently.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
