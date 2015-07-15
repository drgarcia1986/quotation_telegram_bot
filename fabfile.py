# -*- coding: utf-8 -*-
import os

from fabric.api import env, sudo


PROJECT_USER = 'cotacao_bot'
PROJECT_ROOT = '/home/{}/project/'.format(PROJECT_USER)
VIRTUALENV_ROOT = '{}/venv/'.format(PROJECT_ROOT)
PYTHON_PATH = '{}/bin/python'.format(VIRTUALENV_ROOT)
PIP_PATH = '{}/bin/pip'.format(VIRTUALENV_ROOT)
REQUIREMENTS_PATH = '{}/requirements.txt'.format(PROJECT_ROOT)

CMD_CHANGE_UNIX_USER_TO_PROJECT_USER = 'su -l {}'.format(PROJECT_USER)
CMD_GO_TO_PROJECT_ROOT = 'cd {}'.format(PROJECT_ROOT)
CMD_GIT_PULL = 'git pull --rebase origin master'

SUPERVISOR = 'supervisorctl'

env.environment_name = 'production'
env.user = 'root'
env.hosts = [os.environ.get('HOST_IP')]
env.key_filename = os.environ.get('HOST_SSH_KEY')


def update_source():
    command = '{change_user} -c "{go_to_project_root} && {git_pull}"'.format(
        change_user=CMD_CHANGE_UNIX_USER_TO_PROJECT_USER,
        go_to_project_root=CMD_GO_TO_PROJECT_ROOT,
        git_pull=CMD_GIT_PULL
    )
    sudo(command)


def update_dependecies():
    command = (
        '{change_user} -c "{pip_path} install -r {requirements_path}"'.format(
            change_user=CMD_CHANGE_UNIX_USER_TO_PROJECT_USER,
            pip_path=PIP_PATH,
            requirements_path=REQUIREMENTS_PATH
        )
    )
    sudo(command)


def restart_services():
    cmds = ('reread', 'update', 'restart all')
    for cmd in cmds:
        sudo('{} {}'.format(SUPERVISOR, cmd))


def deploy():
    update_source()
    update_dependecies()
    restart_services()
