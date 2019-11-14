[![Build Status](https://travis-ci.org/caddy-ansible/caddy-ansible.svg?branch=master)](https://travis-ci.org/caddy-ansible/caddy-ansible)
[![Galaxy Role](https://img.shields.io/badge/ansible--galaxy-caddy-blue.svg)](https://galaxy.ansible.com/caddy_ansible/caddy_ansible/)

Caddy Ansible Role
=========

This role installs and configures the caddy web server. The user can specify any http configuration parameters they wish to apply their site. Any number of sites can be added with configurations of your choice.

Dependencies
------------
None

Role Variables
--------------

**The [Caddyfile](https://caddyserver.com/docs/caddyfile)** (notice the pipe)<br>
default:
```
caddy_config: |
  localhost:2020
  gzip
  # tls email@example.com
  root /var/www
  git github.com/antoiner77/caddy-ansible
```

If you wish to use a template for the config you can do this:
```
caddy_config: "{{ lookup('template', 'templates/Caddyfile.j2') }}"
```

**The type of license to use**<br>
default:
```
caddy_license: personal
```
If you set the license type to `commercial` then you should also specify (replacing the dummy values with your real ones):
```
caddy_license_account_id: YOUR_ACCOUNT_ID
caddy_license_api_key: YOUR_API_KEY
```
**Auto update Caddy?**<br>
default:
```
caddy_update: yes
```
**Features that can be added to core:** http.authz, http.awses, http.awslambda,
http.cache, http.cgi, http.cors, http.datadog, http.expires, http.filebrowser,
http.filter, http.forwardproxy, http.git, http.gopkg, http.grpc, http.hugo,
http.ipfilter, http.jekyll, http.jwt, http.locale, http.login, http.mailout,
http.minify, http.nobots, http.prometheus, http.proxyprotocol, http.ratelimit,
http.realip, http.reauth, http.restic, http.upload, http.webdav, dns, net,
hook.service, tls.dns.azure, tls.dns.cloudflare, tls.dns.digitalocean,
tls.dns.dnsimple, tls.dns.dnspod, tls.dns.dyn, tls.dns.exoscale, tls.dns.gandi,
tls.dns.googlecloud, tls.dns.linode, tls.dns.namecheap, tls.dns.ovh,
tls.dns.rackspace, tls.dns.rfc2136, tls.dns.route53, tls.dns.vultr

Changing this variable will reinstall Caddy with the new features if `caddy_update` is enabled<br>
default:
```
caddy_features: http.git
```
**Use `setcap` for allowing Caddy to open a low port (e.g. 80, 443)?**<br>
default:
```
caddy_setcap: yes
```
**Verify the PGP signature on download?**<br>
```
caddy_pgp_verify_signatures: no
```
**Use systemd capabilities controls**<br>
default:
```
caddy_systemd_capabilities_enabled: False
caddy_systemd_capabilities: "CAP_NET_BIND_SERVICE"
```
NOTE: This feature requires systemd v229 or newer and might be needed in addition to `caddy_setcap: yes`.

Supported:
* Debian 9 (stretch)
* Fedora 25
* Ubuntu 16.04 (xenial)

RHEL/CentOS has no release that supports systemd capability controls at this time.

**Add additional environment variables**<br>

Add environment variables to the systemd script

```
caddy_environment_variables:
  FOO: bar
  SECONDVAR: spam
```

**Use additional cli arguments**<br>
default:
```
caddy_additional_args: ""
```
Example for Letsencrypt staging:
```
caddy_additional_args: "-ca https://acme-staging.api.letsencrypt.org/directory"
```


Example Playbooks
----------------
```
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

Example with Cloudflare DNS for TLS

```
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

Debugging
---------
If the service fails to start you can figure out why by looking at the output of Caddy.<br>

```console
systemctl status caddy -l
```

If something doesn't seem right, open an issue!

Contributing
------------
Pull requests are welcome. Please test your changes beforehand with vagrant:
```
vagrant up
vagrant provision (since it already provisioned there should be no changes here)
vagrant destroy
```
