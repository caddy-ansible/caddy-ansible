# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.define "buster" do |buster|
    buster.vm.box = "debian/buster64"
  end

  config.vm.define "bionic" do |bionic|
    bionic.vm.box = "bento/ubuntu-18.04"
  end

  config.vm.define "centos7" do |centos7|
    centos7.vm.box = "bento/centos-7.3"
  end

  config.vm.define "fedora29" do |fedora29|
    fedora29.vm.box = "bento/fedora-29"
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = 'tests/playbook.yml'
  end

  $script = <<SCRIPT
  # curl localhost and get the http response code
  while ! curl -Is localhost:2020 -o /dev/null; do
    sleep 1 && echo -n .
  done
  echo
  http_code=$(curl --silent --head --output /dev/null -w '%{http_code}' localhost:2020)
  case $http_code in
    200|404) echo "$http_code | Server running" ;;
    000)     echo "$http_code | Server not accessible!" >&2 ;;
    *)       echo "$http_code | Unknown http response code!" >&2 ;;
  esac
SCRIPT

  # Fix 'stdin: is not a tty' error
  config.ssh.pty = true
  config.vm.provision :shell, inline: $script

  config.vm.synced_folder ".", "/vagrant", disabled: true
end
