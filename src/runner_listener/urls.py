from django.urls import path
from . import views

urlpatterns = [
    path('start', views.FlowStarted.as_view(), name='started'),
    path('success', views.FlowCompleted.as_view(), name='success'),
    path('fail', views.FlowFailed.as_view(), name='fail'),
]
