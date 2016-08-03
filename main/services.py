"""Basic os services."""

import os
import sys


def shutdown_service(service: str):
    """Desliga um serviço."""
    os.system('sudo service {} stop'.format(service))


def shutdown_local_services():
    """Desliga serviços de desenvolvimento comuns nesta máquina."""
    for service in 'postgresql nginx redis-server rabbitmq-server mongod'.split():
        shutdown_service(service)

    os.system('dropbox stop')


def start_service(service: str):
    """Inicia um serviço."""
    os.system('sudo service {} start'.format(service))


def start_services():
    """Inicia serviços passados como argumentos na linha de comando."""
    for service in sys.argv[1:]:
        start_service(service)
