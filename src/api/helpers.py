import os
import yaml
from django.conf import settings
from git import Repo


def process_github_payload(payload):
    """
    processes a GitHub payload to extract important information 
    for running the flow
    return: dictionary of only attributes we care about
    """
    flow_job = {}
    flow_job['user_name'] = payload['repository']['owner']['name']
    flow_job['repo_name'] = payload['repository']['name']
    flow_job['commit_id'] = payload['head_commit']['id']
    flow_job['commit_time'] = payload['head_commit']['timestamp']

    flow_job['repo_url'] = payload['repository']['clone_url']
    
    return flow_job


def clone_repo(flow_job):
    """
    takes a flow job and clones the repo into:
    DESIGNS_DIR/<user_name>/<repo_name>/<commit_id>
    return: flow job with the absolute path of the job on the filesystem
    """
    job_dir = os.path.join(settings.DESIGNS_DIR, flow_job['user_name'], flow_job['repo_name'], flow_job['commit_id'])
    if not os.path.exists(job_dir):
        Repo.clone_from(flow_job['repo_url'], job_dir)
    flow_job['job_dir'] = job_dir
    return flow_job


def get_job_definition(flow_job):
    """
    takes the cloned repo directory and extracts job definition from the yaml file
    """
    job_definition_file = os.path.join(flow_job['job_dir'], 'openroad-flow.yml')
    with open(job_definition_file, 'r') as f:
        job_definition = yaml.load(f)
    flow_job['job_definition'] = job_definition
    return flow_job
