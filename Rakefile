require 'yaml'
require "chake"

$SAAP_ENV = ENV.fetch('SAAP_ENV', 'local')

ssh_config_file = "config/#{$SAAP_ENV}/ssh_config"
ips_file = "config/#{$SAAP_ENV}/ips.yaml"
config_file = "config/#{$SAAP_ENV}/config.yaml"
iptables_file = "config/#{$SAAP_ENV}/iptables-filter-rules"

ENV['CHAKE_TMPDIR'] = "tmp/chake.#{$SAAP_ENV}"
ENV['CHAKE_SSH_CONFIG'] = ssh_config_file

chake_rsync_options = ENV['CHAKE_RSYNC_OPTIONS'].to_s.clone
chake_rsync_options += ' --exclude backups'
chake_rsync_options += ' --exclude src'
ENV['CHAKE_RSYNC_OPTIONS'] = chake_rsync_options

if Gem::Version.new(Chake::VERSION) < Gem::Version.new('0.10')
  fail "Please upgrade to chake 0.10+"
end

ips ||= YAML.load_file(ips_file)
config ||= YAML.load_file(config_file)
firewall ||= File.open(iptables_file).read
config['keep_yum_cache'] = ENV['keep_yum_cache'] ? true : false

$nodes.each do |node|
  node.data['environment'] = $SAAP_ENV
  node.data['config'] = config
  node.data['peers'] = ips
  node.data['firewall'] = firewall
end
