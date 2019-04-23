import os
from json2html import *

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def construct_job_created_body(flow_job):
    """
    Extract flow definition and forms the body of the email
    """
    name = flow_job['user_name']
    body = '<p>We just saw you made a new push to your design repo. Awesome!</p>'
    body += '<p>Now, your design is being run through our automated flow, and you will receive '
    body += 'emails to keep you updated with the progress of your submitted design.</p><br>'
    body += '<strong>Below are the job details we received:</strong><br><br><br>'
    
    body += '<u>Design Files:</u>'
    body += '<ul>'
    for design_file in flow_job['job_definition']['design_files']:
        body += '<li>' + design_file + '</li>'
    body += '</ul><br>'
    
    body += '<u>Library:</u> ' + flow_job['job_definition']['library'] + '<br><br>'
    
    body += '<u>Stages:</u>'
    body += '<ul>'
    for stage in flow_job['job_definition']['flow']:
        body += '<li>' + stage + '</li><br>'
        body += json2html.convert(json = flow_job['job_definition']['stages'][stage])
    body += '</ul><br><br>'
    
    return name, body
