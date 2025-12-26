from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import image_upload

urlpatterns = [
    path('upload/', image_upload, name='image-upload'),  # Image upload view
]
