[![Build Status](https://travis-ci.org/caddy-ansible/caddy-ansible.svg?branch=master)](https://travis-ci.org/caddy-ansible/caddy-ansible)
[![Galaxy Role](https://img.shields.io/badge/ansible--galaxy-caddy-blue.svg)](https://galaxy.ansible.com/caddy_ansible/caddy_ansible/)

# Caddy Ansible Role

<!-- toc -->

- [Dependencies](#dependencies)
- [Role Variables](#role-variables)
  * [The Caddyfile](#the-caddyfile)
  * [The OS to download caddy for](#the-os-to-download-caddy-for)
  * [The type of license to use](#the-type-of-license-to-use)
  * [Auto update Caddy?](#auto-update-caddy)
  * [Additional Available Features](#additional-available-features)
  * [Use `setcap`?](#use-setcap)
  * [Verify the PGP signature on download?](#verify-the-pgp-signature-on-download)
  * [Use systemd capabilities controls](#use-systemd-capabilities-controls)
  * [Add additional environment variables](#add-additional-environment-variables)
  * [Use additional CLI arguments](#use-additional-cli-arguments)
  * [Use a GitHub OAuth token to request the list of caddy releases](#use-a-github-oauth-token-to-request-the-list-of-caddy-releases)
- [Example Playbooks](#example-playbooks)
- [Debugging](#debugging)
- [Contributing](#contributing)

<!-- tocstop -->

This role installs and configures the caddy web server. The user can specify any http configuration parameters they wish to apply their site. Any number of sites can be added with configurations of your choice.

## Dependencies

None

## Role Variables

### The Caddyfile

See [Caddyfile docs](https://caddyserver.com/docs/caddyfile). Notice the `|` used to include a multi-line string.

default:

```yaml
caddy_config: |
  http://localhost:2020
  respond "Hello, world!"
```

If you wish to use a template for the config you can do this:

```yaml
caddy_config: "{{ lookup('template', 'templates/Caddyfile.j2') }}"
```

### The OS to download caddy for

default:

```yaml
caddy_os: linux
```

### The type of license to use

default:

```yaml
caddy_license: personal
```

If you set the license type to `commercial` then you should also specify (replacing the dummy values with your real ones):

```yaml
caddy_license_account_id: YOUR_ACCOUNT_ID
caddy_license_api_key: YOUR_API_KEY
```

### Auto update Caddy?

default:

```yaml
caddy_update: true
```

### Additional Available Packages

Changing this variable will reinstall Caddy with the new packages if `caddy_update` is enabled. Check https://caddyserver.com/download for available packages.

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

### Verify the PGP signature on download?

default:

```yaml
caddy_pgp_verify_signatures: false
```

### Use systemd capabilities controls

default:

```yaml
caddy_systemd_capabilities_enabled: false
caddy_systemd_capabilities: "CAP_NET_BIND_SERVICE"
```

NOTE: This feature requires systemd v229 or newer and might be needed in addition to `caddy_setcap: yes`.

Supported:

* Debian 9 (stretch)
* Fedora 25
* Ubuntu 16.04 (xenial)

RHEL/CentOS has no release that supports systemd capability controls at this time.

### Add additional environment variables

Add environment variables to the systemd script.

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
  roles:
    - role: caddy-ansible
      caddy_config: |
        localhost:2020
        gzip

        tls email@example.com

        root /var/www
        git github.com/antoiner77/caddy-ansible
```

Example with Cloudflare DNS for TLS:

```yaml
---
- hosts: all
  roles:
    - role: caddy-ansible
      caddy_features: tls.dns.cloudflare
      caddy_environment_variables:
        CLOUDFLARE_EMAIL: your@email.com
        CLOUDFLARE_API_KEY: 1234567890
      caddy_config: |
        yourcloudflareddomain.com {
            tls {
                dns cloudflare
            }

            gzip

            root /var/www
            git github.com/antoiner77/caddy-ansible
        }
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
