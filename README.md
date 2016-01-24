Caddy Ansible Role
=========

Installs Caddy

Dependencies
------------
None

Role Variables
--------------

Email is used for the lets encrypt integration:<br>
example:
```
caddy_email: foo@foo.bar
```
Features that can be added to core: cors,git,hugo,ipfilter,jsonp,search<br>
default:
```
caddy_features: git
```
List of sites and their options<br>
example:
```
caddy_sites:
  foo.bar:
    - root /var/www
    - gzip
```
Directives like git are also possible (notice the semicolons)<br>
example:
```
caddy_sites:
  foo.bar:
    - root /var/www
    - git github.com/user/site {
        branch development;
      }
```
Site indepentent config options<br>
default:
```
caddy_config:
  - gzip
```

Example Playbook
----------------

Example coming
