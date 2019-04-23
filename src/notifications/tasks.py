from django.conf import settings
from celery.decorators import task
from celery.utils.log import get_task_logger
from frontend.models import Flow
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from json2html import *
from .models import Notification

logger = get_task_logger(__name__)

def send_email(to, name, subject, body):
    sender = settings.DEFAULT_FROM_EMAIL

    context = {'base_url': settings.BASE_URL,
               'name': name,
               'body': body}
    html_content = render_to_string(str(settings.APPS_DIR.path('notifications', 'templates', 'email.html')), context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, sender, to=[to])
    msg.get_connection(fail_silently=True)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@task(name='send_flow_triggered')
def send_flow_triggered(flow_id):
    logger.info('Sending a triggered email for flow' + str(flow_id))
    flow = Flow.objects.get(openroad_uuid=flow_id)
    flow_definition = flow.flow_definition

    body = '<p>We just saw you triggered a flow on your design: ' + flow.design.name + '. Awesome!</p>'
    body += '<p>Now, we are looking for a runner server to take care of your design. We will send '
    body += 'emails to keep you updated with the progress of your submitted flow.</p><br>'
    body += '<strong>Below are the job details we received:</strong><br><br><br>'

    body += '<u>Design Files:</u>'
    body += '<ul>'
    for design_file in flow_definition['design_files']:
        body += '<li>' + design_file + '</li>'
    body += '</ul><br>'

    body += '<u>Library:</u> ' + flow_definition['library'] + '<br><br>'

    body += '<u>Stages:</u>'
    body += '<ul>'
    for stage in flow_definition['flow']:
        body += '<li>' + stage + '</li><br>'
        body += json2html.convert(json=flow_definition['stages'][stage])
    body += '</ul><br><br>'

    # add to notifications table
    notification = Notification(message=flow.design.name + ' flow triggered',
                                icon=Notification.FLAG,
                                click_view='frontend:design-flows',
                                click_parameter=flow.design.id,
                                user=flow.design.user)
    notification.save()

    # send email
    send_email(flow.design.user.email, 'OpenROAD User', 'OpenROAD | Flow Run Requested', body)

@task(name='send_flow_started')
def send_flow_started(flow_id, storage_url):
    logger.info('Sending a started email for flow' + str(flow_id))
    flow = Flow.objects.get(openroad_uuid=flow_id)

    body = '<p>Yo! We secured a runner server for your design. Your flow just started. <br>'
    body += "Your output files will be available at <a href='" + storage_url + "'>this link</a>. <br><br>"
    body += 'Want some coffee?</p><br>'

    # add to notifications table
    notification = Notification(message=flow.design.name + ' flow started',
                                icon=Notification.PLAY,
                                click_view='frontend:design-flows',
                                click_parameter=flow.design.id,
                                user=flow.design.user)
    notification.save()

    # send email
    send_email(flow.design.user.email, 'OpenROAD User', 'OpenROAD | Flow Started', body)

@task(name='send_flow_completed')
def send_flow_completed(flow_id):
    logger.info('Sending a completed email for flow' + str(flow_id))
    flow = Flow.objects.get(openroad_uuid=flow_id)

    body = '<p>Great news! <br>Your design has walked through all our flow steps with no problem. Yaay!. <br>'
    body += "Find your output files at <a href='" + flow.output_files_url + "'>this link</a>. <br><br>"
    body += 'How do you like this experience?</p><br>'

    # add to notifications table
    notification = Notification(message=flow.design.name + ' flow completed',
                                icon=Notification.CHECK,
                                click_view='frontend:design-flows',
                                click_parameter=flow.design.id,
                                user=flow.design.user)
    notification.save()

    # send email
    send_email(flow.design.user.email, 'OpenROAD User', 'OpenROAD | Flow Completed', body)

@task(name='send_flow_failed')
def send_flow_failed(flow_id):
    logger.info('Sending a failed email for flow' + str(flow_id))
    flow = Flow.objects.get(openroad_uuid=flow_id)

    body = '<p>Ops! Looks like something went wrong with your design. <br>'
    body += "Please, check the log files at <a href='" + flow.output_files_url + "'>this link</a>, "
    body += 'and don\'t hesitate to trigger the flow again when you figure out the problem.</p><br><br>'
    body += 'Need help? Reach out to our support :)'

    # add to notifications table
    notification = Notification(message=flow.design.name + ' flow error',
                                icon=Notification.TIMES,
                                click_view='frontend:design-flows',
                                click_parameter=flow.design.id,
                                user=flow.design.user)
    notification.save()

    # send email
    send_email(flow.design.user.email, 'OpenROAD User', 'OpenROAD | Flow Failed', body)