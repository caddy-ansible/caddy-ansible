# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "wheezy" do |wheezy|
    wheezy.vm.box = "debian/wheezy64"
  end

  config.vm.define "jessie" do |jessie|
    jessie.vm.box = "debian/jessie64"
  end

  config.vm.define "precise" do |precise|
    precise.vm.box = "ubuntu/precise64"
  end

  config.vm.define "trusty" do |trusty|
    trusty.vm.box = "ubuntu/trusty64"
  end

  config.vm.define "centos6" do |centos6|
    centos6.vm.box = "geerlingguy/centos6"
  end

  config.vm.define "centos7" do |centos7|
    centos7.vm.box = "centos/7"
  end

  config.vm.provision "ansible" do |ansible|
      ansible.playbook = 'tests/test.yml'
  end

  $script = <<SCRIPT
  # curl localhost and get the http response code
  http_code=$(curl --silent --output /dev/null --connect-time 10 -w '%{http_code}' localhost:2020)
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
