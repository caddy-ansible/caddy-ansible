# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "trusty" do |trusty|
    trusty.vm.box = "ubuntu/trusty64"
  end

  config.vm.define "centos7" do |centos7|
      centos7.vm.box = "centos/7"
  end

  config.vm.provision "ansible" do |ansible|
      ansible.playbook = 'tests/test.yml'
  end
end
