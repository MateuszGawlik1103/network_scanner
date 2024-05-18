from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print

def delete_target():
    # Konfiguracja połączenia z GMP 
    conn = TLSConnection(hostname="localhost", port=9390)
    transform = EtreeTransform()
    gmp = Gmp(connection=conn, transform=transform)

    # Uwierzytelnianie
    gmp.authenticate(username='admin', password='admin')

    response_display_target = gmp.get_targets()

    target_info = response_display_target.xpath('.//target')
    targets_id = [target.get('id') for target in target_info]



    # Pobranie informacji o wszystkich zadaniach
    response1 = gmp.delete_target(targets_id[0])

    pretty_print(response1)


def delete_task():
    # Konfiguracja połączenia z GMP 
    conn = TLSConnection(hostname="localhost", port=9390)
    transform = EtreeTransform()
    gmp = Gmp(connection=conn, transform=transform)

    # Uwierzytelnianie
    gmp.authenticate(username='admin', password='admin')

    response_display_task = gmp.get_tasks()

    task_info = response_display_task.xpath('.//task')
    tasks_id = [task.get('id') for task in task_info]



    # Pobranie informacji o wszystkich zadaniach
    response1 = gmp.delete_task(tasks_id[0])

    pretty_print(response1)


def stop_task():
    # Konfiguracja połączenia z GMP 
    conn = TLSConnection(hostname="localhost", port=9390)
    transform = EtreeTransform()
    gmp = Gmp(connection=conn, transform=transform)

    # Uwierzytelnianie
    gmp.authenticate(username='admin', password='admin')

    response_display_task = gmp.get_tasks()

    task_info = response_display_task.xpath('.//task')
    tasks_id = [task.get('id') for task in task_info]


    # Pobranie informacji o wszystkich zadaniach
    response1 = gmp.stop_task(tasks_id[0])

    pretty_print(response1)



if __name__ == "__main__":

    delete_task()
    delete_target()
