from enum import Enum
from datetime import datetime, timedelta
class Logger:
    def __init__(self,log_file_path, debug_on):
        self.log_file_path = log_file_path
        self.debug_on = debug_on

    def log(self, message, level):
        now = datetime.now()
        now = now + timedelta(hours=2)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if (level == Logger_levels.DEBUG):
            if (self.debug_on == True):
                print(f"[{dt_string}][DEBUG] {message}");
                self.write_to_file(f"[{dt_string}][DEBUG] {message}\n")
        elif (level == Logger_levels.INFO):
            print(f"[{dt_string}][INFO] {message}");
            self.write_to_file(f"[{dt_string}][INFO] {message}\n")
        elif (level == Logger_levels.WARN):
            print(f"[{dt_string}][WARN] {message}");
            self.write_to_file(f"[{dt_string}][WARN] {message}\n")
        elif (level == Logger_levels.ERROR):
            print(f"[{dt_string}][ERROR] {message}");
            self.write_to_file(f"[{dt_string}][ERROR] {message}\n")
        elif (level == Logger_levels.SUCCESS):
            print(f"[{dt_string}][SUCCESS] {message}");
            self.write_to_file(f"[{dt_string}][SUCCESS] {message}\n")
        else:
            print("Invalid log level")

    def write_to_file(self, message):
        with open(self.log_file_path, "a") as f:
            f.write(message)



class Logger_levels(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    SUCCESS = 4