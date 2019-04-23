from django.urls import path
from . import views

urlpatterns = [
    path('github/design', views.GitHubFlowTrigger.as_view(), name='index'),
]
