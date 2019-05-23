from django.utils import timezone
from celery.decorators import task
from celery.utils.log import get_task_logger
from frontend.models import Flow
from notifications.tasks import send_flow_started, send_flow_completed, send_flow_failed


logger = get_task_logger(__name__)

@task(name='flow_started_task')
def flow_started_task(flow_uuid, storage_url, live_monitoring_url):
    flow = Flow.objects.get(openroad_uuid=flow_uuid)
    if flow:
        flow.status = Flow.STARTED
        flow.started_on = timezone.now()
        flow.output_files_url = storage_url
        flow.live_monitoring_url = live_monitoring_url
        flow.save()
        logger.info('Flow ' + str(flow) + ' started ..')
        send_flow_started.delay(flow_uuid, storage_url)

    return True

@task(name='flow_completed_task')
def flow_completed_task(flow_uuid, storage_url=None):
    flow = Flow.objects.get(openroad_uuid=flow_uuid)
    if flow:
        flow.status = Flow.COMPLETED
        flow.ended_on = timezone.now()
        if storage_url:
            flow.output_files_url = storage_url
        flow.save()
        logger.info('Flow ' + str(flow) + ' completed ..')
        send_flow_completed.delay(flow_uuid)

    return True

@task(name='flow_failed_task')
def flow_failed_task(flow_uuid, storage_url=None):
    flow = Flow.objects.get(openroad_uuid=flow_uuid)
    if flow:
        flow.status = Flow.FAILED
        flow.ended_on = timezone.now()
        if storage_url:
            flow.output_files_url = storage_url
        flow.save()
        logger.info('Flow ' + str(flow)+ ' failed ..')
        send_flow_failed.delay(flow_uuid)

    return True