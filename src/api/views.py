from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from . import helpers
from notifications import helpers as notifications
import json

class GitHubFlowTrigger(APIView):
    """
    1. Receives a webhook from GitHub to run the flow
    2. Clone the repo
    3. Submit flow for processing
    """
    def post(self, request, format=None):
        github_payload = JSONParser().parse(request)
        flow_job = helpers.process_github_payload(github_payload)
        flow_job = helpers.clone_repo(flow_job)
        flow_job = helpers.get_job_definition(flow_job)
        notifications.notify_job_created(flow_job)
        return Response(flow_job, status=status.HTTP_201_CREATED)
