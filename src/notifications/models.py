from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Notification(models.Model):
    message = models.CharField('Notification message', max_length=100)

    FLAG = 'flag-o'
    PLAY = 'play'
    CHECK = 'check'
    TIMES = 'times'
    PLUS = 'plus-circle'
    icons = ((FLAG, FLAG),
             (PLAY, PLAY),
             (CHECK, CHECK),
             (TIMES, TIMES),
             (PLUS, PLUS))
    icon = models.CharField('Fontawesome Icon', choices=icons, max_length=20)
    click_view = models.CharField('View', max_length=100)
    click_parameter = models.CharField('View Parameter', max_length=10, default='', blank=True)
    read = models.BooleanField('Read', default=True)
    timestamp = models.DateTimeField('Posted On', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'