"""Basic os services."""

from os import system


def shutdown_service(service: str):
    """Desliga um serviço."""
    system('sudo service {} stop'.format(service))


def shutdown_local_services():
    """Desliga serviços de desenvolvimento comuns nesta máquina."""
    for service in 'postgresql nginx redis-server rabbitmq-server'.split():
        shutdown_service(service)
