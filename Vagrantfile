# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-18.04"

  #config.vm.network "forwarded_port", guest: 8888, host: 8888
  config.vm.synced_folder ".", "/vagrant"

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

   config.vm.provision "ansible_local" do |ansible|
       ansible.playbook = "playbook.yml"
       compatibility_mode = "2.0"
   end
end
