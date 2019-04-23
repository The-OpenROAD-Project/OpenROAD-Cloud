from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

public_urls = [
    path('', views.public.HomeView.as_view(), name='index'),
    path('login', views.public.LoginView.as_view(), name='login'),
    path('logout', views.public.LogoutView.as_view(), name='logout'),
    path('terms-of-service', views.public.TermsOfServiceView.as_view(), name='terms-of-service'),
]

user_urls = [
    path('user/dashboard', views.user.DashboardView.as_view(), name='dashboard'),
    path('user/designs', views.user.DesignsView.as_view(), name='designs'),
    path('user/designs/<int:design_id>', views.user.DesignsView.as_view(), name='design-delete'),
    path('user/designs/<int:design_id>/flows', views.user.FlowsView.as_view(), name='design-flows'),
    path('user/designs/<int:design_id>/flow', views.user.FlowView.as_view(), name='design-flow'),
    path('user/flow/<int:flow_id>', views.user.FlowStreamView.as_view(), name='flow-stream'),
    path('user/account/profile', views.user.ProfileView.as_view(), name='profile'),
    path('user/account/github', views.user.GitHubView.as_view(), name='github'),
    path('user/account/gitlab', views.user.GitLabView.as_view(), name='gitlab'),
    path('user/settings', views.user.SettingsView.as_view(), name='settings'),
    path('user/documentation', views.user.DocumentationView.as_view(), name='documentation'),
]

urlpatterns = public_urls + user_urls
