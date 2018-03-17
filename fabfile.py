from fabric.api import run, sudo, env, cd

env.use_ssh_config = True
env.hosts = ['dreamcast.neuf.no']
env.project_path = '/var/www/neuf.no/infoskjerm2'
env.user = 'gitdeploy'


def deploy():
    with cd(env.project_path):
        run('git pull')  # Get source
        run('pipenv install')  # install deps in virtualenv
        run('umask 022; pipenv run python manage.py collectstatic --noinput')  # Collect static
        run('pipenv run python manage.py migrate')  # Run DB migrations

    # Reload
    sudo('/usr/bin/supervisorctl pid infoskjerm.neuf.no | xargs kill -HUP', shell=False)
