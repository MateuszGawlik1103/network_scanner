from gvm.connections import TLSConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from lxml import etree
from gvm.protocols.gmpv208 import AlertCondition, AlertEvent, AlertMethod, ReportFormatType
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




def scan(target_name=None, hosts=None):
    # Połączenie z gvmd przez socket Unix
    connection = TLSConnection(hostname="localhost", port=9390)
    transform = EtreeTransform()
    # Utworzenie obiektu protokołu GMP
    with Gmp(connection=connection, transform=transform) as gmp:
        gmp.authenticate("admin", "admin")
        response = gmp.get_scanners()
        # Pobranie informacji o skanerach
        scanners_info = response.xpath('.//scanner')
        # Pobranie nazw skanerów
        scanner_names = [scanner.xpath('name/text()')[0] for scanner in scanners_info]
        for scanner in scanners_info:
            if scanner.xpath('name/text()')[0] == 'OpenVAS Default':
                # Pobranie ID skanera OpenVAS Default
                default_scanner_id = scanner.get('id')
        print("Id of default Openvas scanner:")
        print(default_scanner_id)
        #config_id
        #create_target
        #start_task

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
        print("Task id: ", task_id)
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
            print(f'{now_time.strftime("%H:%M:%S")}: {status}')
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
        print("PDF report created")


scan()
#Dane do logowania
email = 'fsdgsfgdfgfd'
password = 'rgsfdgdsgf'

# Tworzenie połączenia z serwerem SMTP Onet
server = smtplib.SMTP('smtp.poczta.interia.pl', 587)
server.starttls()

# Logowanie do serwera
server.login(email, password)

# Tworzenie wiadomości
adresat = 'fdsgfsfdgf'
# Multipurpose Internet Mail Extensions Multipart
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = adresat
msg['Subject'] = 'PDFskan1'

# Treść wiadomości
body = "Arsenal zwycięzcą Ligi Mistrzów i Premier League"
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

print("Wiadomość została wysłana pomyślnie.")







    