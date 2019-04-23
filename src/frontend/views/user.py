import time
import rethinkdb as r
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, StreamingHttpResponse
from datetime import timedelta
from frontend.views.helpers import validate_repo
from frontend.tasks import retrieve_commit_info, send_task_to_runner
from frontend.models import Design, Flow
from notifications.models import Notification
from django.utils import timezone


class DashboardView(LoginRequiredMixin, View):
    template_name = 'user/dashboard.html'

    def get(self, request):

        notifications = {
            'notifications': Notification.objects.filter(user=request.user).order_by('-timestamp')[:10]
        }
        running_flows = {
            'running_flows': Flow.objects.filter(design__in=Design.objects.filter(user=request.user),
                                                 status=Flow.STARTED)
        }
        flows = Flow.objects.filter(design__in=Design.objects.filter(user=request.user),
                                    status=Flow.COMPLETED)
        computation_time = timedelta(0)
        for flow in flows:
            computation_time += flow.computation_time()

        dashboard = {
            'new_designs': Design.objects.filter(user=request.user).count(),
            'flows_completed': Flow.objects.filter(design__in=Design.objects.filter(user=request.user),
                                                   status=Flow.COMPLETED).count(),
            'compute_minutes': int(computation_time.seconds / 60),
            'minutes_saved': 'N/A'
        }
        show_intro = False
        if timezone.now() - request.user.date_joined < timedelta(minutes=2):
            show_intro = True
        context = {**dashboard, **running_flows, **notifications,
                   'show_intro': show_intro}
        return render(request, self.template_name, context=context)


class DesignsView(LoginRequiredMixin, View):
    template_name = 'user/designs.html'

    def get(self, request):
        designs = {
            'designs': Design.objects.filter(user=request.user)
        }
        context = {**designs}
        return render(request, self.template_name, context=context)

    def post(self, request):
        design_name = request.POST['design_name']
        repo_url = request.POST['repo_url']

        repo_is_valid, error = validate_repo(request.user.id, repo_url)
        if repo_is_valid:
            # create the design
            design = Design(name=design_name, repo_url=repo_url, user=request.user)
            design.save()
            designs = {
                'designs': Design.objects.filter(user=request.user)
            }
            context = {
                'imported': True,
                'message': 'Design repo imported successfully',
                **designs
            }
            return render(request, self.template_name, context=context)
        else:
            context = {
                'imported': False,
                'message': error
            }
            return render(request, self.template_name, context=context)

    def delete(self, request, design_id):
        design = Design.objects.get(user=request.user, id=design_id)
        if design:
            design.delete()
            return HttpResponse('Done', status=200)
        else:
            return HttpResponse('Error', status=404)


class FlowsView(LoginRequiredMixin, View):
    template_name = 'user/flows.html'

    def get(self, request, design_id):
        # make sure the user owns this design
        design = Design.objects.get(user=request.user, id=design_id)
        if design:
            flows = {
                'flows': Flow.objects.filter(design=design_id).order_by('-triggered_on')
            }
        else:
            flows = {
                'flows': []
            }
        context = {**flows,
                   'design': design}

        return render(request, self.template_name, context=context)


class FlowView(LoginRequiredMixin, View):
    template_name = 'user/flow.html'

    def post(self, request, design_id):
        # triggers the flow for the user
        # make sure the design is owned by this user
        design = Design.objects.get(user=request.user, id=design_id)
        if design:
            flow = Flow(design=design)
            flow.save()
            # get commit info
            retrieve_commit_info.apply_async(args=[flow.id], countdown=5)
            # send to a runner
            send_task_to_runner.apply_async(args=[flow.openroad_uuid, design.repo_url], countdown=5)

            context = {'flow': flow}
            return render(request, self.template_name, context=context)
        else:
            return render(request, self.template_name)

    def get(self, request, design_id):
        flow_id = design_id  # we use design id because it is what is used in the POST request
        flow = Flow.objects.get(pk=flow_id)
        context = {'flow': flow}
        return render(request, self.template_name, context=context)


class FlowStreamView(LoginRequiredMixin, View):
    def live_stream(self, flow_id):
        flow = Flow.objects.get(pk=flow_id)

        if flow.status == Flow.COMPLETED or flow.status == Flow.FAILED:
            yield 'Live streaming ended. Please, check the logs in the output files.'
            return

        live_stream_url = flow.live_monitoring_url
        while live_stream_url == '#':
            yield 'Live streaming is not available yet. Please, wait!'
            time.sleep(1)
            flow = Flow.objects.get(pk=flow_id)
            live_stream_url = flow.live_monitoring_url

        yield 'Live streaming is starting ..'
        conn = r.connect(flow.live_monitoring_url, password='brown340')
        # get the logs initially
        cursor = r.db('openroad').table('flow_log').\
            filter(r.row['openroad_uuid'] == str(flow.openroad_uuid)).run(conn)
        for d in cursor:
            yield d['logs']

        # then listen for changes in these logs
        cursor = r.db('openroad').table('flow_log').\
            filter(r.row['openroad_uuid'] == str(flow.openroad_uuid)).\
            changes().run(conn)
        for d in cursor:
            yield d['new_val']['logs']

    def test(self):
        for i in range(1000):
            yield i
            time.sleep(1)

    def get(self, request, flow_id):
        return StreamingHttpResponse(self.live_stream(flow_id))


class ProfileView(LoginRequiredMixin, View):
    template_name = 'user/account/profile.html'

    def get(self, request):
        return render(request, self.template_name)


class GitHubView(LoginRequiredMixin, View):
    template_name = 'user/account/github.html'

    def get(self, request):
        return render(request, self.template_name)


class GitLabView(LoginRequiredMixin, View):
    template_name = 'user/account/gitlab.html'

    def get(self, request):
        return render(request, self.template_name)


class SettingsView(LoginRequiredMixin, View):
    template_name = 'user/settings.html'

    def get(self, request):
        return render(request, self.template_name)


class DocumentationView(LoginRequiredMixin, View):
    template_name = 'user/documentation.html'

    def get(self, request):
        return render(request, self.template_name)