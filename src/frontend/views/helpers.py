import re
import os
import yaml
import shutil
from django.conf import settings
from git import Repo
from frontend.models import Flow


def validate_email_format(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_regex.match(email)


def check_password_strength(password):
    return len(password) > 6


def validate_repo(user_id, repo_url):
    """
    validate that the repo exists and contains openroad-flow.yml file
    :param repo_url: a public git URL that can be cloned
    :return: True if it is a valid design repo, False and reason if not
    """
    repo_dir = os.path.join(settings.VALIDATION_TMP_DIR, str(user_id), repo_url)

    if repo_url.startswith('https://github.com/The-OpenROAD-Project/openroad-template-design'):
        return False, 'Sorry, but you cannot import the template design to your workspace. Please, fork the repo first!'

    try:
        Repo.clone_from(repo_url, repo_dir)
    except:
        shutil.rmtree(os.path.join(settings.VALIDATION_TMP_DIR, str(user_id)), ignore_errors=False)
        return False, 'Cannot import repo. Are you sure this is a valid git repo?'

    try:
        job_definition_file = os.path.join(repo_dir, 'openroad-flow.yml')
        with open(job_definition_file, 'r') as f:
            job_definition = yaml.load(f)
        # to add more checks here later ..
    except:
        shutil.rmtree(os.path.join(settings.VALIDATION_TMP_DIR, str(user_id)), ignore_errors=False)
        return False, 'This repo doesn\'t seem to be following the OpenROAD template design repo'

    # delete folder to clean up space
    shutil.rmtree(os.path.join(settings.VALIDATION_TMP_DIR, str(user_id)), ignore_errors=False)
    return True, None
