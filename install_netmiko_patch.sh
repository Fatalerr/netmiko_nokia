#!/usr/bin/bash
# liujun.gz@gmail.com

# NOTE: You should install the netmiko before execute this script.

site_path=$(pip show netmiko|awk '/Location/{print $2}')
echo 
echo "NOTE: You should install the netmiko before execute this script."
echo 
echo "Step.1 Find the location of the installed 'netmiko'"
echo " Result: $site_path"
echo

echo "Step.2 Install the patch to netmiko..."
tar -xzvf netmiko_nokia.tgz -C $site_path
echo 

echo "Step.3 Add two lines to 'ssh_dispatcher.py"
echo "  from netmiko.nokia.nokia_flexins_ssh import NokiaFlexinsSSH"
echo '  "nokia_flexins": NokiaFlexinsSSH, in the CLASS_MAPPER_BASE'
