import os

from testinfra.utils.ansible_runner import AnsibleRunner

inventory = os.environ['MOLECULE_INVENTORY_FILE']
testinfra_hosts = AnsibleRunner(inventory).get_hosts('all')


def test_files(host):
    dirs = [
        "/etc/caddy",
        "/var/log/caddy"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.exists
        assert d.is_directory


def test_packages(host):
    pkgs = []
    for p in pkgs:
        assert host.package(p).is_installed


def test_service(host):
    s = host.service("caddy")
    assert s.is_enabled
    assert s.is_running


def test_socket(host):
    sockets = [
        "tcp://127.0.0.1:2020"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
