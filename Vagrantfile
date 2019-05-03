# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-18.04"
  #config.vm.network "forwarded_port", guest: 8888, host: 8888
  config.vm.synced_folder ".", "/vagrant"
  config.vm.provision "shell", path: "bootstrap.sh", privileged: false

  # Provider specific configuration options
  config.vm.provider "virtualbox" do |vb|
      vb.customize [
        "modifyvm", :id,
        "--cpus", "2",
        "--ioapic", "on",
        "--memory", "2048",
        "--cableconnected1", "on",
      ]
  end
end
