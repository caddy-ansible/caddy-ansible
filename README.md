# Caddy Ansible Role

<!-- toc -->

- [Dependencies](#dependencies)
- [Role Variables](#role-variables)
  * [The Caddyfile](#the-caddyfile)
  * [Whether to template the Caddyfile on each run](#whether-to-template-the-caddyfile-on-each-run)
  * [The OS to download caddy for](#the-os-to-download-caddy-for)
  * [The version of Caddy to use](#the-version-of-caddy-to-use)
  * [Auto update Caddy?](#auto-update-caddy)
  * [Additional Available Packages](#additional-available-packages)
  * [Use `setcap`?](#use-setcap)
  * [Use systemd capabilities controls](#use-systemd-capabilities-controls)
  * [Add additional environment variables or files](#add-additional-environment-variables-or-files)
  * [Use additional CLI arguments](#use-additional-cli-arguments)
  * [Use a GitHub OAuth token to request the list of caddy releases](#use-a-github-oauth-token-to-request-the-list-of-caddy-releases)
- [Example Playbooks](#example-playbooks)
- [Developing](#developing)
- [Debugging](#debugging)
- [Contributing](#contributing)

<!-- tocstop -->

This role installs and configures the caddy web server. The user can specify any http configuration parameters they wish to apply their site. Any number of sites can be added with configurations of your choice.

## Dependencies

`jmespath`, which must be manually installed on the Ansible controller. See [Selecting JSON data: JSON queries](https://docs.ansible.com/ansible/latest/collections/community/general/docsite/filter_guide_selecting_json_data.html) for more details.

## Role Variables

### The Caddyfile

See [Caddyfile docs](https://caddyserver.com/docs/caddyfile). Notice the `|` used to include a multi-line string. You may set `caddy_conf_filename` to `config.json` to use json format.

default:

```yaml
caddy_conf_filename: Caddyfile
caddy_config: |
  http://localhost:2020
  respond "Hello, world!"
```

If you wish to use a template for the config you can do this:

```yaml
caddy_config: "{{ lookup('template', 'templates/Caddyfile.j2') }}"
```

### Whether to template the Caddyfile on each run

By default the Caddyfile is templated on each run. By setting this variable you can ensure the file is created on the first run but never updated after.

```yaml
caddy_config_update: true
```

### The OS to download caddy for

default:

```yaml
caddy_os: linux
```

### The version of Caddy to use

default:

```yaml
caddy_version: ''
```

This option cannot be used together with `caddy_packages` because that option prevents the downloads from using Github, meaning no older versions are available.

The version of Caddy will only be changed after the first run of the role if `caddy_update` is set to `true`, otherwise the version of Caddy will remain as the one selected on first run of the role.

### Auto update Caddy?

default:

```yaml
caddy_update: true
```

### Additional Available Packages

Changing this variable will reinstall Caddy with the new packages if `caddy_update` is enabled. Check https://caddyserver.com/download for available packages.

This causes the builds to be downloaded from https://caddyserver.com rather than using the github releases. This service is provided for free by the Caddy maintainers and if you rely on it you should consider donating. The capacity of this service is limited so if you use this role to manage Caddy across many hosts it is recommended to use a different method.

default:

```yaml
caddy_packages: []
```

### Use `setcap`?

This allows Caddy to open a low port (under 1024 - e.g. 80, 443).

default:

```yaml
caddy_setcap: true
```

### Use systemd capabilities controls

Set this to `false` if you need to use this on a version of systemd without support for
the `CapabilityBoundingSet`, `AmbientCapabilities` and `NoNewPrivileges` options, otherwise
it should generally be fine to leave as default.

default:

```yaml
caddy_systemd_capabilities_enabled: true
caddy_systemd_capabilities: "CAP_NET_BIND_SERVICE"
```

### Add additional environment variables or files

Add [environment variables](https://www.freedesktop.org/software/systemd/man/systemd.exec.html#Environment=) to the systemd script.

default:

```yaml
caddy_environment_variables: {}
```

Example usage:

```yaml
caddy_environment_variables:
  FOO: bar
  SECONDVAR: spam
```

Add [environment files](https://www.freedesktop.org/software/systemd/man/systemd.exec.html#EnvironmentFile=) to the systemd script.

default:

```yaml
caddy_environment_files: []
```

Example usage:

```yaml
caddy_environment_files:
  - /etc/default/caddy_additional_env_file
```

### Use additional CLI arguments

default:

```yaml
caddy_additional_args: ""
```

Example for LetsEncrypt staging:

```yaml
caddy_additional_args: "-ca https://acme-staging.api.letsencrypt.org/directory"
```

### Use a GitHub OAuth token to request the list of caddy releases

This role uses the GitHub releases list to check when a new version is available. [GitHub has some fairly agressive rate-limiting](https://developer.github.com/v3/#rate-limiting) which can cause failures. You can set your GitHub token to increase the limits for yourself when running the role (e.g. if deploying many servers behind a NAT or running this role repeatedly as part of a CI process).

default:

```yaml
caddy_github_token: ""
```

## Example Playbooks

```yaml
---
- hosts: all
  become: yes
  roles:
    - role: caddy_ansible.caddy_ansible
      caddy_config: |
        files.example.com
        encode gzip
        file_server browse {
            root /home/caddy/
        }
```

Example with DigitalOcean DNS for TLS:

```yaml
---
- hosts: all
  roles:
    - role: caddy_ansible.caddy_ansible
      caddy_environment_variables:
        DO_AUTH_TOKEN: "your-token-here"
      caddy_systemd_capabilities_enabled: true
      caddy_systemd_network_dependency: false
      caddy_packages: ["github.com/caddy-dns/lego-deprecated"]
      caddy_config: |
        nextcloud.example.com {
            log

            reverse_proxy http://localhost:8080 {
                header_up Host {http.request.host}
                header_up X-Real-IP {http.request.remote.host}
                header_up X-Forwarded-For {http.request.remote.host}
                header_up X-Forwarded-Port {http.request.port}
                header_up X-Forwarded-Proto {http.request.scheme}
            }

            tls webmaster@example.com {
                dns lego_deprecated digitalocean
            }
        }
```

## Developing

It is recommended to create a virtualenv for development and then install all requirements for tests:

```bash
python3 -m pip install -U requirements.txt
python3 -m pip install -U ansible ansible-lint yamllint molecule-plugins[docker,lint] pytest pytest-testinfra
```

After doing so you can run the molecule tests with:

```bash
PY_COLORS=1 ANSIBLE_FORCE_COLOR=1 MOLECULE_DISTRO=ubuntu2004 molecule test
```

Or run the alternate playbook for testing when a specific version is requested:

```bash
PY_COLORS=1 ANSIBLE_FORCE_COLOR=1 MOLECULE_DISTRO=ubuntu2004 MOLECULE_PLAYBOOK=converge-version.yml molecule test
```

## Debugging

If the service fails to start you can figure out why by looking at the output of Caddy.

```bash
systemctl status caddy -l
```

If something doesn't seem right, open an issue!

## Contributing

Pull requests are welcome. Please test your changes beforehand with vagrant:

```bash
vagrant up
vagrant provision   # (since it already provisioned there should be no changes here)
vagrant destroy
```
