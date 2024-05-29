from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from logger import Logger
from logger import Logger_levels as lvl


log_obj = Logger("/opt/log/app.log", False)

def delete_target(gmp):

    response_display_target = gmp.get_targets()

    target_info = response_display_target.xpath('.//target')
    targets_id = [target.get('id') for target in target_info]


    response1 = gmp.delete_target(targets_id[0])    
    if response1.get('status') =='400':
        log_obj.log("Failed to delete task",lvl.ERROR)
        return False
    log_obj.log(f"Target {response1.get('id')} deleted", lvl.INFO)
    


def delete_task(gmp):

    response_display_task = gmp.get_tasks()

    task_info = response_display_task.xpath('.//task')
    tasks_id = [task.get('id') for task in task_info]

    response1 = gmp.delete_task(tasks_id[0])

    pretty_print(response1)


def stop_task(gmp):

    response_display_task = gmp.get_tasks()

    task_info = response_display_task.xpath('.//task')
    tasks_id = [task.get('id') for task in task_info]

    response1 = gmp.stop_task(tasks_id[0])

    pretty_print(response1)

