# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.define "buster" do |buster|
    buster.vm.box = "debian/buster64"
  end

  config.vm.define "bionic" do |bionic|
    bionic.vm.box = "bento/ubuntu-18.04"
  end

  config.vm.define "focal" do |focal|
    focal.vm.box = "bento/ubuntu-20.04"
  end

  config.vm.define "centos7" do |centos7|
    centos7.vm.box = "bento/centos-7.6"
  end

  config.vm.define "fedora32" do |fedora32|
    fedora32.vm.box = "bento/fedora-32"
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = 'tests/playbook.yml'
    ansible.verbose = true
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
    000)     echo "$http_code | Server not accessible!" >&2 ; exit 1 ;;
    *)       echo "$http_code | Unknown http response code!" >&2 ; exit 1 ;;
  esac
SCRIPT

  # Fix 'stdin: is not a tty' error
  config.ssh.pty = true
  config.vm.provision :shell, inline: $script

  config.vm.synced_folder ".", "/vagrant", disabled: true
end
