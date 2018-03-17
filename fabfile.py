from contextlib import contextmanager as _contextmanager
from fabric.api import run, sudo, env, cd, prefix
from fabric.context_managers import shell_env

env.use_ssh_config = True
env.hosts = ['dreamcast.neuf.no']
env.project_path = '/var/www/neuf.no/infoskjerm2'
env.user = 'gitdeploy'
env.activate = 'source {}/.venv/bin/activate'.format(env.project_path)


@_contextmanager
def virtualenv():
    with cd(env.project_path), prefix(env.activate):
        yield


def deploy():
    with shell_env(PIPENV_VENV_IN_PROJECT='yup'), virtualenv():
        run('git pull')  # Get source
        run('pipenv install')  # install deps in virtualenv
        run('umask 022; python manage.py collectstatic --noinput')  # Collect static
        run('python manage.py migrate')  # Run DB migrations

    # Reload
    sudo('/usr/bin/supervisorctl pid infoskjerm.neuf.no | xargs kill -HUP', shell=False)
