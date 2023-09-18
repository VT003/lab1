# Lab1 - Part3 Orchestrator Code
# VTG003

import os
import argparse
from optparse import OptionParser

# Install route for hosts
def host_routes(route_add):
    print("Adding route to Hosts")
    container_name, network, gateway = route_add
    rt = f"docker exec -it {container_name} route add -net {network} gw {gateway}"
    print('CMD: ' + rt)
    os.system(rt)

# Initialize docker containers 
def initialize_container(container_names):
    print("Starting Topology")
    initialize = 'docker-compose up -d'
    for name in container_names:
        initialize += ' ' + name
    print('CMD: ' + initialize)
    os.system(initialize)

# South Path (Routers: R1, R4, R3)
def south_path():
    print("South Path (Routers: r1, r4, r3)")

    os.system("docker exec -it r1 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 10'"'")
    os.system("docker exec -it r1 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth2'"' -c '"'ip ospf cost 5'"'")

    os.system("docker exec -it r4 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth0'"' -c '"'ip ospf cost 5'"'")
    os.system("docker exec -it r4 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 5'"'")

    os.system("docker exec -it r3 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 10'"'")
    os.system("docker exec -it r3 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth2'"' -c '"'ip ospf cost 5'"'")

# Copy zerbra.conf and ospfd.conf from system to container and start service
def start_OSPF(container_names):
    print("Starting Zebra & OSPF on Topology")
    for name in container_names:
        os.system("docker cp ./Dockerfiles/"+ name +"/zebra.conf "+ name + ":/etc/quagga")
        os.system("docker cp ./Dockerfiles/"+ name +"/ospfd.conf "+ name +":/etc/quagga")
        os.system("docker exec -it "+ name +" service zebra start")
        os.system("docker exec -it "+ name +" service ospfd start")

# Remove docker container 
def remove_container(container_names):
    remove = "docker-compose rm -fsv"
    for name in container_names:
        remove += ' ' + name
    print('CMD: ' + remove)
    os.system(remove)

# Main Function
def main():
    arg = OptionParser()
    arg.add_option('-i', '--initialize-container', action='store_true',
            dest='initialize', default=False, help='Initializes container. Give names of containers')
    arg.add_option('-o', '--ospf', action='store_true',
            dest='ospf', default=False, help='Starts Zebra and OSPF service. Give names of containers')
    arg.add_option('-a', '--add-routes', action='store_true',
            dest='routes', default=False, help='Installs routes on host')
    arg.add_option('-s', '--south', action='store_true',
            dest='south', default=False, help='Moves traffic in south direction')
    arg.add_option('-r', '--remove-container', action='store_true',
            dest='rm', default=False, help='Removes container. Give name of containers')
    (switch, var) = arg.parse_args()

    if switch.initialize:
        initialize_container(var)
    elif switch.ospf:
        start_OSPF(var)
    elif switch.routes:
        host_routes(var)
    elif switch.south:
        south_path()
    elif switch.rm:
        remove_container(var)
    else:
        print("Use -h for assistance")

if __name__ == "__main__":
    main()

