from fabric.api import env
from fabric.api import sudo
from fabric.api import task
from fabric.contrib.files import upload_template


def handler(service, action):
    """ Handler method for service operations. """
    cmd = 'systemctl {} {}'.format(action, service)
    return sudo(cmd, pty=False)


def nginx_handler(action):
    """ Helper method for nginx service operations. """
    return handler('nginx', action)


def gunicorn_handler(action):
    """ Helper method for gunicorn instance service operations. """
    instance = 'django-{}-{}'.format(env.prefix, env.branch)
    return handler(instance, action)


def memcached_handler(action):
    """ Helper method for memcadhed service operations. """
    return handler('memcached', action)


def add_systemd_service(filename, context):
    """ Deploys an upstart configuration task file. """
    destination = '/lib/systemd/system/django-{}-{}.service'.format(
        env.prefix, env.branch)
    upload_template(filename, destination, context=context, use_sudo=True)

    # set root as file owner
    cmd = 'chown root:root {}'.format(destination)
    sudo(cmd)


@task
def enable_systemd_service():
    # enable service
    cmd = 'systemctl enable django-{}-{}'.format(env.prefix, env.branch)
    sudo(cmd)


@task
def logs():
    """ Shows systemd django service log """
    sudo('journalctl -u django-{}-{}.service'.format(env.prefix, env.branch))
