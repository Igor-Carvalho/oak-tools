#!/usr/bin/env python3.5
"""setup configuration."""

from setuptools import find_packages, setup

setup(
    name='oak-tools',
    version='0.0.11',
    description='My Simple Tools',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
    ],
    entry_points={
        'console_scripts': [
            'desligar-serviços=main.services:shutdown_local_services',
            'iniciar-serviços=main.services:start_services',
            'download=main.downloader:main',
            'new_project=main.new_project:main',
        ]
    }
)
