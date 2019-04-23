import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.contrib.auth.models import User


class Design(models.Model):
    openroad_uuid = models.UUIDField('OpenROAD UUID', default=uuid.uuid4, editable=False)
    name = models.CharField('Design Name', max_length=20)
    repo_url = models.URLField('Repository URL')
    imported_on = models.DateTimeField('Imported On', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def number_of_flow_runs(self):
        flows = Flow.objects.filter(design=self).order_by('-triggered_on')
        return len(flows)

    def last_flow_run(self):
        flows = Flow.objects.filter(design=self).order_by('-triggered_on')
        if flows:
            return flows[0].triggered_on
        return None

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Design'
        verbose_name_plural = 'Designs'


class Flow(models.Model):
    openroad_uuid = models.UUIDField('OpenROAD UUID', default=uuid.uuid4)
    triggered_on = models.DateTimeField('Triggered On', default=timezone.now)
    started_on = models.DateTimeField('Started On', null=True, blank=True)
    ended_on = models.DateTimeField('Ended On', null=True, blank=True)
    commit_message = models.TextField('Commit Message', default='retrieving ..')
    commit_id = models.CharField('Commit ID', max_length=40, default='retrieving ..')
    live_monitoring_url = models.URLField('Live Monitor', default='#')
    output_files_url = models.URLField('Output Files', default='#')
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    flow_definition = JSONField('Flow Definition', default=None, null=True, blank=True)

    TRIGGERED = 'triggered'
    STARTED = 'started'
    COMPLETED = 'completed'
    FAILED = 'failed'
    flow_status = ((TRIGGERED, TRIGGERED),
                   (STARTED, STARTED),
                   (COMPLETED, COMPLETED),
                   (FAILED, FAILED))
    status = models.CharField('Status', choices=flow_status, default=TRIGGERED, max_length=10)
    status_message = models.TextField('Status Message', null=True, blank=True)

    def computation_time(self):
        if self.started_on and self.ended_on:
            return self.ended_on - self.started_on
        return 0

    def __str__(self):
        return self.design.name + ' - ' + self.commit_message

    class Meta:
        verbose_name = 'Flow'
        verbose_name_plural = 'Flows'
