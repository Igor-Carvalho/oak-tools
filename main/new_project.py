#!/usr/bin/env python3.5
"""Create a new django project using custom template."""

from argparse import ArgumentParser
from os import system


def main():
    """Run module."""
    parser = ArgumentParser()
    parser.add_argument('project_name')
    args = parser.parse_args()

    template_url = 'https://github.com/Igor-Carvalho/django-aws-template/archive/master.zip'
    extension = 'py,rst,txt,html,js,json'
    name = '.bowerrc'
    params = args.project_name, template_url, extension, name
    cmd = 'django-admin startproject {} --template {} --extension {} --name {}'.format(*params)
    system(cmd)

if __name__ == '__main__':
    main()
