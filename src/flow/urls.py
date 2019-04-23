from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include(('frontend.urls', 'frontend'), namespace='frontend')),
    path('runner-listener/', include(('runner_listener.urls', 'runner-lister'), namespace='runner-lister')),
    path('admin/', admin.site.urls),
]
