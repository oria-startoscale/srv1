"""
This file is ONLY utilized by pycharm in pytest configuration. DO NOT rename it or remove it!
It was created to allow good workflow in pycharm against docker containers as described here:
https://stratoscale.atlassian.net/wiki/display/BK/Fluent+skipper-pycharm+workflow
"""
import os
import logging
import subprocess

import pytest
import re

from docker_test_tools import config, environment

config = config.Config(config_path=os.environ.get('CONFIG', None))
controller = environment.EnvironmentController(log_path=config.log_path,
                                               project_name=config.project_name,
                                               compose_path=config.docker_compose_path,
                                               reuse_containers=config.reuse_containers)


@pytest.fixture(scope="session", autouse=True)
def global_setup_teardown():
    """
    This function will be executed once per testing session: before & after.
    It is a replacement for the layers plugin in nose2 and is needed because pycharm
    does not provide nose2 integration
    """
    controller.setup()
    # In pycharm execution, skipper hasn't set the network for us
    try:
        connect_to_containers_network()
    except subprocess.CalledProcessError:
        # This might fail because when executed using skipper, it is already connected to the relevant network
        logging.warning("Connecting build container to testing network failed,"
                        "probably because it is already connected.")
    yield
    controller.teardown()


def connect_to_containers_network():
    """Connect current container to the environment containers network."""
    logging.info("Connecting to the environment network")
    container_id = get_current_container_id()
    subprocess.check_output(
        'docker network connect subsystem_tests-network {container_id}'.format(container_id=container_id),
        shell=True)


def get_current_container_id():
    """Return the current container ID."""
    with open('/proc/self/cgroup', 'rt') as cgroup_file:
        for line in cgroup_file.readlines():
            return re.sub(r'^docker-', '', re.sub(r'\.scope$', '', re.sub(r'^.*\/', '', line.strip())))
