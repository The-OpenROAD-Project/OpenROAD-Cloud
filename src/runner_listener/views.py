from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from runner_listener.tasks import flow_started_task, flow_completed_task, flow_failed_task


class FlowStarted(APIView):
    def post(self, request):
        flow_uuid = request.POST.get('flow_uuid', None)
        storage_url = request.POST.get('storage_url', None)
        live_monitoring_url = request.POST.get('live_monitoring_url', None)

        if not flow_uuid or not storage_url or not live_monitoring_url:
            return Response('Missing parameters', status=status.HTTP_400_BAD_REQUEST)

        flow_started_task.delay(flow_uuid, storage_url, live_monitoring_url)
        return Response('Received', status=status.HTTP_202_ACCEPTED)


class FlowCompleted(APIView):
    def post(self, request):
        flow_uuid = request.POST.get('flow_uuid', None)

        if not flow_uuid:
            return Response('Missing parameters', status=status.HTTP_400_BAD_REQUEST)

        flow_completed_task.delay(flow_uuid)
        return Response('Received', status=status.HTTP_202_ACCEPTED)


class FlowFailed(APIView):
    def post(self, request):
        flow_uuid = request.POST.get('flow_uuid', None)

        if not flow_uuid:
            return Response('Missing parameters', status=status.HTTP_400_BAD_REQUEST)

        flow_failed_task.delay(flow_uuid)
        return Response('Received', status=status.HTTP_202_ACCEPTED)