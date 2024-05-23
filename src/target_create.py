from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from logger import Logger
from logger import Logger_levels as lvl

log_obj = Logger("/opt/log/app.log", False)
# Zwraca target_id
def create_target(target_name, hosts):
    # Połączenie z gvmd przez socket Unix
    connection = TLSConnection(hostname="localhost",port=9390)
    transform = EtreeTransform()

    # Utworzenie obiektu protokołu GMP
    with Gmp(connection=connection, transform = transform) as gmp:
        gmp.authenticate("admin","admin")
        # Utworzenie celu
        response = gmp.create_target(name=target_name, hosts=hosts, port_range="80-443")
        target_id = response.get('id')
        log_obj.log(f"Utworzono nowy cel o ID: {target_id}", lvl.INFO)
        return target_id
    
#print(create_target("target1", ["192.160.0.1"]))


