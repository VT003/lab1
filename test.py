import argparse
import subprocess

def start_container(container_names):
    print('Starting docker containers')
    for name in container_names:
      cmd = ['docker-compose', 'up', '-d', name]
      subprocess.run(cmd)
    print('Done Successfully')

def start_zebra_ospf(container_names):
    print('Starting Zebra and OSPF on routers')
    for name in container_names:
       subprocess.run(['docker', 'cp', './Dockerfiles/'+ name +'/zebra.conf', name +':/etc/quagga'])
       subprocess.run(['docker', 'cp', './Dockerfiles/'+ name +'/ospfd.conf', name +':/etc/quagga'])
       subprocess.run(['docker', 'exec', '-it', name, 'service', 'zebra', 'start'])
       subprocess.run(['docker', 'exec', '-it', name, 'service', 'ospfd', 'start'])
    print('Done Successfully')

def add_routes(routes):
    print('Adding routes to hosts')
    container, subnet, gateway = routes
    cmd = ['docker', 'exec', '-it', container, 'route', 'add', '-net', subnet, 'gw', gateway]
    subprocess.run(cmd)
    print('Done Successfully')

def configure_router(container, interface, cost):
    cmd = [
        f"configure terminal",
        f"router ospf",
        f"interface {interface}",
        f"ip ospf cost {cost}"
    ]
    for command in cmd:
        subprocess.run(["docker", "exec", "-it", container, "vtysh", "-c", command])

def south_path():
    print('Configuring network to go through R4')
    # Configure Router R1
    configure_router("r1", "eth1", 10)
    configure_router("r1", "eth2", 5)

    # Configure Router R4
    configure_router("r4", "eth0", 5)
    configure_router("r4", "eth1", 5)

    # Configure Router R3
    configure_router("r3", "eth1", 10)
    configure_router("r3", "eth2", 5)

def delete_container(container_names):
    for name in container_names:
        cmd = ['docker-compose', 'rm', '-fsv', name]
        subprocess.run(cmd)
    print('Done Successfully')


def main():
    argParser = argparse.ArgumentParser(prog="Lab1-Orchestrator", description="Automates all the docker commands reuired to build docker network for Lab1", epilog="Created by Vatsal Goel")

    argParser.add_argument(
        "-s", 
        "--start_container", 
        help="Starts docker container", 
        nargs= "*")
    argParser.add_argument(
        "-z", 
        "--start_zebra_ospf", 
        help="Copy Zebra & OSPF files to container and start services", 
        nargs= "*")
    argParser.add_argument(
        "-a", 
        "--add_routes", 
        help="Adds routes to the host", 
        nargs= "*")
    argParser.add_argument(
        "-p", 
        "--south_path", 
        help="Directs traffic to South path", 
        action = "store_true")
    argParser.add_argument(
        "-d", 
        "--delete_container", 
        help="Deletes docker container", 
        nargs= "*")
    
    arg = argParser.parse_args()

    if arg.start_container:
        start_container(arg.start_container)
    elif arg.start_zebra_ospf:
        start_zebra_ospf(arg.start_zebra_ospf)
    elif arg.add_routes:
        add_routes(arg.add_routes)
    elif arg.south_path:
        south_path()
    elif arg.delete_container:
        delete_container(arg.delete_container)

    if not any(vars(arg).values()):
        argParser.print_help()
        return
        

if __name__ == "__main__":
    main()
