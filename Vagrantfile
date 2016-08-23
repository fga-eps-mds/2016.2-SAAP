# -*- mode: ruby -*-
# # vi: set ft=ruby :

require 'yaml'

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.ssh.insert_key = false
  config.vm.provider "virtualbox" do |vm, override| 
#    override.vm.network 'private_network', ip: "10.10.10.2"
    override.vm.network 'forwarded_port', guest: "8080" , host: "4567"
    override.vm.network 'forwarded_port', guest: "9869" , host: "9869"
    override.vm.network 'forwarded_port', guest: "80" , host: "9090"
  end

  env = ENV.fetch('SAAP_ENV', 'local')

  if File.exist?("config/#{env}/ips.yaml")
    ips = YAML.load_file("config/#{env}/ips.yaml")
  else
    ips = nil
  end

  config.vm.define 'digital_ocean' do |digital_ocean|
    digital_ocean.vm.provider "virtualbox" do |vm, override|
      override.vm.network 'private_network', ip: ips['digital_ocean'] if ips
      vm.memory = 2048
      vm.cpus = 2
    end
		digital_ocean.vm.provision "shell", inline: "sudo yum -y install rsync"
  end


#  config.vm.provision "chef_solo" do |chef|
#    chef.add_recipe "basics"
#  end

#  opennebula ready box

#config.ssh.username = 'root'
#config.ssh.password = 'opennebula'
end
