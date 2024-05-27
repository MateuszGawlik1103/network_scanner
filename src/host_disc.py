import nmap
import ipaddress


import ipaddress

def get_inet_addresses(host_ip):
    # Podziel adres IP i maskę podsieci
    ip, mask = host_ip.split('/')
    
    # Utwórz obiekt adresu IP
    ip_address = ipaddress.IPv4Address(ip)
    
    # Utwórz obiekt maski podsieci
    subnet_mask = int(mask)
    
    # Utwórz adres sieci
    network_address = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False).network_address
    
    return network_address

# Przykładowe użycie


# Zwraca liste aktywnych hostow w danej sieci
def get_active_hosts(ip):
    ip_net = str(ip)
    active_hosts = []

    # Utworz obiekt skanera Nmap
    nm = nmap.PortScanner()

    # Skanuj podsiec w poszukiwaniu aktywnych hostow
    nm.scan(hosts=ip_net, arguments='-sn')

    # Iteruj przez wyniki skanowania
    for host in nm.all_hosts():
        active_hosts.append(host)

    return active_hosts


