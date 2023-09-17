# Lab1 - Part3 Orchestrator Code
# VTG003

import os
import sys
from optparse import OptionParser
import argparse

# Initialize docker containers 
def initialize_container(containers):
    print("Starting topology")
    build = 'docker-compose up -d'
    for dc in containers:
        build += ' ' + dc

    print('CMD: ' + build)
    os.system(build)

# Copy zerbra.conf and ospfd.conf from system to container and start service
def start_OSPF(containers):
    print("Starting OSPF on Topology")

    for dc in containers:
        os.system("docker cp ./Dockerfiles/"+ dc +"/zebra.conf "+ dc + ":/etc/quagga")
        os.system("docker cp ./Dockerfiles/"+ dc +"/ospfd.conf "+ dc +":/etc/quagga")
        os.system("docker exec -it "+ dc +" service zebra start")
        os.system("docker exec -it "+ dc +" service ospfd start")

# Install route for hosts
def endpoint_routes(route):
    print("Adding route to Hosts")
    r = "docker exec -it " + route[0] + " route add -net " + route[1] + " gw " + route[2]
    print('CMD: ' + r)
    os.system(r)

# North Path (Routers: R1, R2, R3)
def north_path():
    print("North Path (Routers: r1, r2, r3)")

    #For R1
    os.system("docker exec -it r1 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 5'"'")
    os.system("docker exec -it r1 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth2'"' -c '"'ip ospf cost 10'"'")

    #For R2
    os.system("docker exec -it r2 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth0'"' -c '"'ip ospf cost 5'"'")
    os.system("docker exec -it r2 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 5'"'")

    #For R3
    os.system("docker exec -it r3 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth0'"' -c '"'ip ospf cost 5'"'")
    os.system("docker exec -it r3 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 10'"'")

    #For R4
    os.system("docker exec -it r4 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth0'"' -c '"'ip ospf cost 10'"'")
    os.system("docker exec -it r4 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 10'"'")

# South Path (Routers: R1, R4, R3)
def south_path():
    print("South Path (Routers: r1, r4, r3)")

    #For R1
    os.system("docker exec -it r1 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 10'"'")
    os.system("docker exec -it r1 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth2'"' -c '"'ip ospf cost 5'"'")

    #For R2
    os.system("docker exec -it r2 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth0'"' -c '"'ip ospf cost 10'"'")
    os.system("docker exec -it r2 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 10'"'")

    #For R3
    os.system("docker exec -it r3 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth0'"' -c '"'ip ospf cost 10'"'")
    os.system("docker exec -it r3 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 5'"'")

    #For R4
    os.system("docker exec -it r4 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth0'"' -c '"'ip ospf cost 5'"'")
    os.system("docker exec -it r4 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 5'"'")

# Remove docker container 
def remove_container(containers):
    remove = "docker-compose rm -fsv"
    for dc in containers:
        remove += ' ' +  dc

    print('CMD: ' + remove)
    os.system(remove)

# Main Function
def main():
    arg = argparse.ArgumentParser()
    arg.add_argument('-u', '--initialize-container', action='store_true',
            dest='initialize', default=False, help='Initialize container. Give names of containers')
    arg.add_argument('-o', '--ospf', action='store_true',
            dest='ospf', default=False, help='Start Zebra and OSPF. Give names of containers')
    arg.add_argument('-p', '--add-routes', action='store_true',
            dest='routes', default=False, help='Install routes on host.')
    arg.add_argument('-n', '--north', action='store_true',
            dest='north', default=False, help='Move traffic to north path')
    arg.add_argument('-s', '--south', action='store_true',
            dest='south', default=False, help='Move traffic to south path')
    arg.add_argument('-r', '--remove-container', action='store_true',
            dest='stop', default=False, help='Remove container. Give name of containers')
    variable = arg.parse_args()

    # Choose which option to follow through
    action_map = {
        'initialize': initalize_container,
        'ospf': start_OSPF,
        'routes': endpoint_routes,
        'north': north_path,
        'south': south_path,
        'stop': remove_container
    }

    action = action_map.get(variable.action)
    if action:
        action(variable)
    else:
        print("Use -h for assistance")

if __name__ == "__main__":
    main()

