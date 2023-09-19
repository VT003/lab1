import argparse
import subprocess

def start_container(container_names):
    print('Starting docker containers')
    for name in container_names:
        cmd = ['docker-compose', 'up', '-d', name]
        subprocess.Popen(cmd)

def start_zebra_ospf(container_names):
    print('Starting Zebra and OSPF on routers')
    for name in container_names:
        subprocess.run(["docker", "cp", "./Dockerfiles/"+ name +"/zebra.conf", name + ":/etc/quagga"])
        subprocess.run(["docker", "cp", "./Dockerfiles/"+ name +"/ospfd.conf", name +":/etc/quagga"])
        subprocess.run(["docker", "exec", "-it", name, "service", "zebra", "start"])
        subprocess.run(["docker", "exec", "-it", name, "service", "ospfd", "start"])

def add_routes(routes):
    print('Adding routes to hosts')
    container, subnet, gateway = routes
    cmd = ['docker', 'exec', '-it', container, 'route add -net', subnet, 'gw', gateway]
    subprocess.Popen(cmd)

def south_path():
    print('Configuring network to go through R4')
    subprocess.run(["docker", "exec", "-it", "r1", "vtysh", "-c", "configure terminal", "-c", "router ospf", "-c", "interface eth1", "-c", "ip ospf cost 10"])
    subprocess.run(["docker", "exec", "-it", "r1", "vtysh", "-c", "configure terminal", "-c", "router ospf", "-c", "interface eth2", "-c", "ip ospf cost 5"])

    subprocess.run(["docker", "exec", "-it", "r3", "vtysh", "-c", "configure terminal", "-c", "router ospf", "-c", "interface eth1", "-c", "ip ospf cost 10"])
    subprocess.run(["docker", "exec", "-it", "r3", "vtysh", "-c", "configure terminal", "-c", "router ospf", "-c", "interface eth2", "-c", "ip ospf cost 5"])

    subprocess.run(["docker", "exec", "-it", "r4", "vtysh", "-c", "configure terminal", "-c", "router ospf", "-c", "interface eth0", "-c", "ip ospf cost 5"])
    subprocess.run(["docker", "exec", "-it", "r4", "vtysh", "-c", "configure terminal", "-c", "router ospf", "-c", "interface eth1", "-c", "ip ospf cost 5"])

def delete_container(container_names):
    for name in container_names:
        cmd = ['docker-compose', 'down', '-d', name]
        subprocess.Popen(cmd)


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
        "-sp", 
        "--south_path", 
        help="Directs traffic to South path", 
        nargs= "?")
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
        # If no flags are given, prints help and exit
        argParser.print_help()
        return
        

if __name__ == "__main__":
    main()