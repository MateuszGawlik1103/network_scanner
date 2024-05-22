from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from lxml import etree
from gvm.protocols.gmpv208 import AlertCondition, AlertEvent, AlertMethod, ReportFormatType
from gvm.errors import GvmError
from logger import Logger
from logger import Logger_levels as lvl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import host_disc
import target_create
import base64
import io
import time
from pathlib import Path
from datetime import datetime, timedelta
import smtplib
from base64 import b64decode
from delete_task import delete_task, delete_target
import os


# Dane do logowania
email = os.environ.get('EMAIL')
# App password do maila
email_pass = os.environ.get('EMAIL_PASS')

log_obj = Logger("/opt/log/app.log", False)

def try_to_connect():
    while True:
        try:
            connection = TLSConnection(hostname="localhost",port=9390)
            log_obj.log("Connection established", lvl.INFO)
            return connection
        except GvmError | ConnectionRefusedError:
            log_obj.log("Connection failed. Retrying after 30s...", lvl.WARN)
            time.sleep(30)

def authenticate(gmp):
    response = gmp.authenticate("admin", "admin")
    if response.get('status') != '200':
        log_obj.log("Authentication failed", lvl.ERROR)
        return False
    log_obj.log("Authenticated to GVM", lvl.INFO)
    return True

def scan(target_name=None, hosts=None):
    # Połączenie z gvmd przez socket Unix
    connection = try_to_connect()
    transform = EtreeTransform()
    # Utworzenie obiektu protokołu GMP
    
    while True:
        try:
            with Gmp(connection=connection, transform=transform) as gmp:  
                authenticate(gmp)
                response = gmp.get_scanners()
                # Pobranie informacji o skanerach
                scanners_info = response.xpath('.//scanner')
                # Pobranie nazw skanerów
                scanner_names = [scanner.xpath('name/text()')[0] for scanner in scanners_info]
                for scanner in scanners_info:
                    if scanner.xpath('name/text()')[0] == 'OpenVAS Default':
                        # Pobranie ID skanera OpenVAS Default
                        default_scanner_id = scanner.get('id')
                log_obj.log(f"Id of default Openvas scanner: {default_scanner_id}", lvl.INFO)


                # Id konfiguracji 'Full and fast'
                config_response = gmp.get_scan_configs()
                # Pobranie informacji o konfiguracji skanowania
                configs_info = config_response.xpath('.//config')
                for config in configs_info:
                    if config.xpath('name/text()')[0] == 'Full and fast':
                        # Pobranie ID konfiguracji skanowania 'Full and fast'
                        config_id = config.get('id')



                # Stworzenie celu
                # Pobranie sieci z interfejsow
                inet_adresses = host_disc.get_inet_addresses()
                # Lista aktywnych hostow ze wszystkich interfejsow
                all_active_hosts = []
                for inet_adress in inet_adresses:
                    # Lista aktywnych hostow z poszczegolnych interfejsow
                    active_hosts = host_disc.get_active_hosts(inet_adress)
                    all_active_hosts.extend(active_hosts)
                target_id = target_create.create_target("New target1", all_active_hosts)
                
                # Stworzenie polecenia (task)
                response_task = gmp.create_task('Task1', config_id, target_id, default_scanner_id)
                task_id = response_task.get('id')
                log_obj.log("Task id: ", task_id, lvl.INFO)
                pretty_print(response_task)

                # Start skanu
                gmp.start_task(task_id=task_id)
                task_ready = False
                # Sprawdzenie, czy skan gotowy
                while not task_ready:
                    got_task = gmp.get_task(task_id)
                    status = got_task.find(".//status").text
                    if status == 'Done':
                        task_ready = True
                    now_time = datetime.now()
                    log_obj.log(f'{now_time.strftime("%H:%M:%S")}: {status}', lvl.INFO)
                    time.sleep(30)
                ready_task = gmp.get_task(task_id)
                report_id = ready_task.find(".//task").find('.//report').attrib.get("id")
                report = gmp.get_report(report_id=report_id, details=True, report_format_id=ReportFormatType.PDF,
                                        filter_string="apply_overrides=0 levels=hmlg rows=100 min_qod=70 first=1 sort-reverse=severity")
                report_element = report.find("report")
                content = report_element.find("report_format").tail
                binary_base64_encoded_pdf = content.encode('ascii')
                binary_pdf = b64decode(binary_base64_encoded_pdf)
                pdf_path = Path('report.pdf').expanduser()
                # Zapis do pdf
                pdf_path.write_bytes(binary_pdf)
                delete_task()
                delete_target()
                log_obj.log("PDF report created", lvl.SUCCESS)
                send_email(email, email_pass)
                break
        except ConnectionRefusedError:
            print("connection refused. Retrying after 30s...")
            time.sleep(30)
            continue

    




def send_email(email, email_pass):
    # Tworzenie połączenia z serwerem SMTP gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    # Logowanie do serwera
    server.login(email, email_pass)
    
    # Tworzenie wiadomości
    adresat = email
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = adresat
    msg['Subject'] = 'PDFtest'
    
    # Treść wiadomości
    body = "Arsenal winning the league (next season...)"
    msg.attach(MIMEText(body, 'plain'))
    file = "report.pdf"
    # Dodawanie pliku PDF
    with open(file, "rb") as attachment:
        part = MIMEApplication(attachment.read(), _subtype="pdf")
        part.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(part)
    
    # Wysyłanie wiadomości
    server.sendmail(email, adresat, msg.as_string())
    
    # Zamykanie połączenia
    server.quit()
    
    log_obj.log("Message sent succesfully.", lvl.SUCCESS)


if __name__ =='__main__':
    scan()







    