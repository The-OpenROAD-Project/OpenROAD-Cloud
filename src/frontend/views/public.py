from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.db import IntegrityError
from django.contrib import auth
from django.contrib.auth.models import User
from .helpers import validate_email_format, check_password_strength
from django.db import transaction
from notifications.models import Notification


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        if not validate_email_format(email):
            context = {'signup_failed': True,
                       'message': 'Please, enter a valid email!'}
            return render(request, self.template_name, context=context)

        if not check_password_strength(password):
            context = {'signup_failed': True,
                       'message': 'Password length must be at least 6!'}
            return render(request, self.template_name, context=context)

        try:
            with transaction.atomic():
                user = User.objects.create_user(email, email, password)
                auth.login(request, user)

                notification = Notification(message='Account created',
                                            icon=Notification.PLUS,
                                            click_view='frontend:profile',
                                            user=user)
                notification.save()

                return redirect('frontend:dashboard')
        except IntegrityError as e:
            user = auth.authenticate(request, username=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('frontend:dashboard')

            context = {'signup_failed': True,
                       'message': 'Do you have an account with the same email? Login instead!'}
            return render(request, self.template_name, context=context)
        except Exception as e:
            context = {'signup_failed': True,
                       'message': 'Ops! Our server couldn\'nt create a new account. Try again later!'}
            return render(request, self.template_name, context=context)


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        redirect_to = request.GET.get('next')
        context = {'next': redirect_to}
        return render(request, self.template_name, context=context)

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        redirect_to = request.POST.get('next')
        if redirect_to is None:
            redirect_to = 'frontend:dashboard'

        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(redirect_to)

        else:
            context = {'login_failed': True}
            return render(request, self.template_name, context=context)


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('frontend:index')


class TermsOfServiceView(View):
    template_name = 'terms-of-service.html'

    def get(self, request):
        return render(request, self.template_name)

