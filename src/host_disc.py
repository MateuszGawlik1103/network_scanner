import nmap
import ipaddress

def get_inet_addresses(host_ip):
    # Split the IP address and subnet mask
    ip, mask = host_ip.split('/')
    
    # Create an IP address object
    ip_address = ipaddress.IPv4Address(ip)
    
    # Create a subnet mask object
    subnet_mask = int(mask)
    
    # Create a network address
    network_address = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    
    return network_address

# Example usage
#print(get_inet_addresses("192.168.43.224/24"))

# Returns a list of active hosts in the given network
def get_active_hosts(ip):
    ip_net = str(ip)
    active_hosts = []

    # Create a Nmap scanner object
    nm = nmap.PortScanner()

    # Scan the subnet for active hosts
    nm.scan(hosts=ip_net, arguments='-sn')

    # Iterate through the scan results
    for host in nm.all_hosts():
        active_hosts.append(host)

    return active_hosts
