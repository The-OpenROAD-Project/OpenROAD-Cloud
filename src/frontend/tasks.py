import requests
import os
import shutil
import yaml
from django.conf import settings
from celery.decorators import task
from celery.utils.log import get_task_logger
from git import Repo
from frontend.models import Flow
from notifications.tasks import send_flow_triggered

logger = get_task_logger(__name__)


def get_flow_definition(repo_dir):
    flow_definition_file = os.path.join(repo_dir, 'openroad-flow.yml')
    with open(flow_definition_file, 'r') as f:
        flow_definition = yaml.load(f)
    return flow_definition


@task(name='retrieve_commit_info')
def retrieve_commit_info(flow_id):
    logger.info('Retrieving commit info for flow ' + str(flow_id))
    flow = Flow.objects.get(pk=flow_id)
    repo_dir = os.path.join(settings.VALIDATION_TMP_DIR, str(flow_id), flow.design.repo_url)

    repo = Repo.clone_from(flow.design.repo_url, repo_dir)
    heads = repo.heads
    master = heads.master
    commit = master.commit
    flow_definition = get_flow_definition(repo_dir)
    flow.commit_id = commit
    flow.commit_message = commit.message.strip()
    flow.flow_definition = flow_definition
    flow.save()

    # clean
    shutil.rmtree(os.path.join(settings.VALIDATION_TMP_DIR, str(flow_id)), ignore_errors=False)

    # notify user
    send_flow_triggered.delay(flow.openroad_uuid)


@task(name='send_task_to_runner')
def send_task_to_runner(flow_id, repo_url):
    r = requests.post(settings.RUNNER_URL + '/start',
                      data={'flow_uuid': flow_id,
                            'flow_repo_url': repo_url})
    logger.info('Notified Runner to start flow ' + flow_id)
    logger.info('Runner responded ' + r.text)
