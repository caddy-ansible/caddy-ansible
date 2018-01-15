from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_files(host):
    dirs = [
        "/etc/caddy",
        "/opt/node_exporter"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.exists
        assert d.is_directory


def test_packages(host)
    pkgs = [
        "git"
    ]
    for p in pkgs:
        assert host.package(p).is_installed


def test_service(host):
    s = host.service("caddy")
    assert s.is_enabled
    assert s.is_running


def test_socket(host):
    sockets = [
        "tcp://localhost:2020"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
