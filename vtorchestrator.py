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
def host_routes(route):
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
    os.system("docker exec -it r3 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 5'"'")
    os.system("docker exec -it r3 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth2'"' -c '"'ip ospf cost 10'"'")

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
    os.system("docker exec -it r3 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth1'"' -c '"'ip ospf cost 10'"'")
    os.system("docker exec -it r3 vtysh -c '"'configure terminal'"' -c '"'router ospf'"' -c '"'interface eth2'"' -c '"'ip ospf cost 5'"'")

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
    arg = OptionParser()
    arg.add_option('-i', '--initialize-container', action='store_true',
            dest='initialize', default=False, help='Initializes container. Give names of containers')
    arg.add_option('-o', '--ospf', action='store_true',
            dest='ospf', default=False, help='Starts Zebra and OSPF service. Give names of containers')
    arg.add_option('-a', '--add-routes', action='store_true',
            dest='routes', default=False, help='Installs routes on host')
    arg.add_option('-n', '--north', action='store_true',
            dest='north', default=False, help='Moves traffic in north direction')
    arg.add_option('-s', '--south', action='store_true',
            dest='south', default=False, help='Moves traffic in south direction')
    arg.add_option('-r', '--remove-container', action='store_true',
            dest='rm', default=False, help='Removes container. Give name of containers')
    (options, var) = arg.parse_args()

    if options.initialize:
        initialize_container(var)
    elif options.ospf:
        start_OSPF(var)
    elif options.routes:
        host_routes(var)
    elif options.north:
        north_path()
    elif options.south:
        south_path()
    elif options.rm:
        remove_container(var)
    else:
        print("Use -h for assistance")

if __name__ == "__main__":
    main()
