import nmap
import netifaces
import ipaddress


# Zwraca liste sieci interfejsow
def get_inet_addresses():
    # Pobierz informacje o interfejsach sieciowych
    interfaces = netifaces.interfaces()
    netmask = '255.255.255.0'
    ipaddr = []
    # Usuniecie interfejsu loopback z listy
    interfaces.pop(0)
    print(interfaces)
    # Przeiteruj przez interfejsy sieciowe
    for interface in interfaces:
        # Sprawdz czy interfejs ma adres IPv4
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            # Pobierz informacje o adresach IPv4 interfejsu
            addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET]
            print("Adresy na interfejsie ", interface, ": ", addresses)
            
        # Przeiteruj przez adresy IPv4 interfejsu
        for addr_info in addresses:
            ip=addr_info['addr']
            ip_net = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
            print(ip_net)
            ipaddr.append(ip_net)
    return ipaddr

	

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


